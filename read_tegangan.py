#!/usr/bin/python
import os, sys
import serial
# import time
import json

try:
    os.system("sudo chmod 777 /dev/ttyUSB0")
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout=5)
except:
    try:
        os.system("sudo chmod 777 /dev/ttyUSB1")
        ser = serial.Serial('/dev/ttyUSB1',9600, timeout=5)
    except:
        try:
            os.system("sudo chmod 777 /dev/ttyUSB2")
            ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=5)
        except:
            pass


# val1 = ""
# val2 = ""
    
# listen for the input, exit if nothing received in timeout period
while True:
    try:
        line = ser.readline()
        data = line.decode('utf-8')
        if (data[0]=='{' ) :
            data=json.loads(data)
            # print(data)
            # fldata = format(float(data), ".2f")
            # json_data = "tegangan: "+str(fldata)
            # data = json.loads(data)
        try:
            tegangan=data['t']
            kecepatan=data['r']
        except:
            tegangan="0.00"
            kecepatan="0.00"

        data_json = {
            "tegangan": tegangan,
            "kecepatan": kecepatan
        }

        if len(str(data)) != 0:
            file = "database/datastore.json"
            with open(file, 'w') as file_object:  #open the file in write mode
                json.dump(data_json, file_object, indent=4)
            # print(data_json)
        else:
            print("Time out! Exit.\n")
            pass

    except:
        pass
    # print(format(float(data), ".2f"))

   
