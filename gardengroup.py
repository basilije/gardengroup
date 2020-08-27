#!/usr/bin/python3

import Adafruit_GPIO.SPI as a
import csv as c
import datetime as d
import RPi.GPIO as g
import threading as h
import Adafruit_MCP3008 as m
import os as o
import configparser as p
import sqlite3 as q
from time import sleep as s


def printException(text, exce):
    print(text, type(exce), exce.args)

def connectToSpecificDatabase(sqlite_db_folder_name):
    connection = None
    try:
        sqlite_database_name = sqlite_db_folder_name + str(d.datetime.now()).split(" ")[0] +'.db'
        connection = q.connect(sqlite_database_name)
    except Exception as ex:
        printException("CONNECT TO DB " + sqlite_database_name +" EXCEPTION ", ex)
    return connection

def createTable(sqlite_connection):
    try:
        sqlite_create_table_query = '''CREATE TABLE records (P0 INT NOT NULL, P1 INT NOT NULL, P2 INT NOT NULL, P3 INT NOT NULL, P4 INT NOT NULL, P5 INT NOT NULL, P6 INT NOT NULL, P7 INT NOT NULL, dt TEXT NOT NULL);'''
        cursor = sqlite_connection.cursor()    
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        cursor.close()  
    except Exception as ex:
        printException("CREATE TABLE EXCEPTION ", ex)

def insertRecord(sqlite_connection, record):
    try:
        sql = ''' INSERT INTO records(P0,P1,P2,P3,P4,P5,P6,P7,dt) VALUES(?,?,?,?,?,?,?,?,?) '''
        cur = sqlite_connection.cursor()
        cur.execute(sql, record)
        sqlite_connection.commit()
    except Exception as ex:
        printException("INSERT RECORD EXCEPTION", ex)

def printHeader():
    # Print nice channel column headers.
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
    print('-' * 57)    

def getMCPDevice(hardware = True):
    mcp = None
    try:
        if hardware:
            # Hardware SPI configuration:
            SPI_PORT, SPI_DEVICE = 0, 0
            mcp = m.MCP3008(spi=a.SpiDev(SPI_PORT, SPI_DEVICE))  
    except Exception as ex:
        printException("GET MCP EXCEPTION ", ex)  
    return mcp

def appendListAsRow(file_name, list_of_elem):   
    try:
        write_obj= open(file_name, 'a+', newline='') # Open file in append mode
        csv_writer = c.writer(write_obj)  # Create a writer object from csv module
        csv_writer.writerow(list_of_elem)  # Add contents of list as last row in the csv file
    except Exception as ex:
        printException("APPEND LIST AS ROW EXCEPTION ", ex)

def initializeLog(log_file_name, table_header):
    try:
        appendListAsRow(log_file_name, table_header)
        print('-' * 57, '\n>>>', log_file_name)
        fi = open(log_file_name, "w+").close()    
    except Exception as ex:
        printException("INITIALIZE LOG EXCEPTION ", ex)

def appendLog(log_file_name, values):
    try:
        values.append(d.datetime.now())  # Append the date and time.
        log = [str(v) for v in values]  # To the list of a strings.
        print(log) # Why not?
        appendListAsRow(log_file_name, log)      
    except Exception as ex:
        printException("APPEND LOG EXCEPTION ", ex)
     
def gpioON(gpio,sec):
    if sec>0:
        g.output(gpio, g.LOW)
        s(sec)

def gpioOFF(gpio):
    g.output(gpio, g.HIGH)
  
def gpioOnTime(no_gpio, on_time):
    print("COMMAND:", no_gpio, on_time)
    
    g.setmode(g.BCM)
    g.setup(no_gpio,g.OUT, initial=g.HIGH)

    gpioOFF(no_gpio)
    gpioON(no_gpio, on_time)
    gpioOFF(no_gpio)   

def fileToThread(command_file_name):
    try:
        on_time = 0
        int_in_file = open(command_file_name).read()
        if int_in_file != "":
            on_time = int(float(int_in_file)*100) / 100.
        no_gpio = int(command_file_name.replace(".txt",""))    
        h.Thread(target=gpioOnTime, args=(no_gpio, on_time)).start()
    except Exception as ex:
        printException("FILE TO THREAD EXCEPTION ", ex)

