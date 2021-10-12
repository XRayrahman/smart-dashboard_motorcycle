from logging import root
from kivymd.app import MDApp
from kivy.app import App
#from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem
from kivy.lang import Builder
#from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
#from googlemaps import convert
import requests
#import smtplib
import googlemaps
import pandas as pd
import joblib
#import cefpython3 as cef
import json
import http.client
from datetime import datetime
from time import strftime
import time
from kivy.clock import Clock
import urllib
import subprocess
from subprocess import Popen, PIPE, STDOUT
import asyncio
from kivy_garden.speedmeter import SpeedMeter
from kivy_garden.qrcode import QRCodeWidget
from kivymd_extensions.akivymd import *
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
#import rfcomm_server
#from kivy.garden.cefpython import CEFBrowser

#Window.borderless = True
#Window.fullscreen = True
#Window.maximize()

class MyLayout(Screen):

    def estimasi(self, userinput, SOC_value):
        #as_been_called = False
        lay = MyLayout()
        #path_to_kv_file = "test.kv"
        
        #alamat = pd.read_csv('data.csv')

        
        API_file = open("api-key.txt","r")
        API_key = API_file.read()
        API_file.close()
        #gmaps = googlemaps.Client(key=API_key)
        
        #random_number = StringProperty()
        
        scaler = joblib.load('std_rev1.bin')
        model = joblib.load('estimasi_rev1.pkl')

        #a_file = open("data.json","r")
        #alamat = json.load(a_file)
        #a_file.close()
        #speed = self.ids.name_tujuan.text

        self.origin = (-2.01234699405899,29.377851313693) 
        #destinations = convert.location_list(self.tujuan)
        #destinations = self.ids.name_tujuan.text
        #destinations = alamat['coordinates']
        #print(self.soc)
        #print(self.speed)
        #print(destinations)
        #actual_distance = []

        #conn = http.client.HTTPSConnection("www.googleapis.com")
        #userinput= "pasar turi"
        #userinput = self.ids.tujuan.text
        destinationinput = urllib.parse.quote(userinput)
        print(destinationinput)

        try:
            placeID_Destination_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+destinationinput+"&inputtype=textquery&locationbias=ipbias&key=AIzaSyCFIna2ndU8cxZRJN0FfH9KqvlOSvDzTDw&fields=geometry%2Cplace_id"
        except Exception:
            self.ids.DummytimeEst.text = "Timeout"
            self.ids.DummyDistance.text = "Timeout"
        #conn.request("GET", "/maps/api/place/findplacefromtext/json?input="+destinationinput+"&inputtype=textquery&locationbias=ipbias&key=AIzaSyCFIna2ndU8cxZRJN0FfH9KqvlOSvDzTDw", payload, headers)
        #conn.request("GET", placeID_Destination_URL, payload, headers)
        #res = conn.getresponse()
        #DestinationJSON = json.load(res)
        #DestinationJSON = res.read()
        #print(DestinationJSON)
        #placeID_Destination = DestinationJSON['candidates'][0]['place_id']
        #print(placeID_Destination)
        payload={}
        headers = {}
        
        try:
            response = requests.request("GET", placeID_Destination_URL, headers=headers, data=payload)
            #print(DestinationJSON)
            print(response.text)
            responseJSON = json.loads(response.text)
            geolat_destination = responseJSON['candidates'][0]['geometry']['location']['lat']
            geolng_destination = responseJSON['candidates'][0]['geometry']['location']['lng']
            placeid_destination = responseJSON['candidates'][0]['place_id']
            self.str_geolat_destination = str(geolat_destination)
            self.str_geolng_destination = str(geolng_destination)
            print(placeid_destination)
        except Exception as e:
            print('INVALID REQUEST DESTINATION',str(e))
        #geo_destination = str_geolat_destination+","+str_geolng_destination
        #self.ids.button_estimasi.on_release = self.ids.mapview.center_on(geo_destination)
        #self.ids.mapview.center_on.lat = geolat_destination
        #self.ids.mapview.center_on.lon = geolng_destination
        #print(self.ids.mapview1.lat)
        
        #now = datetime.now()
        #departureTime?
        #try:
        Distancematrix_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=driving&key="+API_key+"&destinations=place_id:"+placeid_destination+"&origins=sukolilo&key=AIzaSyCFIna2ndU8cxZRJN0FfH9KqvlOSvDzTDw"
        #-- Parameter Tambahan --
        #&units=metric&traffic_model=pessimistic
        #------------------------
        payload={}
        headers = {}
        distanceresp = requests.request("GET", Distancematrix_URL, headers=headers, data=payload)
        #distanceresp = gmaps.distance_matrix(origin, placeid_destination, mode='driving') ["rows"][0]["elements"][0]["distance"]["value"]
        #print(DestinationJSON)
        print(distanceresp.text)
        
        try:
            distanceJSON = json.loads(distanceresp.text)
            Tdistance = distanceJSON['rows'][0]['elements'][0]['distance']['value']
            Ddistance = distanceJSON['rows'][0]['elements'][0]['distance']['text']
            DtimeEst = distanceJSON['rows'][0]['elements'][0]['duration']['text']
            lay.ids.DummyDistance.text = Ddistance
            lay.ids.DummyTimeEst.text = DtimeEst
            TrueDistance = Tdistance/1000
            print(TrueDistance)
        except Exception as e:
            print('INVALID REQUEST DISTANCE :',str(e) )

        try:
            #SOC_value = self.ids.SOC_value.text
            print("SOC :",SOC_value)
            SOC = SOC_value
            SOC = SOC_value.replace("%","")
            print(float(SOC))
            eco = 45
            normal = 60
            sport = 70
            speedmode = [eco, normal, sport]
        except Exception as e:
            print('INVALID STORING DATA :',str(e) )
        

        try:
            length = TrueDistance
            for x in speedmode:
                coba = [[float(SOC), float(x), float(length)]]
                data = scaler.transform(coba)
                test = model.predict(data)
                print("estimasi pemakaian energi :",float(x), float(test))
                if (float(SOC) - (3/100)*5 <= float(test)):
                    if x == eco:
                        estimasi_eco = "TIDAK"
                    elif x == normal:
                        estimasi_normal = "TIDAK"
                    elif x == sport:
                        estimasi_sport = "TIDAK"

                elif (float(SOC) - (3/100)*5 > float(test)):
                    if x == eco:
                        estimasi_eco = "CUKUP"
                    elif x == normal:
                        estimasi_normal = "CUKUP"
                    elif x == sport:
                        estimasi_sport = "CUKUP"
        except Exception as e:
            print('estimation error :',str(e) )

        try:
            lay.ids.recommendation.text = "ECO          :  %s\n\nNORMAL  :  %s\n\nSPORT     :  %s" %(estimasi_eco, estimasi_normal, estimasi_sport)
            #popup = Popup(title='Test popup',
            #            content=Label(text='Hello world'),
            #            size_hint=(None, None), size=(400, 400))
            #popup.open()
        except Exception as e:
            print('recommendation error :',str(e) )
        #try:
        #    MyLayout.move_s_mini2(lay)
        #    MyLayout.move_menubar_left2(lay)
        #    MyLayout.move_maps(lay)
        #    self.root.ids.SOC_value.text = "21"
        #    #lay.ids.
        #except Exception as e:
        #    print('changing screen error :',str(e) )


        MyLayout.estimasi.has_been_called = True
        
            #lay.ids.screendget_mini.switch_to(lay.ids.s_mini2)
            #lay.ids.menubar_left.switch_to(lay.ids.menubar_leftTop2)
            #lay.ids.screendget.switch_to(lay.ids.test2)

        #try:
        #    mapview = self.root.ids.mapview
        #    lat = self.root.geolat_destination
        #    lng = self.root.geolng_destination
        #    mapview.center_on(lat, lng)
        #except Exception as e:
        #    print('center map error :',str(e) )

        #self.ids.window2.open()
        #self.ids.estimasi_output.text = bisa
        #home= input("Home address \n")
        #destination = input("point address \n")
        ##url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        
        ##r= requests.get(url + "origins=" + home + "&destinations=" + destination + "&key=" + API_key)
        ##gmaps = googlemaps.Client(key=API_key)
        ##time = r.json()["rows"][0]["elements"][1]["duration"]["text"]
        ##seconds = r.json()["rows"][1]["elements"][1]["duration"]["value"]
        ##print("\n travel time is", time)
        
    #def testibutton(self):

    def move_s_mini2(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini2)
    
    def move_s_mini1(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini1)

    def move_menubar_left2(self):
        
        self.ids.menubar_left.switch_to(self.ids.menubar_leftTop2)

    def move_menubar_left1(self):
        self.ids.menubar_left.switch_to(self.ids.menubar_leftTop1)
        #if self.ids.menubar_left.screen('menubar_leftTop1') :
        #    self.ids.menubar_left.switch_to(self.ids.menubar_leftTop2)
        #else :
        #    self.ids.menubar_left.switch_to(self.ids.menubar_leftTop1)
 
    def move_maps(self):
        #self.ids.screendget.remove_widget(self.ids.test1)
        
        self.ids.screendget.switch_to(self.ids.test2)
    
    def center_maps(self):
        try:
            mapview = self.ids.mapview
            lat = self.geolat_destination
            lng = self.geolng_destination
            mapview.center_on(lat, lng)
        except Exception:
            print("error center map")

        try:
            mapview.add_marker(lat, lng, layer=None)
        except Exception:
            print("error marker map")
        
    def move_speed(self):
        self.ids.screendget.switch_to(self.ids.test1)

    def move_graph(self):
        self.ids.screendget.switch_to(self.ids.test3, direction='left')
    
    def submit(self):
        #print(name)
        self.soc = self.ids.sisaSOC.text
        self.speed = self.ids.kecepatan.text
        self.tujuan = self.ids.tujuan.text

      
    
        
