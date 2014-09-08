#!/usr/bin/env bash

Xvfb :10 -ac &
pid=$!

export DISPLAY=:10
sudo -E python /Pallas/Main/pallas.py --log-level DEBUG --proxy-path /home/vagrant/browsermob-proxy-2.0-beta-9/bin/ --target "http://localhost:7337/"

kill $pid
