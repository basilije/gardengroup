gardengroup are: Kelsey Slavin, Javier Dominguez, Curtis Aloia and Vasilije Mehandzic.


gardengroup.py and cfg.cfg should be in /home/pi/gardengroup/
index.php should be in your nginx running folder (/var/www/html/)
File 'install_script.sh' is probably the best way how to install everything properly
To ensure each command runs well, copy and paste each into terminal. Many need a (Y/n) prompt at the end.
phpChart_Lite.zip should be unpacked (as sudo) into /var/www/html/phpChartLite/

Using cfg file:
[gpio]           Selecting which gpio ports will be controlled by program.
port1 = 20  
port2 = 21

[web]            Changing button settings
refresh = 2
button_style = 'style="height:57px;"' 

[default]
input = P3         Default MCP3008 input
values = 50        How many of the last values to display
auto_refresh = off Whether to refresh page on loop

[criteria]
ad_in = 3         Choose which signal in
cmp_sign = <      Condition for turning on relay (less than or more than)
ad_value = 505    Value at which operation will be preformed
on_gpio_port = 2  Which relay will engage
gpio_duration = 2 Time (in seconds) realy will remain active
gpio_wait = 7     Time (in seconds) before it will activate again
loop_sleep = 1.33 Time (in seconds) before program will read input


all rights reserved.
