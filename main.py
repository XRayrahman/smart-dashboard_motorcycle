from logging import root
from kivymd.app import MDApp
import os
# os.environ["KIVY_TEXT"] = "pil"
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
from kivy.uix.screenmanager import RiseInTransition,FadeTransition, ScreenManager, Screen
#from googlemaps import convert
import requests
#import smtplib
import googlemaps
import pandas as pd
import numpy as np
import joblib
#import cefpython3 as cef
import requests
import json
import http.client
from datetime import datetime
from time import strftime
from math import *
import time
import urllib
import subprocess
from subprocess import Popen, PIPE, STDOUT
#import asyncio
from kivy.clock import Clock
from kivy.graphics import Color, Line, SmoothLine, MatrixInstruction
from kivy.graphics.context_instructions import Translate, Scale
from kivy_garden.speedmeter import SpeedMeter
from kivy_garden.qrcode import QRCodeWidget
from kivy_garden.mapview.utils import clamp
from kivy_garden.mapview import MapView, MapMarker , MapLayer
from kivy_garden.mapview.constants import (
    CACHE_DIR,
    MAX_LATITUDE,
    MAX_LONGITUDE,
    MIN_LATITUDE,
    MIN_LONGITUDE,
)
from kivymd_extensions.akivymd import *
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
#Clock.max_iteration = 50
from kivy.base import ExceptionHandler, ExceptionManager
# from kivy.config import Config
# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '480')
# Config.write()
#import rfcomm_server
#from kivy.garden.cefpython import CEFBrowser

#Window.borderless = True
# Window.size=(800,480)
Window.fullscreen = True
# Window.maximize()

