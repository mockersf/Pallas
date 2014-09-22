#!/usr/bin/env bash

Xvfb :10 -ac &
pid=$!

export DISPLAY=:10
py.test --cov-report term-missing --cov /Pallas/Pallas /Pallas/Pallas/tests
sudo -E python /Pallas/Pallas/pallas.py --log-level DEBUG --proxy-path /home/vagrant/browsermob-proxy-2.0-beta-9/bin/ --target "http://localhost:7337/"

kill $pid
