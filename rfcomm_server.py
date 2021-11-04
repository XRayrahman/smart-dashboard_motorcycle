#!/usr/bin/env python3
import bluetooth
# from bluetooth import native_socket
import json
import os
import time
#import main
print("START")
#os.system("print(Waiting for connection)")
os.system("sudo sdptool add sp")
os.system("sudo hciconfig hci0 reset")
os.system("sudo hciconfig hci0 piscan")
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                           service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                           profiles=[bluetooth.SERIAL_PORT_PROFILE],
                           # protocols=[bluetooth.OBEX_UUID]
                           )
print("Waiting for connection on RFCOMM channel", port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)
#
val1 = ""
val2 = ""
val3 = ""
try:
    while True:
        
        data = client_sock.recv(1024)
        #data = b'{ "wifiID": "iPhone",  "password": "lima5555"}\r'
        #data= b'\xef\xef\xef\xef\xef\xef\xef\xef\xef\xef'
        #data = b'{ "tujuan": "pasar turi"}\r'
        try:
            data = data.decode('utf-8')
            if (data[0]=='{') :
                data=json.loads(data)
                
            # if(data['wifiID']) :
            try:
                wifi=data['wifiID']
                if val1 == wifi:
                    pass
                else:
                    print(wifi)
                    val1 = wifi
                #print("wifi id :", wifi)
                #print(tx)
            except:
                wifi=""
                pass

            # if(data['password']) :
            try:
                pas= data['password']
                if val2 == pas:
                    pass
                else:
                    print(pas)
                    val2 = pas
                #print("password :", pas)
            except:
                pas=""
                pass

            # if(data['tujuan']) :
            try:
                tujuan=data['tujuan']
                if val3 == tujuan:
                    pass
                else:
                    print(tujuan)
                    val3 = tujuan
                #print("tujuan :", tujuan)
            except:
                tujuan=""
                pass
            
            tx = {
                "connection" :{                    
                    "wifiID": wifi,
                    "password": pas
                },
                "address" : {
                    "tujuan": tujuan
                }
            }
            if len(data) != 0:
                file = "con-log.json"
                with open(file, 'w') as file_object:  #open the file in write mode
                    json.dump(tx, file_object, indent=4, separators=(", ", " : "))
            else:
                pass
            # print(tx["address"]["tujuan"])
            
            time.sleep(1)
            #print(json.dumps(tx, indent=4, separators=(", ", " = ")))
        except:
            pass
        if not data:
            break
    
except OSError:
    pass
#finally:

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
