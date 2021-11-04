#!/usr/bin/python
import os, sys
import serial
# import time
import json

ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 5)


    
# listen for the input, exit if nothing received in timeout period
while True:
    line = ser.readline()
    data = line.decode('utf-8')
    fldata = format(float(data), ".2f")
    json_data = "tegangan: "+str(fldata)
    # data = json.loads(data)
    
    tegangan_json = {
        "tegangan": fldata
    }
    if len(str(data)) != 0:
        file = "datastore.json"
        with open(file, 'w') as file_object:  #open the file in write mode
            json.dump(tegangan_json, file_object, indent=4)
    else:
        print("Time out! Exit.\n")
        sys.exit()
    # print(format(float(data), ".2f"))
    print(json_data)
   
