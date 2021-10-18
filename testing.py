import json
import time
import os
import subprocess
from subprocess import PIPE, run



#while Test().run():
##print (file["password"])
# function to connect to a network   
def connect(name, password):
    commandl = "nmcli dev wifi connect "+name+" password "+password+""
    # print ("success connection : ",sub.out)
    sub(commandl)
 
# function to display avavilabe Wifi networks   
def displayAvailableNetworks():
    commandl = "nmcli dev wifi"
    sub(commandl)


def sub(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print ("program output : ", out)
    print ("error : ",err)
    return out
#ChIJd9BCGUf51y0RR2D7jmxJkJg
# def destination_input(destinationinput):
#     MyLayout.estimasi(destinationinput)
val = ""
tuj = ""
displayAvailableNetworks()
while True:
    f = open('con-log.json')
    file = json.load(f)
    tujuan = file['address']['tujuan']
    wifiID = file['connection']['wifiID']
    password = file['connection']['password']
    #print (tujuan)
    if len(wifiID) == 0:
        if len(tujuan) == 0:
            pass
        else:
            if tuj != tujuan:
                try:
                    #fungsi tujuan
                    print(tujuan)
                    tuj = tujuan
                    pass
                except:
                    print("gagal mencari tujuan")
            else:
                pass
    else:
        if len(password) == 0:
            pass
        else:
            #code disini
            if val != wifiID:
                try:
                    connect(wifiID, password)
                    val = wifiID
                    #test = sub.out
                except:
                    print("gagal untuk menyambungkan")
                    pass
            else:
                pass
                #else:
                #    print ("koneksi sukses")
    # if len(tujuan) == 0:
    #     pass
    # else:
    #     print ("tujuan ada")
    time.sleep(1)
    