from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import RiseInTransition,FadeTransition, ScreenManager, Screen
from time import strftime
from math import *
from subprocess import Popen, PIPE, STDOUT
from kivy.clock import Clock
from kivy.graphics import Color, Line, SmoothLine
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
import os
import requests
import joblib
import requests
import json

#Clock.max_iteration = 50
# from kivy.config import Config
# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '480')
# Config.write()

Window.borderless = True
#Window.size=(800,480)
#Window.fullscreen = True
Window.maximize()

class Dashboard(MDApp):
    sw_started= False
    sw_seconds = 0
    val = ""
    tuj = ""
    icon = 'logo.svg'
    #global screen_manager
    screen_manager = ScreenManager()
    jarak_tempuh_total = 0
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "500" 
        self.title="EVOLION"

        
        return MyLayout()

    def on_start(self):

        self.root.ids.screen_manager.switch_to(self.root.ids.splashScreen)
        self.subScreen = Clock.schedule_once(self.changeScreen,9)
        
        self.root.ids.switch.active=True
        self.jarak_sebelumnya = 0

        SOC = 2
        self.SOC = SOC
        self.root.ids.SOC_bar.value = SOC
        SOC_text = str(SOC)+" V"
        # SOC_text = "TEGANGAN : "+str(SOC)+" V"
        self.root.ids.tegangan_value_text.text = SOC_text
        SOC_value = round((SOC/3)*100, 0)
        SOC_value = str(SOC_value)+"%"

        self.sub1 = Clock.schedule_interval(self.update_status,     5) #(program, interval/waktu dijalankan)
        self.sub2 = Clock.schedule_interval(self.update_data,       1)
        self.sub3 = Clock.schedule_interval(self.odometer,          1)
        self.sub4 = Clock.schedule_interval(self.odometer_submit,   5)
        self.asyncRun = Clock.schedule_once(self.asyncProgram,      10)


    def asyncProgram(self,dt):
        Popen("python data_communication.py", shell=True);
        # Popen("python rfcomm_server.py", shell=True);

    def changeScreen(self,dt):
        self.root.ids.screen_manager.transition = RiseInTransition()
        self.root.ids.screen_manager.switch_to(self.root.ids.mainScreen)

    #update data SOC dan kecepatan
    def update_data(self,nap):
        # tegangan = 0.00
        strtegangan = "0.0"
        if self.sw_started:
            self.sw_seconds += nap

        try:
            dt = open('database/tegangan.json')
            data_tegangan = json.load(dt)
            strtegangan = data_tegangan['tegangan']
        except:
            strtegangan = "0.00"

        SOC_text = strtegangan +" V"
        # SOC_text = "TEGANGAN : "+ strtegangan +" V"
        self.root.ids.tegangan_value_text.text = SOC_text
        valtegangan = float(strtegangan)
        if valtegangan >= 71:
            SOC_value = round(80+((valtegangan-71)/0.7),1)
        elif valtegangan <= 60:
            SOC_value = round(0,1)
            # SOC_value = round(30-((60-valtegangan)/2),1)
        else:
            SOC_value = round(80-((70-valtegangan)/0.1125),1)
        # if valtegangan >= 7:
        #     SOC_value = round(20+((valtegangan-7)/2.5),1)
        # elif valtegangan <= 6:
        #     SOC_value = round(10-((6-valtegangan)/0.6),1)
        # else:
        #     SOC_value = round(20-((7-valtegangan)/0.1),1)

        # SOC_value = round((float(strtegangan)/3)*100, 1)
        # self.root.ids.SOC_bar.current_percent = 20
        self.root.ids.SOC_bar.current_percent = SOC_value
        self.SOC_value = str(SOC_value)+"%"

        #kecepatan
        try:    
            dk = open('database/kecepatan.json')
            data_kecepatan = json.load(dk)
            self.kecepatan = data_kecepatan['kecepatan']
        except:
            self.kecepatan = "0.00"

        kecepatan = (float(self.kecepatan)/6)*188.4*0.036
        kecepatan = (format(float(kecepatan), ".0f"))

        #maksimal kecepatan
        if int(kecepatan) >= 121:
            kecepatan = 120

        # print(kecepatan)
        self.root.ids.speed_bar.value = kecepatan
        speeds = str(kecepatan)
        self.root.ids.speed_bar_value.text = speeds
        speed_value = "%s km/h" %(speeds)
        # self.root.ids.speed_value.text = speed_value

        # self.root.ids.progress_relative.current_percent = 20


    def odometer(self,nap):
        # tegangan = 0.00
        #odo = "0.0"
        if self.sw_started:
            self.sw_seconds += nap  
        jarak_tempuh = (float(self.kecepatan)/6)*188.4*0.00001
        self.jarak_tempuh_total_lima = jarak_tempuh + self.jarak_sebelumnya
        self.jarak_sebelumnya = jarak_tempuh

    def odometer_submit(self,nap):
        # tegangan = 0.00
        #odo = "0.0"
        if self.sw_started:
            self.sw_seconds += nap

        try:
            opdata = open('database/odometer.json')
            data = json.load(opdata)
            odo = data['total_km']
        except Exception as e:
            print('odo error :',str(e) )
        
        
        self.jarak_tempuh_total = float(odo)
        #jarak_tempuh = format(float(jarak_tempuh), ".0f")
        self.jarak_tempuh_total = self.jarak_tempuh_total + self.jarak_tempuh_total_lima
        # self.jarak_tempuh_total = self.jarak_tempuh_total + jarak_tempuh
    
        self.total_odo = format(float(self.jarak_tempuh_total), ".3f")
        self.root.ids.odometer.text = format(float(self.total_odo), ".3f")
        # except:
        odometer = {
            "total_km": self.total_odo
        }
        # except:
            # pass
            
        try:
            if len(str(data)) != 0:
                file = "database/odometer.json"
                with open(file, 'w') as file_object: 
                    json.dump(odometer, file_object, indent=4)
                # print(data_json)
            else:
                print("Time out! Exit.\n")
                pass
        except:
            pass
            # pass
        # odo = "0.123"
        
        # try:
        

        

    def update_status(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        #tambah detik = :%S
        #self.root.ids.SOC_value.text = "blok"
        self.root.ids.time.text = strftime('[b]%H:%M  |[/b]')

        fd = open('database/connection.json')
        connectionFile = json.load(fd)
        wifiID = connectionFile['wifi']['id']
        password = connectionFile['wifi']['pass']
        #print (tujuan)

        if len(wifiID) == 0:
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

        fe = open('database/estimation.json')
        estimationFile = json.load(fe)
        tujuanLat = estimationFile['address']['tujuan']['latitude']
        tujuanLng = estimationFile['address']['tujuan']['longitude']


        if len(tujuanLat) == 0:
            pass
        else:
            if self.tuj != tujuanLat:
                try:
                    #fungsi tujuan
                    try:
                        self.root.ids.mapview.remove_widget(self.root.marker)
                    except:
                        pass

                    try:
                        self.root.estimasi(tujuanLat,tujuanLng, self.SOC_value)
                    except Exception as e:
                        print('estimation error :',str(e) )
                        
                    self.root.center_maps()
                    self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini2)
                    self.root.ids.screendget.switch_to(self.root.ids.test2)
                    self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop2)
                    self.root.ids.mode_label.text = "JARAK"
                    self.root.ids.suhu_label.text = "WAKTU"
                    self.root.ids.card_label.text = "REKOMENDASI"
                    self.tuj = tujuanLat
                    print("selesai")
                except Exception as e:
                    print('function error :',str(e) )
            else:
                pass
    


