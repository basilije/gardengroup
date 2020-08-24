#!/usr/bin/python3

import Adafruit_GPIO.SPI as a
import csv as c
import datetime as d
import RPi.GPIO as g
import threading as h
import Adafruit_MCP3008 as m
import os as o
import time as t
import sqlite3 as q
  
def connectToSpecificDatabase():
    sqliteConnection = None
    try:
        sqlite_database_name = sqlite_db_folder_name + str(d.datetime.now()).split(" ")[0] +'.db'
        sqliteConnection = q.connect(sqlite_database_name)
    except:
        print("Not Successfully Connected to database", sqlite_database_name)
    return sqliteConnection

def createTable(sqliteConnection):
    try:
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS records (P0 INT NOT NULL, P1 INT NOT NULL, P2 INT NOT NULL, P3 INT NOT NULL, P4 INT NOT NULL, P5 INT NOT NULL, P6 INT NOT NULL, P7 INT NOT NULL, dt TEXT NOT NULL);'''
        cursor = sqliteConnection.cursor()    
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created or already exists")
        cursor.close()  
    except Exception as ex:
        print(type(ex), ex.args)

def insertRecord(connection, record):
    sql = ''' INSERT INTO records(P0,P1,P2,P3,P4,P5,P6,P7,dt) VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, record)
    connection.commit()
 
def printHeader():
    # Print nice channel column headers.
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
    print('-' * 57)    

def getMCPDevice(hardware = True):
    mcp = None
    if hardware:
        # Hardware SPI configuration:
        SPI_PORT   = 0
        SPI_DEVICE = 0
        mcp = m.MCP3008(spi=a.SpiDev(SPI_PORT, SPI_DEVICE))   
    return mcp

def initializeLog(log_file_name, table_header):
    appendListAsRow(log_file_name, table_header)
    print('-' * 57, log_file_name)
    fi = open(log_file_name, "w+").close()    

def appendLog(log_file_name, values):
    values.append(d.datetime.now())  # Append the date and time.
    log = [str(v) for v in values]  # To the list of a strings.
    print(log) # Why not?
    appendListAsRow(log_file_name, log)      
    
def appendListAsRow(file_name, list_of_elem):   
    try:
        write_obj= open(file_name, 'a+', newline='') # Open file in append mode
        csv_writer = c.writer(write_obj)  # Create a writer object from csv module
        csv_writer.writerow(list_of_elem)  # Add contents of list as last row in the csv file
    except Exception as ex:
        print(ex.type(), ex.args, " appending problem")
     
def gpioON(gpio,s):
    if s>0:
        g.output(gpio, g.LOW)
        t.sleep(s)

def gpioOFF(gpio):
    g.output(gpio, g.HIGH)
  
def gpioOnTime(no_gpio, on_time):
    print("COMMAND:", no_gpio, on_time)
    
    g.setmode(g.BCM)
    g.setup(no_gpio,g.OUT, initial=g.HIGH)

    gpioOFF(no_gpio)
    gpioON(no_gpio, on_time)
    gpioOFF(no_gpio)   

def mainCommand(command_file_name):
    try:
        on_time = 0
        int_in_file = open(command_file_name).read()
        if int_in_file != "":
            on_time = int(float(int_in_file)*100) / 100.
        no_gpio = int(command_file_name.replace(".txt",""))    
        h.Thread(target=gpioOnTime, args=(no_gpio, on_time)).start()
    except Exception as ex:
        print(ex.type(), ex.args, " main problem")

 
# Main program loop.
sqlite_db_folder_name = "dbs/"
log_folder_name = "logs/"
log_file_name = log_folder_name + str(d.datetime.now()).replace(":","").replace("-","").replace(" ","_").replace(".",",")+".csv"
table_header = ["P0","P1","P2","P3","P4","P5","P6","P7","Date"]
range_of_gpio_pins = range(25)
table_in_db_created = False
loop_sleep = 0.51

mcp = getMCPDevice()                
printHeader()
initializeLog(log_file_name, table_header)

while True: 
    # Read all the ADC.   
    try:
        adc_values = [mcp.read_adc(i) for i in range(8)]
        appendLog(log_file_name, adc_values)
    except Exception as ex:
        print(ex.type(), ex.args, "ooops")
        adc_values = [0] * 8   
    t.sleep(loop_sleep)  # Pause for half a second.

    # Find if there is some of the gpio-named files.     
    for ch in range_of_gpio_pins:
        # find if there is any command file left:
        command_file_name = str(ch) + ".txt"
        if o.path.exists(command_file_name):
            # if exists, do the GPIO thing:
            mainCommand(command_file_name)            
            try:
                o.remove(command_file_name)            
            except Exception as ex:
                print("no command file name", ex.type(), ex.args)            
     
    # Write the log to the database.         
    try:
        sqliteConnection = connectToSpecificDatabase()
        if not(table_in_db_created):
            createTable(sqliteConnection)
            table_in_db_created = True
        insertRecord(sqliteConnection, adc_values)
        if (sqliteConnection):
            sqliteConnection.close()        
    except Exception as ex:
        print("SQL error", type(ex), ex.args)
