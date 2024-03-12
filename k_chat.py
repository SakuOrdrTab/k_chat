import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from src.phi2_api import Phi2_api

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.phi2_api = Phi2_api()  # Initialize the Phi-2 API

    def prompt_entered(self, instance):
        # self.ids.output_label.text = instance.text.upper()
        response = self.phi2_api.get_answer(instance.text)
        self.ids.output_label.text += response

class ChatApp(App):
    def build(self):
        return MainWindow()

if __name__=="__main__":
    print(kivy.__version__)
    ChatApp().run()