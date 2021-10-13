from logging import root
from kivymd.app import MDApp
from kivy.app import App
#from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
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
from kivy_garden.mapview import MapView, MapMarker 
from kivymd_extensions.akivymd import *
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
Clock.max_iteration = 50
from kivy.base import ExceptionHandler, ExceptionManager

#import rfcomm_server
#from kivy.garden.cefpython import CEFBrowser

#Window.borderless = True
#Window.fullscreen = True
#Window.maximize()

class Progress(Popup):
    
    def __init__(self, **kwargs):
        super(Progress, self).__init__(**kwargs)
        # call dismiss_popup in 2 seconds
        Clock.schedule_once(self.dismiss_popup, 3)

    def dismiss_popup(self, *args):
        self.dismiss()
class MyLayout(Screen):

    #def Popup_open():
        

    def comm_con(self,*args):
        try:
            self.ids.screendget_mini.switch_to(self.ids.s_mini2)
            self.ids.recommendation.text = "test1"
        except Exception as e:
            print("error :", str(e))

    def __init__(self, *args, **kwargs):
        super(MyLayout,self).__init__(*args,**kwargs)
        #try:
            #Clock.schedule_once(self.comm_con)
        #Clock.schedule_interval(self.comm_con, 7)
        #except Exception as e:
        #   print("error :", str(e))
        #Clock.schedule_interval(self.comm_con,15)


    def move_s_mini2(self):
        try:
            self.ids.screendget_mini.switch_to(self.ids.s_mini2)
        except Exception as e:
            print("error :", str(e))

    def move_menubar_left2(self):
        
        self.ids.menubar_left.switch_to(self.ids.menubar_leftTop2)

    def move_menubar_left1(self):
        self.ids.menubar_left.switch_to(self.ids.menubar_leftTop1)
 
    def move_maps(self):
        #self.ids.screendget.remove_widget(self.ids.test1)
        
        self.ids.screendget.switch_to(self.ids.test2)
    
    def center_maps(self):
        try:
            mapview = self.ids.mapview
            lat = self.geolat_destination
            lng = self.geolng_destination
            mapview.center_on(lat, lng)
            #marker1 = MapMarkerPopup(lat=lat, lon=lng) 

        except Exception as e:
            print("error center map:", str(e))

        try:
            self.marker = MapMarker(lat=lat, lon=lng, source="marker-red.png")
            mapview.add_widget(self.marker)
            #mapview.add_marker(lat=lat, lon=lng)
        except Exception as e:
            print("error marker map:", str(e))
        
    def move_speed(self):
        self.ids.screendget.switch_to(self.ids.test1)

    def move_graph(self):
        self.ids.screendget.switch_to(self.ids.test3, direction='left')
    
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
    
    def move_s_mini1(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini1)

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

        self.origin = (-2.01234699405899,29.377851313693) 
        #destinationinput = urllib.parse.quote(userinput)
        #print(destinationinput)
        placeid_destination = userinput
        
        
        
        try:
            placeID_Destination_URL = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeid_destination+"&key=AIzaSyCFIna2ndU8cxZRJN0FfH9KqvlOSvDzTDw&fields=geometry"
        except Exception as e:
            print('INVALID URL',str(e))
        payload={}
        headers = {}
        try:
            response = requests.request("GET", placeID_Destination_URL, headers=headers, data=payload)
            #print(DestinationJSON)
            print(response.text)
            responseJSON = json.loads(response.text)
            self.geolat_destination = responseJSON['result']['geometry']['location']['lat']
            self.geolng_destination = responseJSON['result']['geometry']['location']['lng']
            self.str_geolat_destination = str(self.geolat_destination)
            self.str_geolng_destination = str(self.geolng_destination)
            print(placeid_destination)
        except Exception as e:
            print('INVALID REQUEST DESTINATION',str(e))

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
            self.ids.DummyDistance.text = Ddistance
            self.ids.DummyTimeEst.text = DtimeEst
            TrueDistance = Tdistance/1000
            print(TrueDistance)
        except Exception as e:
            print('INVALID REQUEST DISTANCE :',str(e) )

        try:
            SOC_value = self.ids.SOC_value.text
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
            print('estimation error ni :',str(e) )

        #try:
        self.ids.recommendation.text = "ECO          :  %s\n\nNORMAL  :  %s\n\nSPORT     :  %s" %(estimasi_eco, estimasi_normal, estimasi_sport)

        try:
            self.popup = MDDialog(title='Tersambung',
                        radius=[20, 7, 20, 7],
                        md_bg_color=(244/255,67/255,54/255,1),
                        size_hint=(None, None), size=(400, 400))
            self.popup.open()
        except Exception as e:
            print('recommendation error :',str(e) )
    
    
    
       
class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    
    pass

# class MyHandler(ExceptionHandler):
#     def handle_exception(self, inst):
#         if isinstance(inst, ValueError):
#             Logger.exception('ValueError caught by MyHandler')
#             return ExceptionManager.PASS
#         return ExceptionManager.RAISE

# ExceptionManager.add_handler(MyHandler())

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
    val = ""
    tuj = ""
    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        #tambah detik = :%S
        #self.root.ids.SOC_value.text = "blok"
        self.root.ids.time.text = strftime('[b]%H[/b]:%M')
        #self.root.ids.recommendation.text = "test1"
        SOC = 2
        SOC_value = round((SOC/3)*100, 1)
        SOC_value = str(SOC_value)+"%"
        #displayAvailableNetworks()
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
                if self.tuj != tujuan:
                    try:
                        #fungsi tujuan
                        try:
                            self.root.ids.mapview.remove_widget(self.root.marker)
                        except Exception as e:
                            print('marker error :',str(e) )
                        try:
                            self.root.estimasi(tujuan, SOC_value)
                        except Exception as e:
                            print('estimation error :',str(e) )
                            
                        self.root.center_maps()
                        self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini2)
                        self.root.ids.screendget.switch_to(self.root.ids.test2)
                        self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop2)
                        self.tuj = tujuan
                        print("selesai")
                    except Exception as e:
                        print('function error :',str(e) )
                else:
                    pass
        else:
            if len(password) == 0:
                pass
            else:
                #code disini
                if self.val != wifiID:
                    try:
                        self.root.connect(wifiID, password)
                        self.val = wifiID
                        #test = sub.out
                    except:
                        print("gagal untuk menyambungkan")
                        pass
                else:
                    pass
                    #else:
                    #    print ("koneksi sukses")
    

    def build(self):
        #self.theme_cls.accent_color = "Green"
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "BlueGray"
        #self.theme_cls.primary_hue = "800" 
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "500" 
        return MyLayout()

    def on_start(self):
        
        self.sub1 = Clock.schedule_interval(self.update_time, 5)

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
        print(Clock.max_iteration)
        

#MyLayout.estimasi.has_been_called = False
lay = MyLayout()
blu = Popen("python3 rfcomm_server.py", shell=True);
Gesits().run()


##ifi = Popen("python3 testing.py", shell=True);
#stdout = blu.communicate()
#blu_val = blu.stdout.read()
#print(blu_val)
#print(arch)
