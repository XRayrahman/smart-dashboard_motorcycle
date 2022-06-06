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
def store_data_json(file, json_structure):
    with open(file, 'w') as file_object:  
        json.dump(json_structure, file_object, indent=4)

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

                    path_tegangan = "database/tegangan.json"
                    store_data_json(path_tegangan, data_json_tegangan)
                    # tegangan_sebelumnya = tegangan
                except Exception as e:
                    print('tegangan error :',str(e) )
                    # tegangan = "0.00"

                try:
                    kecepatan=data['r']
                
                    data_json_kecepatan = {
                        "kecepatan": kecepatan
                    }
                        
                    path_kecepatan = "database/kecepatan.json"
                    store_data_json(path_kecepatan, data_json_kecepatan)
                    # kecepatan_sebelumnya = kecepatan
                except Exception as e:
                    # kecepatan = "0.00"
                    print("kecepatan error : "+str(e))

                try:
                    turn_left= data['turn'][0]
                    turn_right= data['turn'][1]

                    data_json_turn = {
                        "turn_signal":{
                            "right":turn_left,
                            "left":turn_right
                        }
                    }
                        
                    path_turn = "database/vehicle_info.json"
                    store_data_json(path_turn, data_json_turn)
                except:
                    turn_left=False;
                    turn_right=False;

                

                try:
                    statusEstimation = data['isRun']
                    if statusEstimation == True:

                        ### koneksi
                        try:
                            bluetooth_wifi_id=data['wifi_id']
                            bluetooth_wifi_pass=data['wifi_pass']
                            restart_wifi=data['restart']
                            # isConnected = True
                        except:
                            print('wifi not valid')
                            bluetooth_wifi_id=""
                            bluetooth_wifi_pass=""
                            restart_wifi=False

                            
                        data_json_connection = {
                            "wifi":{
                                "id":bluetooth_wifi_id,
                                "pass":bluetooth_wifi_pass
                            },
                            "restart":restart_wifi
                        }
                        
                        path_connection = "database/connection.json"
                        store_data_json(path_connection, data_json_connection)

                        # print(bluetooth_wifi_id)

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
                        
                        path_estimation = "database/estimation.json"
                        store_data_json(path_estimation, data_json_estimation)
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
   
