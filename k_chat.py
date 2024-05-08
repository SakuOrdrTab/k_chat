import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from phi2_api import Phi2_api
from chatgpt35_api import Chatgpt35_api

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.llm = Phi2_api()  # Initialize the Phi-2 API

    def prompt_entered(self, instance):
        # self.ids.output_label.text = instance.text.upper()
        response = self.llm.get_answer(instance.text, raw_answer=False)
        self.ids.output_label.text += response + "\n"
        instance.text = ""

class ChatApp(App):
    def build(self):
        return MainWindow()

if __name__=="__main__":
    print(kivy.__version__)
    ChatApp().run()