class MyLayout(Screen):

    def __init__(self, *args, **kwargs):
        super(MyLayout,self).__init__(*args,**kwargs)

        this_path = str(os.getcwd())
        path = this_path+"/.key/api-key.txt"
        API_file = open(path,"r")
        print(API_file)
        self.API_key = API_file.read()
        API_file.close()

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
            line = LineMapLayer(self.lat, self.lng, self.OriginLat, self.OriginLng)
            mapview.add_layer(line, mode='scatter')
            mapview.center_on(self.OriginLat, self.OriginLng)
            #marker1 = MapMarkerPopup(lat=lat, lon=lng) 

        except Exception as e:
            print("error center map:", str(e))

        try:
            self.marker_origin = MapMarker(lat=self.OriginLat, lon=self.OriginLng, source="marker-3-24.png")
            self.marker_destination = MapMarker(lat=self.lat, lon=self.lng, source="marker-red.png")
            mapview.add_widget(self.marker_origin)
            mapview.add_widget(self.marker_destination)
            Clock.schedule_once(self.zoom_maps, 12)
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
        try:
            self.commandl = "nmcli dev wifi connect "+name+" password "+password
        # print ("success connection : ",sub.out)
        # print (self.command1)
            scan = os.popen("nmcli device wifi rescan")
            isConnect = os.popen(self.commandl).read()
            # isConnect = True
        except:
            isConnect = "";
        
        if isConnect != "":
            self.popup = MDDialog(title='terhubung dengan internet \n wifi id : '+name,
                        radius=[7, 7, 7, 7],
                        md_bg_color=(25/255,135/255,84/255,1),
                        size_hint=(None, None), size=(400, 400))
            self.popup.open()
        else:
            self.popup = MDDialog(title='tidak dapat terhubung dengan internet',
                        radius=[7, 7, 7, 7],
                        md_bg_color=(244/255,67/255,54/255,1),
                        size_hint=(None, None), size=(400, 400))
            self.popup.open()
        # self.sub(self.commandl)
    
    # function to display avavilabe Wifi networks   
    # def displayAvailableNetworks(self):
    #     self.commandl = "nmcli dev wifi"
    #     self.sub(self.commandl)


    # def sub(self,command):
    #     self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #     (out, err) = self.proc.communicate()
    #     print ("program output : ", out)
    #     print ("error : ",err)
    
    def move_s_mini1(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini1)


    def move_s_mini2(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini2)

    def estimasi(self, destinationLat, destinationLng, SOC_value):
        # lay = MyLayout()
        #path_to_kv_file = "test.kv"
        #gmaps = googlemaps.Client(key=API_key)
        
        scaler = joblib.load('std_rev1.bin')
        model = joblib.load('estimasi_rev1.pkl')

        self.lat = destinationLat
        self.lng = destinationLng
        self.OriginLat = -7.2849060923904085
        self.OriginLng = 112.7961434972626
        # self.lat = -7.277094626336178
        # self.lng = 112.7974416864169
        body = {"locations":[[self.OriginLng,self.OriginLat],[self.lng,self.lat]],"metrics":["distance","duration"],"units":"km"}
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': self.API_key,
            'Content-Type': 'application/json; charset=utf-8'
        }
        post_matrix = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)

        try:
            data_matrix = json.loads(post_matrix.text)
            duration = data_matrix['durations'][0][1]
            TrueDistance = data_matrix['distances'][0][1]
            self.ids.DummyDistance.text = str(TrueDistance) + " km"
            self.ids.DummyTimeEst.text = str(duration) + " s"
        except Exception as e:
            print('INVALID REQUEST DISTANCE :',str(e) )
        
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        get_geocode_origin = requests.get('https://api.openrouteservice.org/geocode/reverse?api_key='+self.API_key+'&point.lon='+str(self.OriginLng)+'&point.lat='+str(self.OriginLat)+'&size=2', headers=headers)
        get_geocode_destination = requests.get('https://api.openrouteservice.org/geocode/reverse?api_key='+self.API_key+'&point.lon='+str(self.lng)+'&point.lat='+str(self.lat)+'&size=2', headers=headers)

        try:
            geocode_origin = json.loads(get_geocode_origin.text)
            geocode_destination = json.loads(get_geocode_destination.text)
            place_name_origin = geocode_origin["features"][0]["properties"]["label"]
            place_name_destination = geocode_destination["features"][0]["properties"]["label"]
            self.ids.lokasi_label.text = "ASAL        :  %s\nTUJUAN   :  %s" %(place_name_origin,place_name_destination)
            # print(call.status_code, call.reason)
            print(place_name_destination)
        except Exception as e:
            print('INVALID REQUEST DISTANCE :',str(e) )

        try:
            SOC_value = self.ids.SOC_bar.current_percent
            print("SOC : ",SOC_value)
            SOC = SOC_value
            # SOC = SOC_value.replace("%","")
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
                print("estimasi pemakaian energi : ",float(x),float(test))
                if (float(SOC) - (3/100)*5 <= float(test)):
                    if x == eco:
                        estimasi_eco = "TIDAK CUKUP"
                    elif x == normal:
                        estimasi_normal = "TIDAK CUKUP"
                    elif x == sport:
                        estimasi_sport = "TIDAK CUKUP"

                elif (float(SOC) - (3/100)*5 > float(test)):
                    if x == eco:
                        estimasi_eco = "CUKUP"
                    elif x == normal:
                        estimasi_normal = "CUKUP"
                    elif x == sport:
                        estimasi_sport = "CUKUP"
            # satu rekomendasi
            self.ids.recommendation.text = str(estimasi_normal)
            self.popup = MDDialog(title='Estimasi berhasil',
                        text= 'ECO : '+estimasi_eco+'\nNORMAL :'+estimasi_normal+'\nSPORT :'+estimasi_sport,
                        radius=[7, 7, 7, 7],
                        md_bg_color=(25/255,135/255,84/255,1),
                        size_hint=(None, None), size=(400, 400))
            self.popup.open()
        except Exception as e:
            print('estimation error ni :',str(e) )
            self.popup = MDDialogMap(title='Estimasi gagal',
                        text= 'pastikan kendaraan terkoneksi dengan internet',
                        radius=[7, 7, 7, 7],
                        md_bg_color=(244/255,67/255,54/255,1),
                        size_hint=(None, None), size=(400, 400))
            self.popup.open()

        # tiga rekomendasi
        # self.ids.recommendation.text = "ECO          :  %s\n\nNORMAL  :  %s\n\nSPORT     :  %s" %(estimasi_eco, estimasi_normal, estimasi_sport)