def compareValues(adc_values, ad_in, cmp_sign, ad_value):
    value1 = float(adc_values[int(ad_in)])
    value2 = float(ad_value)
    to_return = None
    if cmp_sign == "<":
        to_return = (value1 < value2)
    if cmp_sign == ">":
        to_return = (value1 > value2)
    if cmp_sign == "=":
        to_return = (value1 == value2)
    if cmp_sign == "!=":
        to_return = (value1 != value2)
    return(to_return)

 
# Main program loop.
sqlite_db_folder_name = "dbs/"
log_folder_name = "logs/"
log_file_name = log_folder_name + str(d.datetime.now()).replace(":","").replace("-","").replace(" ","_").replace(".",",")+".csv"
table_header = ["P0","P1","P2","P3","P4","P5","P6","P7","Date"]
range_of_gpio_pins = range(25)
table_in_db_created = False
mcp = getMCPDevice()                
printHeader()
initializeLog(log_file_name, table_header)
loop_sleep = 0.5
port_to_use = None
port_time = d.datetime.now()
ad_in = None
cmp_sign = None
ad_value = None
on_gpio_port = None
gpio_duration = None
gpio_wait = None
cfg_file_name = 'cfg.cfg'
cfg_port_section = 'gpio'
cfg_criteria_section = 'criteria'
cp = p.ConfigParser()

while True:
    loop_sleep = 0.5
    # Read all the ADC.
    adc_values = [0] * 8    
    try:
        adc_values = [mcp.read_adc(i) for i in range(8)]
        appendLog(log_file_name, adc_values)
    except Exception as ex:
        printException("READ ADC EXCEPTION ", ex)        


# Find if there is some of the gpio-named files.     
    for ch in range_of_gpio_pins:
# find if there is any command file left:
        command_file_name = str(ch) + ".txt"
        
        if o.path.exists(command_file_name):
# if exists, do the GPIO thing:
            fileToThread(command_file_name)  
                      
            try:
                o.remove(command_file_name)            
            except Exception as ex:
                printException("NO COMMAND FILE NAME EXCEPTION ", ex)            

# AI things    
    try:
        # Read the configuration file 
        cp.read(cfg_file_name)
        
        for cfg_variable,cfg_value in cp.items(cfg_criteria_section):
            if cfg_variable == 'ad_in': ad_in = cfg_value   
            if cfg_variable == 'cmp_sign': cmp_sign = cfg_value   
            if cfg_variable == 'ad_value': ad_value = cfg_value   
            if cfg_variable == 'on_gpio_port': on_gpio_port  = cfg_value   
            if cfg_variable == 'gpio_duration': gpio_duration = cfg_value   
            if cfg_variable == 'gpio_wait': gpio_wait = float(cfg_value)
            if cfg_variable == 'loop_sleep': loop_sleep = float(cfg_value)

        for cfg_variable,cfg_value in cp.items(cfg_port_section):
            if (on_gpio_port=='1') and cfg_variable == 'port1': port_to_use = cfg_value  
            if (on_gpio_port=='2') and cfg_variable == 'port2': port_to_use = cfg_value 
             
        res = compareValues(adc_values, ad_in, cmp_sign, ad_value)
        
        if res:
            delta_time = d.datetime.now()- port_time
            if delta_time.total_seconds()>float(gpio_wait):
                command_file_name = str(port_to_use) + ".txt"
                fi = open(command_file_name, "w+")
                fi.write(gpio_duration)
                fi.close()
                port_time = d.datetime.now()
            else:
                print("GPIO waiting...",delta_time.total_seconds(),gpio_wait)
                    
    except Exception as ex:
        printException("AI EXCEPTION ", ex)

# Write the log to the database.      
    try:   
        sqlite_connection = connectToSpecificDatabase(sqlite_db_folder_name)
        if not(table_in_db_created):
            createTable(sqlite_connection)
            table_in_db_created = True
        insertRecord(sqlite_connection, adc_values)
        if (sqlite_connection):
            sqlite_connection.close()        
    except Exception as ex:
        printException("SQL EXCEPTION ", ex)
  
    s(loop_sleep)