#class AKFloatingWindow(
#    ThemableBehavior, FakeRectangularElevationBehavior, BoxLayout
#):
#    fade_exit = BooleanProperty(True)
#    animation_transition = StringProperty("out_quad")
#    animation_duration = NumericProperty(0.1)
#    _state = "close"  
#    def state(self):
#        return self._state
#
#    def dismiss(self):
#
#        exit_pos = [-self.width, -self.height]
#
#        if self.fade_exit:
#            (
#                Animation(
#                    opacity=0,
#                    t=self.animation_transition,
#                    duration=self.animation_duration,
#                )
#                + Animation(pos=exit_pos, duration=0)
#            ).start(self)
#        else:
#            self.opacity = 0
#            self.pos = exit_pos

        #self._state = "close"  
class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    
    pass

# class Progress(Popup):
    
#     def __init__(self, **kwargs):
#         super(Progress, self).__init__(**kwargs)
#         # call dismiss_popup in 2 seconds
#         Clock.schedule_once(self.dismiss_popup, 2)

#     def dismiss_popup(self, dt):
#         self.dismiss()

class Gesits(MDApp):
    sw_started= False
    sw_seconds = 0
    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        #tambah detik = :%S
        self.root.ids.time.text = strftime('[b]%H[/b]:%M')

    #def ifi_function(self):
    #    MyLayout.estimasi()





    #while Test().run():
    ##print (file["password"])
    # function to connect to a network   
    def connect(self, name, password):
        self.commandl = "nmcli dev wifi connect "+name+" password "+password+""
        # print ("success connection : ",sub.out)
        self.sub(self.commandl)
    
    # function to display avavilabe Wifi networks   
    def displayAvailableNetworks(self):
        self.commandl = "nmcli dev wifi"
        self.sub(self.commandl)


    def sub(self,command):
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (out, err) = self.proc.communicate()
        print ("program output : ", out)
        print ("error : ",err)
        

    # def destination_input(destinationinput):
    #     MyLayout.estimasi(destinationinput)
    def comm_con(self, val):
        lay = MyLayout() 
        val = ""
        tuj = ""
        SOC = 2
        SOC_value = round((SOC/3)*100, 1)
        SOC_value = str(SOC_value)+"%"
        #displayAvailableNetworks()
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
                            MyLayout.estimasi(lay, tujuan, SOC_value)
                            MyLayout.move_s_mini2(lay)
                            MyLayout.move_menubar_left2(lay)
                            MyLayout.move_maps(lay)
                            tuj = tujuan
                        except Exception as e:
                            print('estimation error :',str(e) )
                    else:
                        pass
            else:
                if len(password) == 0:
                    pass
                else:
                    #code disini
                    if val != wifiID:
                        try:
                            self.connect(wifiID, password)
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
            time.sleep(3)

    def build(self):
        #self.theme_cls.accent_color = "Green"
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "BlueGray"
        #self.theme_cls.primary_hue = "800" 
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "500" 

        #text_file = open("hotReloader.kv", "r")
        #KV = text_file.read()
        #return Builder.load_string(KV)w
        #origin_lat = -2.01234699405899
        #origin_lng = 29.377851313693 
        #mapview = self.ids.mapview
        #mapview.center_on(origin_lat, origin_lng)
        return MyLayout()

