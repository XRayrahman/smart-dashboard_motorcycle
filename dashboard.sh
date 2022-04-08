#!/bin/bash

xte 'mousemove 900 50'
source /home/pi/dashboard/bin/activate
cd /home/pi/dashboard/gesits-system
cat /dev/ttyUSB0 &
cat /dev/ttyUSB1 &
cat /dev/ttyUSB2 &
cat /dev/ttyUSB3 &
python main.py
