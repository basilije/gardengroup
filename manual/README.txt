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

[web]            Changing display web page settings
refresh = 2      Time between auto refresh
button_style = 'style="height:57px;"' 

[default]
input = P3         Default MCP3008 input for plotting
values = 50        How many of the last values to plot
auto_refresh = off Whether to refresh page on loop

[criteria]
ad_in = 3         Choose which ad signal in is compared with ad_value
cmp_sign = <      Choose which relationship to use
ad_value = 505    Value at which operation will be preformed
on_gpio_port = 2  Which relay will engage after the criteria is met
gpio_duration = 2 Time (in seconds) realy will remain active
gpio_wait = 7     Time (in seconds) before it could activate again
loop_sleep = 1.33 Time (in seconds) between reading the input


all rights reserved.