class MDDialog(MDDialog):
    
    def __init__(self, **kwargs):
        super(MDDialog, self).__init__(**kwargs)
        # call dismiss_popup in 2 seconds
        Clock.schedule_once(self.dismiss_popup, 7)

    def dismiss_popup(self, *args):
        self.dismiss()

class MDDialogMap(MDDialog):
    
    def __init__(self, **kwargs):
        super(MDDialog, self).__init__(**kwargs)
        # call dismiss_popup in 2 seconds
        Clock.schedule_once(self.dismiss_popup, 12)

    def dismiss_popup(self, *args):
        self.dismiss() 
    
 

class LineMapLayer(MapLayer):
    def __init__(self,lat,lng,OriginLat,OriginLng, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)

        this_path = str(os.getcwd())
        path = this_path+"/.key/api-key.txt"
        API_file = open(path,"r")
        print(API_file)
        self.API_key_map = API_file.read()
        API_file.close()
        #self.zoom = 16

        url = "https://api.openrouteservice.org/v2/directions/driving-car?&api_key="+self.API_key_map

        #testing Dummies
        #-7.289612, 112.796190

        start = "&start="+str(OriginLng)+","+str(OriginLat)
        end = "&end="+str(lng)+","+str(lat)

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
        self.zoom = 9
    
        
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
            

class NoValueSpeedMeter(SpeedMeter):

    def value_str(self, n): return ''

_displayed = { 
    0: '0',
    30: u'\u03a0 / 6', 60: u'\u03a0/3', 90: u'\u03a0/2', 120: u'2\u03a0/3',
    150: u'5\u03a0/6',
    180: u'\u03a0', 210: u'7\u03a0/6', 240: u'4\u03a0/3'
    }
    
def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}   

#MyLayout.estimasi.has_been_called = False
# lay = MyLayout()
reset()
Dashboard().run()
os.system("sudo killall python")

##ifi = Popen("python3 testing.py", shell=True);
#stdout = blu.communicate()
#blu_val = blu.stdout.read()
#print(blu_val)
