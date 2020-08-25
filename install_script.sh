sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git

cd ~
mkdir gardengroup
cd gardengroup
mkdir logs
mkdir dbs

cd ~
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
sudo python3 setup.py install
sudo pip3 install adafruit-mcp3008

cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008
sudo python setup.py install
sudo python3 setup.py install
sudo raspi-config

sudo apt-get install nginx
sudo apt-get install php php7.3-fpm php7.3-sqlite
sudo geany /etc/php/7.3/cli/php.ini {and enable sqlite3)
sudo sh -c "echo 'server {\r\n	listen 80 default_server;\r\n	listen [::]:80 default_server;\r\n	root /var/www/html;\r\n	index index.php;\r\n	server_name _;\r\n	location / {\r\n		try_files $uri $uri/ =404;\r\n		}\r\n	location ~ \.php$ {\r\n		include snippets/fastcgi-php.conf;\r\n		fastcgi_pass unix:/run/php/php7.3-fpm.sock;\r\n		}\r\n}\r\n' > /etc/nginx/sites-available/default"
sudo service nginx restart

sudo usermod -a -G www-data pi
sudo chgrp -R www-data /home/pi/gardengroup/
sudo chmod -R g+w /home/pi/gardengroup
sudo chgrp -R www-data /home/pi/gardengroup/dbs
sudo chmod -R g+w /home/pi/gardengroup/dbs

cd ~
wget https://phpchart.com/phpChart/download/lswdp/phpChart_Lite.zip
wget https://github.com/basilije/gardengroup/blob/master/phpChart_Lite.zip
sudo mkdir /var/www/html/phpChart_Lite
sudo unzip phpChart_Lite.zip -d /var/www/html/phpChart_Lite/

sudo apt-get install libqt5qml5 libqt5quick5 libqt5webkit5 qml-module-qtquick2 qml-module-qtquick-controls qml-module-qtquick-dialogs qml-module-qtquick-window2 qml-module-qtquick-layouts
sudo apt --fix-broken install
wget https://download.teamviewer.com/download/linux/teamviewer-host_armhf.deb
sudo dpkg -i teamviewer-host_armhf.deb

echo -e '#!/usr/bin/bash\r\n\r\ncd /home/pi/gardengroup/\r\npython3 gardengroup.py\r\n' > /home/pi/startup_script.sh
sudo crontab -e
@reboot sh /home/pi/startup_script.sh
