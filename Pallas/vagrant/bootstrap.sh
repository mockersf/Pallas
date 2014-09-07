#!/usr/bin/env bash

apt-get update
apt-get install -y unzip
apt-get install -y firefox
apt-get install -y xvfb
apt-get install -y python-pip
apt-get install -y default-jdk
apt-get install -y apache2
Xvfb :10 -ac
rm -rf /var/www
ln -fs /vagrant /var/www

pip install selenium
pip install browsermob-proxy
echo "downloading browsermob proxy"
wget -nv https://s3-us-west-1.amazonaws.com/lightbody-bmp/browsermob-proxy-2.0-beta-9-bin.zip
unzip browsermob-proxy-2.0-beta-9-bin.zip
export DISPLAY=:10