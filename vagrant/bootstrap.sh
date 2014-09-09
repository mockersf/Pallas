#!/usr/bin/env bash

#temporary issue between firefox and selenium
wget -nv http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/30.0/linux-i686/en-US/firefox-30.0.tar.bz2
tar jxf firefox-30.0.tar.bz2
mv /usr/lib/firefox /usr/lib/firefox_last
mv firefox /usr/lib/firefox
cp /usr/lib/firefox_last/firefox.sh /usr/lib/firefox/firefox.sh
