sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git
cd ~
mkdir gardengroup
cd gardengroup
mkdir logs
mkdir dbs
cd ..
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
sudo apt-get install php php7.3-fpm
sudo nano /etc/nginx/sites-available/default
sudo nano /var/www/html/index.php
sudo systemctl stop nginx
sudo systemctl start nginx
sudo chown -R pi:www-data /home/pi/gardengroup
sudo geany /etc/php/7.3/cli/php.ini {and enable sqlite3)
sudo apt-get install php7.3-sqlite
sudo service nginx restart
sudo unzip phpChart_Lite.zip -d /var/www/html/
sudo apt-get install libqt5qml5 libqt5quick5 libqt5webkit5 qml-module-qtquick2 qml-module-qtquick-controls qml-module-qtquick-dialogs qml-module-qtquick-window2 qml-module-qtquick-layouts
sudo apt --fix-broken install
wget https://download.teamviewer.com/download/linux/teamviewer-host_armhf.deb
sudo dpkg -i teamviewer-host_armhf.deb
wget https://github.com/basilije/gardengroup/blob/master/phpChart_Lite.zip
sudo mkdir /var/www/html/phpChart_Lite
sudo unzip -d /var/www/html/phpChart_Lite phpChart_Lite.zip
