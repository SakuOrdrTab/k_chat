import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from phi2_api import Phi2_api

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.prompt_textinput = TextInput(size_hint_y=0.15,
                                          font_size=15,
                                          multiline=False)
        self.output_label = Label(text="This will have text",
                       font_size=15)
        self.prompt_textinput.bind(on_text_validate=self.on_prompt_textinput_enter)
        self.add_widget(self.prompt_textinput)
        self.add_widget(self.output_label)

    def on_prompt_textinput_enter(self, instance):
        self.output_label.text = instance.text.upper()

class ChatApp(App):
    def build(self):
        return MainWindow()


if __name__=="__main__":
    print(kivy.__version__)
    phi2 = Phi2_api()
    ChatApp().run()