#     def connect(self, name, password):
#         self.commandl = "nmcli dev wifi connect "+name+" password "+password+""
#     # print ("success connection : ",sub.out)
#         self.sub(self.commandl)
 
# # function to display avavilabe Wifi networks   
#     def displayAvailableNetworks(self):
#         self.commandl = "nmcli dev wifi"
#         self.sub(self.commandl)


#     def sub(self, command):
#         self.proc = self.subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
#         (out, err) = self.proc.communicate()
#         print ("program output : ", out)
#         print ("error : ",err)
#         return out

#     def connection(self):
#         self.val = ""
#         self.tuj = ""
#         self.displayAvailableNetworks()
#         while True:
#             self.f = open('con-log.json')
#             self.file = json.load(self.f)
#             self.tujuan = self.file['address']['tujuan']
#             self.wifiID = self.file['connection']['wifiID']
#             self.password = self.file['connection']['password']
#             #print (tujuan)
#             if len(self.wifiID) == 0:
#                 if len(self.tujuan) == 0:
#                     pass
#                 else:
#                     if self.tuj != self.tujuan:
#                         try:
#                             #fungsi tujuan
#                             print(self.tujuan)
#                             self.tuj = self.tujuan
#                             pass
#                         except:
#                             print("gagal mencari tujuan")
#                     else:
#                         pass
#             else:
#                 if len(self.password) == 0:
#                     pass
#                 else:
#                     #code disini
#                     if self.val != self.wifiID:
#                         try:
#                             self.connect(self.wifiID, self.password)
#                             self.val = self.wifiID
#                             #test = sub.out
#                         except:
#                             print("gagal untuk menyambungkan")
#                             pass
#                     else:
#                         pass
                        #else:
                        #    print ("koneksi sukses")
            # if len(tujuan) == 0:
            #     pass
            # else:
            #     print ("tujuan ada")
            #time.sleep(1)

    def on_start(self):
        
        self.sub1 = Clock.schedule_interval(self.update_time, 0)

        #Clock.schedule_interval(self.connection, 0)
         #capture_output=True)
        #for i in range(20):
        #    self.root.ids.container.add_widget(
        #        OneLineListItem(text=f"Single-line item {i}")
        #    )
        speed = 47
        self.root.ids.rpm.value = speed
        speed_value = "%s km/h" %(str(speed))
        self.root.ids.speed_value.text = speed_value
        print(speed_value)
        
        SOC = 2
        SOC_value = round((SOC/3)*100, 1)
        SOC_value = str(SOC_value)+"%"
        self.root.ids.SOC_value.text = SOC_value
        print(SOC_value)

        Clock.schedule_interval(self.comm_con, 15)

