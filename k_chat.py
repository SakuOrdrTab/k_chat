import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from src.phi2_api import Phi2_api

# Assuming you will use this later
# from phi2_api import Phi2_api

class MainWindow(BoxLayout):
    def prompt_entered(self, instance):
        self.ids.output_label.text = instance.text.upper()

class ChatApp(App):
    def build(self):
        return MainWindow()

if __name__=="__main__":
    print(kivy.__version__)
    phi2 = Phi2_api()  # Assuming this is for future use
    ChatApp().run()