class Gesits(MDApp):
    sw_started= False
    sw_seconds = 0
    val = ""
    tuj = ""
    icon = 'logo.svg'
    global screen_manager
    screen_manager = ScreenManager()

    def build(self):
        #self.theme_cls.accent_color = "Green"
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "BlueGray"
        #self.theme_cls.primary_hue = "800" 
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "500" 
        self.title="MOLI-NAV"

        
        return MyLayout()

    def on_start(self):

        self.root.ids.screen_manager.switch_to(self.root.ids.splashScreen)
        self.subScreen = Clock.schedule_once(self.changeScreen,12)
        
        # self.root.ids.progress.value = 100;
        speed = 47
        self.root.ids.speed_bar.value = speed
        speeds = str(speed)
        self.root.ids.speed_bar_value.text = speeds
        speed_value = "%s km/h" %(str(speed))
        self.root.ids.speed_value.text = speed_value
        print(speed_value)
        #baca tegangan
        # with open('file.txt')

        SOC = 2
        self.SOC = SOC
        self.root.ids.SOC_bar.value = SOC
        SOC_text = "TEGANGAN : "+str(SOC)+" V"
        self.root.ids.tegangan_value_text.text = SOC_text
        SOC_value = round((SOC/3)*100, 1)
        SOC_value = str(SOC_value)+"%"
        self.root.ids.SOC_value.text = SOC_value
        self.root.ids.SOC_bar_value.text = SOC_value
        print(SOC_value)
        print(Clock.max_iteration)
        self.sub1 = Clock.schedule_interval(self.update_time, 5)
        self.sub2 = Clock.schedule_interval(self.update_data, 1)

    def changeScreen(self,dt):
        self.root.ids.screen_manager.transition = RiseInTransition()
        self.root.ids.screen_manager.switch_to(self.root.ids.mainScreen)

    #update data, untuk sekarang hanya SOC
    def update_data(self,nap):
        # tegangan = 0.00
        if self.sw_started:
            self.sw_seconds += nap

        try :
            rt = open('datastore.json')
            data = json.load(rt)
            tegangan = data['tegangan']
            kecepatan = data['kecepatan']
        except:
            pass
        # if tegangan == 0.00:
        #     pass
        # else:
        # self.tegangan = tegangan
        SOC_text = "TEGANGAN : "+str(tegangan)+" V"
        self.root.ids.tegangan_value_text.text = SOC_text
        valtegangan = float(tegangan)
        if valtegangan >= 71:
            SOC_value = round(90+((valtegangan-71)*10),1)
        elif valtegangan <= 63:
            SOC_value = round(30-((63-valtegangan)*.476),1)
        else:
            SOC_value = round(90-((71-valtegangan)*.11428),1)

        # SOC_value = round((float(tegangan)/3)*100, 1)
        self.root.ids.SOC_bar.value = SOC_value
        self.SOC_value = str(SOC_value)+"%"
        self.root.ids.SOC_value.text = self.SOC_value
        self.root.ids.SOC_bar_value.text = self.SOC_value

        #kecepatan
        self.root.ids.speed_bar.value = float(kecepatan)
        speeds = str(kecepatan)
        self.root.ids.speed_bar_value.text = speeds
        speed_value = "%s km/h" %(speeds)
        self.root.ids.speed_value.text = speed_value
        

    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        #tambah detik = :%S
        #self.root.ids.SOC_value.text = "blok"
        self.root.ids.time.text = strftime('[b]%H[/b]:%M')
        #self.root.ids.recommendation.text = "test1"

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
                            self.root.estimasi(tujuan, self.SOC_value)
                        except Exception as e:
                            print('estimation error :',str(e) )
                            
                        self.root.center_maps()
                        self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini2)
                        self.root.ids.screendget.switch_to(self.root.ids.test2)
                        self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop2)
                        self.root.ids.mode_label.text = "JARAK"
                        self.root.ids.suhu_label.text = "WAKTU"
                        self.root.ids.card_label.text = "REKOMENDASI"
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
            self.lat = self.geolat_destination
            self.lng = self.geolng_destination
            line = LineMapLayer(self.lat, self.lng, self.OriginLat, self.OriginLng)
            mapview.add_layer(line, mode='scatter')
            mapview.center_on(self.OriginLat, self.OriginLng)
            #marker1 = MapMarkerPopup(lat=lat, lon=lng) 

        except Exception as e:
            print("error center map:", str(e))

        try:
            self.marker_origin = MapMarker(lat=self.OriginLat, lon=self.OriginLng, source="marker-3.png")
            self.marker_destination = MapMarker(lat=self.lat, lon=self.lng, source="marker-red.png")
            mapview.add_widget(self.marker_origin)
            mapview.add_widget(self.marker_destination)
            Clock.schedule_once(self.zoom_maps, 10)
            #mapview.add_marker(lat=lat, lon=lng)
        except Exception as e:
            print("error marker map:", str(e))
    
    def zoom_maps(self, *args):
        mapview = self.ids.mapview
        mapview.zoom = 15
        
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
        lay = MyLayout()
        #path_to_kv_file = "test.kv"
        this_path = str(os.getcwd())
        path = this_path+"/.key/api-key.txt"
        API_file = open(path,"r")
        print(API_file)
        API_key = API_file.read()
        API_file.close()
        #gmaps = googlemaps.Client(key=API_key)
        
        scaler = joblib.load('std_rev1.bin')
        model = joblib.load('estimasi_rev1.pkl')

        self.origin = (-7.289980, 112.793715) 
        self.OriginLat = -7.289980
        self.OriginLng = 112.793715
        #destinationinput = urllib.parse.quote(userinput)
        #print(destinationinput)
        placeid_destination = userinput
        
        try:
            placeID_Destination_URL = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeid_destination+"&key=AIzaSyBxidFA-DVnYjtl9DSNnaVJ3EaOHdY7i50&fields=geometry"
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

        Distancematrix_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=driving&key="+API_key+"&destinations=place_id:"+placeid_destination+"&origins=sukolilo"
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
            Tdestination = distanceJSON['destination_addresses'][0]
            Tdestination = Tdestination.split(",")
            Tdestination = Tdestination[0:1]
            Tdestination = ','.join(Tdestination)
            Torigin = distanceJSON['origin_addresses'][0]
            Torigin = Torigin.split(",")
            Torigin = Torigin[0:2]
            Torigin = ','.join(Torigin)
            self.ids.lokasi_label.text = "ASAL        :  %s\nTUJUAN   :  %s" %(Torigin,Tdestination)
            # self.ids.label_bottom_ori.text = Torigin
            # self.ids.right_icon.icon = "arrow-right"
            #arrow-right-thin-circle-outline
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
                        estimasi_normal = "TIDAK\nCUKUP"
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

        # tiga rekomendasi
        # self.ids.recommendation.text = "ECO          :  %s\n\nNORMAL  :  %s\n\nSPORT     :  %s" %(estimasi_eco, estimasi_normal, estimasi_sport)

        # satu rekomendasi
        self.ids.recommendation.text = estimasi_normal

        try:
            self.popup = MDDialog(title='Tersambung',
                        radius=[7, 7, 7, 7],
                        md_bg_color=(244/255,67/255,54/255,1),
                        size_hint=(None, None), size=(400, 400))
            self.popup.open()
        except Exception as e:
            print('recommendation error :',str(e) )



class MDDialog(MDDialog):
    
    def __init__(self, **kwargs):
        super(MDDialog, self).__init__(**kwargs)
        # call dismiss_popup in 2 seconds
        Clock.schedule_once(self.dismiss_popup, 7)

    def dismiss_popup(self, *args):
        self.dismiss()
        
    
 