MyLayout.estimasi.has_been_called = False
Gesits().run()
            
    #def bluetooth(self):
    #    try:
    #        while True:
    #            print(rfcomm_server.wifi)
    #            print(rfcomm_server.pas)
    #    except:
    #        pass

        
    ##def update_kv_file(self, text):
    ##    with open(self.path_to_kv_file, "w") as test:
    ##        test.write(text)
    
    ##def __init__(self, **kwargs):
    ##    super(Test, self).__init__(**kwargs)
    ##    self.random_number = str(random.randint(1, 100))
    ##def change_text(self, text):
    ##    self.random_number = str(random.randint(1, 100))
    ##btn1 = ObjectProperty(button1)
    ##btn1.bind(on_press=change_text)
#async def run(cmd):
#    proc = await asyncio.create_subprocess_shell(
#        cmd,
#        stdout=asyncio.subprocess.PIPE,
#        stderr=asyncio.subprocess.PIPE)
#
#    stdout, stderr = await proc.communicate()
#
#    print(f'[{cmd!r} exited with {proc.returncode}]')
#    if stdout:
#        print(f'[stdout]\n{stdout.decode()}')
#    if stderr:
#        print(f'[stderr]\n{stderr.decode()}')
#asyncio.run(run('python3 rfcomm-server.py'))


##blu = Popen("python3 rfcomm_server.py", shell=True);
##ifi = Popen("python3 testing.py", shell=True);
#stdout = blu.communicate()
#blu_val = blu.stdout.read()
#print(blu_val)
#print(arch)
