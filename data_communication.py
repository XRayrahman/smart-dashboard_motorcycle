from curses import baudrate
import os, sys
import serial
# import time
import json
# import json_stream
import fnmatch

# from main import reset

def arduino_ports(preferred_list=['*']):
    '''try to auto-detect serial ports on posix based OS'''
    import glob

    glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    ret = []

    # try preferred ones first
    for d in glist:
        for preferred in preferred_list:
            if fnmatch.fnmatch(d, preferred):
                #ret.append(SerialPort(d))
                ret.append(d)
    if len(ret) > 0:
        return ret
    # now the rest
    for d in glist:
        #ret.append(SerialPort(d))
        ret.append(d)
    return ret
    
# listen for the input, exit if nothing received in timeout period
def store_data_arduino(ser):
    while True:
        try:
            line = ser.readline()
            # print(line)
            data_dec = line.decode('utf-8')
            # print(data_dec)
            # print("----")
            # if (data[0]=='{' ) :
            data=json.loads(data_dec)
            
            # print(data)
            # print(data_dec)
            if len(str(data)) != 0:
                # print(data)
                try:
                    tegangan=data['t']
                    data_json_tegangan = {
                        "tegangan": tegangan
                    }

                    file = "database/tegangan.json"
                    with open(file, 'w') as file_object:  
                        json.dump(data_json_tegangan, file_object, indent=4)
                    # tegangan_sebelumnya = tegangan
                except Exception as e:
                    print('tegangan error :',str(e) )
                    # tegangan = "0.00"

                try:
                    kecepatan=data['r']
                
                    data_json_kecepatan = {
                        "kecepatan": kecepatan
                    }
                        
                    file = "database/kecepatan.json"
                    with open(file, 'w') as file_object:  
                        json.dump(data_json_kecepatan, file_object, indent=4)
                    # kecepatan_sebelumnya = kecepatan
                except Exception as e:
                    # kecepatan = "0.00"
                    print("kecepatan error : "+str(e))

                try:
                    statusEstimation = data['isRun']
                    if statusEstimation == True:

                        ### koneksi
                        try:
                            bluetooth_wifi_id=data['wifi_id']
                            # isConnected = True
                        except:
                            print('wifi id not valid')
                            bluetooth_wifi_id=""

                        try:
                            bluetooth_wifi_pass=data['wifi_pass']
                        except:
                            print('wifi pass not valid')
                            bluetooth_wifi_pass=""

                        # print(bluetooth_wifi_id)
                        data_json_connection = {
                            "wifi":{
                                "id":bluetooth_wifi_id,
                                "pass":bluetooth_wifi_pass
                            }
                        }
                        
                        file = "database/connection.json"
                        with open(file, 'w') as file_object:  
                            json.dump(data_json_connection, file_object, indent=4)

                        ### estimasi   
                        try:
                            ori_latitude=data['o_lat']
                            ori_longitude=data['o_lng']
                            # isConnected = True
                        except:
                            # print('origin address not valid')
                            ori_latitude=""
                            ori_longitude=""

                        try:
                            dest_latitude=data['d_lat']
                            dest_longitude=data['d_lng']
                        except:
                            # print('destination address not valid')
                            dest_latitude=""
                            dest_longitude=""

                        data_json_estimation = {
                            "address":{
                                "asal":{
                                    "latitude":ori_latitude,
                                    "longitude":ori_longitude
                                },
                                "tujuan":{
                                    "latitude":dest_latitude,
                                    "longitude":dest_longitude
                                }
                            }
                        }
                        
                        file = "database/estimation.json"
                        with open(file, 'w') as file_object:  
                            json.dump(data_json_estimation, file_object, indent=4)
                except:
                    statusEstimation = False
                    
                # print(statusEstimation)


                    # print(data_json)
                    # file = "database/datastore.json"
                    # with open(file, 'w') as file_object:  #open the file in write mode
                    #     json.dump(data_json, file_object, indent=4)
            else:
                print("Time out! Exit.\n")
                pass

            # else:
            #     pass

        # except Exception as e:
        #     print('data error :',str(e) )
        except:
            pass

def main():
    # reset()
    baudrate = 115200
    available_ports = arduino_ports()
    port = serial.Serial(available_ports[0], baudrate, timeout=3)
    print(available_ports[0])
    store_data_arduino(port)
    # print(format(float(data), ".2f"))
if __name__ == '__main__':
    main()
   
