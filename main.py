import kivy
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty

from kivy.app import App
from kivy.core.window import Window
import requests
import socket
from kivy.clock import Clock
Window.size = (int(9 *50), int(16 *50))
from PIL import Image
from io import BytesIO
from kivymd.app import MDApp

class MainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(lambda dt: self.refresh_image(), 0.5)
    old = None
    poster_path = StringProperty("static/poster.jpg")
    twilight = StringProperty("static/theatername.jpg")

    #def __init__(self):
    #    Clock.schedule_interval(self.refresh_image(), 0.5)
    def build(self):
        kv = Builder.load_file('MyApp.kv')
        return kv
    def refresh_image(self):
        img = BytesIO(requests.get("http://127.0.0.1:8000/get-current-movie").content)
        img1 = Image.open(img)
        if img1 != self.old:
            self.old = img1
            print("Image changed")
            img1 = Image.open(img)
            img1.save('static/poster.jpg')
            self.ids.poster_image.reload()
        return


class MyApp(MDApp):
    pass

if __name__ == '__main__':
    MyApp().run()