class LineMapLayer(MapLayer):
    def __init__(self,lat,lng,OriginLat,OriginLng, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        #self.zoom = 16

        url = "https://api.openrouteservice.org/v2/directions/driving-car?&api_key=5b3ce3597851110001cf6248fee30172e1284561af50061b93def79c"

        #testing Dummies
        #-7.289612, 112.796190
        #start = "&start=112.796190,-7.289612" 
        start = "&start="+str(OriginLng)+","+str(OriginLat)
        end = "&end="+str(lng)+","+str(lat)
        #end = "&end=8.687872,49.420318"

        #Real World Appliaction
        # start = "&start=" + str(startLat) + "," + str(startLng)
        # end = "&end=" + str(endLat) + "," + str(endLng)

        final = url + start + end
        payload={}
        headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }

        response = requests.request("GET", final, headers=headers, data=payload)
        hasil = json.loads(response.text)
        polyCoordinates = hasil['features'][0]['geometry']['coordinates']


        self._coordinates = [[polyCoordinates[0][1], polyCoordinates[0][0]]]
        for i in range(1, len(polyCoordinates)):
            # self.points =polyCoordinates[i-1], polyCoordinates[i]
            self.points =(polyCoordinates[i][1], polyCoordinates[i][0])
            self._coordinates.append(self.points)
        self._line_points = None
        self._line_points_offset = (0, 0)
        self.zoom = 10
    
        
        # geo_dover   = [51.126251, 1.327067]
        # geo_calais  = [50.959086, 1.827652]
        
        # # NOTE: Points must be valid as they're no longer clamped
        # self.coordinates = [geo_dover, geo_calais]
        # for i in range(25000-2):
        #     self.coordinates.append(self.gen_point())
    @property
    def coordinates(self):
        return self._coordinates
    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates
        self.invalidate_line_points()
        self.clear_and_redraw()

    @property
    def line_points(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points

    @property
    def line_points_offset(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset
    @property
    def line_points_offset(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset
    def calc_line_points(self):
        # Offset all points by the coordinates of the first point, to keep coordinates closer to zero.
        # (and therefore avoid some float precision issues when drawing lines)
        self._line_points_offset = (self.get_x(self.coordinates[0][1]), self.get_y(self.coordinates[0][0]))
        # Since lat is not a linear transform we must compute manually
        self._line_points = [(self.get_x(lon) - self._line_points_offset[0], self.get_y(lat) - self._line_points_offset[1]) for lat, lon in self.coordinates]



    def invalidate_line_points(self):
        self._line_points = None
        self._line_points_offset = (0, 0)
        
    def get_x(self, lon):
        """Get the x position on the map using this map source's projection
        (0, 0) is located at the top left.
        """
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) *self.ms /360.
 
    def get_y(self, lat):
        """Get the y position on the map using this map source's projection
        (0, 0) is located at the top left.
        """
        lat = radians(clamp(-lat, MIN_LATITUDE, MAX_LATITUDE))
        return ((1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi )) *self.ms /2.0
    
    def reposition(self):
        mapview = self.parent

        # Must redraw when the zoom changes
        # as the scatter transform resets for the new tiles
        if (self.zoom != mapview.zoom):
            map_source = mapview.map_source
            self.ms = pow(2.0, mapview.zoom) * map_source.dp_tile_size
            self.invalidate_line_points()
            self.clear_and_redraw()

    def clear_and_redraw(self, *args):
        with self.canvas:
            # Clear old line
            self.canvas.clear()

        # FIXME: Why is 0.05 a good value here? Why does 0 leave us with weird offsets?
        Clock.schedule_once(self._draw_line, 0.05)   
    def _draw_line(self, *args):
        mapview = self.parent
        self.zoom = 12
        self.zoom = mapview.zoom
       
        # When zooming we must undo the current scatter transform
        # or the animation distorts it
        scatter = mapview._scatter
        sx,sy,ss = scatter.x, scatter.y, scatter.scale
        vx,vy,vs = mapview.viewport_pos[0], mapview.viewport_pos[1], mapview.scale
        
        # Account for map source tile size and mapview zoom
        
        #: Since lat is not a linear transform we must compute manually 
        line_points = []
        for lat,lon in self.coordinates:
            line_points.extend((self.get_x(lon),self.get_y(lat)))
            #line_points.extend(mapview.get_window_xy_from(lat,lon,mapview.zoom))
        
         
        with self.canvas:
            # Clear old line
            self.canvas.clear()
            
            # Undo the scatter animation transform
            Translate(*mapview.pos)
            Scale(1/ss,1/ss,1)
            Translate(-sx,-sy)
            
            # Apply the get window xy from transforms
            Scale(vs,vs,1)
            Translate(-vx,-vy)
               
            # Apply the what we can factor out of the mapsource long, lat to x, y conversion
            Translate(self.ms / 2, 0)

            # Translate by the offset of the line points (this keeps the points closer to the origin)
            Translate(*self.line_points_offset)

             
            # Draw new
            Color(31/255,146/255,161/255,1 )
            Line(points=self.line_points, width=6/2, joint="round")#4/ms)#6., joint="round",joint_precision=100)
            Color(146/255,218/255,241/255,1)
            Line(points=self.line_points, width=4 / 2)
            

       
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
        

#MyLayout.estimasi.has_been_called = False
lay = MyLayout()
back1 = Popen("python read_tegangan.py", shell=True);
blu = Popen("python rfcomm_server.py", shell=True);
Gesits().run()
os.system("killall python")
os.system("exit")

##ifi = Popen("python3 testing.py", shell=True);
#stdout = blu.communicate()
#blu_val = blu.stdout.read()
#print(blu_val)
#print(arch)
