import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.widget import Widget
from kivymd.uix.screen import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.network.urlrequest import UrlRequest
from PIL import Image as pilImage
from PIL import ImageFile
from io import BytesIO
import json
import requests
import time
#Window.fullscreen = True
Window.size = (int(9*50), int(16*50))
Window.borderless = True
ImageFile.LOAD_TRUNCATED_IMAGES=True


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checkApi = Clock.schedule_interval(lambda dt: self.refresh_image(), .5)
    old = None
    movie_id = None
    loading = False
    poster_path = "static/poster.jpg"
    poster_path2 = "static/poster.jpg"
    twilight = "static/theatername.jpg"
    current = "poster1"

    def build(self):
        screen = Screen()
        mainCard = MDCard(elevation=7,size_hint=(None,None),width=(Window.width-10),height=((Window.width-10)*(16/9)),center_x=((Window.width)/2),center_y=((Window.height)/2),md_bg_color=(.1,.1,.1,.7),shadow_softness=4)

        boxContainer = MDBoxLayout(size_hint=(1,1),orientation='vertical')
        imageContainer = MDRelativeLayout(size_hint=(1,1))
        self.posterImage = AsyncImage(on_load=self.animate1,allow_stretch=True,keep_ratio=True,pos_hint={'center_x':.5,'center_y':.5},size_hint=(None,None),width=(Window.width - 16),height=((Window.height - 16)*(27/32)),source=self.poster_path)
        self.posterImage2 = AsyncImage(on_load=self.animate2,allow_stretch=True,keep_ratio=True,pos_hint={'center_x':.5,'center_y':.5},size_hint=(None,None),width=(Window.width-16),height=((Window.height-16)*(27/32)),opacity=1,source=self.poster_path2)
        twilightImage = Image(allow_stretch=True,keep_ratio=True, pos_hint={'x': 0,'top':1},size_hint=(None,5/32),width=(Window.width-10),source=self.twilight)
        posterCard = MDCard(elevation=7,pos_hint={'x':0,'bottom':0},size_hint=(None,(27/32)),width=(Window.width-10),md_bg_color=(1,1,1,1),shadow_softness=2)
        imageContainer.add_widget(self.posterImage)
        imageContainer.add_widget(self.posterImage2)
        posterCard.add_widget(imageContainer)
        boxContainer.add_widget(twilightImage)
        boxContainer.add_widget(posterCard)
        mainCard.add_widget(boxContainer)
        screen.add_widget(mainCard)
        return screen

    def update_image(self, data):
        print("SCHEDULER STOPPED")
        self.loading = True
        self.checkApi.cancel()
        #print(data)
        self.movie_id = data['movie_id']
        if data.get('poster_path'):
            new_path = data.get('poster_path')
            print("Source is " + self.current)
            if self.current == "poster1":
                self.poster_path2 = data['poster_path']
                self.posterImage2.source = self.poster_path2
            else:
                self.poster_path = data['poster_path']
                self.posterImage.source = self.poster_path
            return
        print("SCHEDULER STARTED")
        self.start_scheduler()
        return


    def check_for_image(self, req, result):
        msg = result
        if msg.get('msg',None) and self.loading == False:
            data = msg['msg']
            #print(self.movie_id)
            if data != 'Movie has not changed':
                self.update_image(data)
        return

    def refresh_image(self):
        rsp = UrlRequest(f"http://192.168.86.26:9090/get-current-movie/{self.movie_id}", self.check_for_image)
        return

    def animate1(self, *args):
        #print("HELLO THERE> THE IMAGE1 IS LOADED")
        anim1 = Animation(opacity=0, duration=2)
        anim2 = Animation(opacity=1, duration=2)
        anim2.bind(on_complete=self.start_scheduler)
        anim1.start(self.posterImage2)
        anim2.start(self.posterImage)
        self.current = "poster1"
        self.loading = False
        return

    def animate2(self, *args):
        #print("HELLO THERE> THE IMAGE2 IS LOADED")
        anim1 = Animation(opacity=0, duration=2)
        anim2 = Animation(opacity=1, duration=2)
        anim2.bind(on_complete=self.start_scheduler)
        anim1.start(self.posterImage)
        anim2.start(self.posterImage2)
        self.current = "poster2"
        self.loading = False
        return

    def start_scheduler(self, *args):
        print("SCHEDULER STARTED")
        time.sleep(0.5)
        self.checkApi()
        return

if __name__ == "__main__":
    MyApp().run()
