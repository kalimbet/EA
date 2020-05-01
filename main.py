from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image
import requests

Window.clearcolor = (.13, .13, .13, .13)

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width','1200')
Config.set('graphics', 'height', '860')

error_text = ""


def regUser():
    url = 'http://localhost:3000/api/register-user'
    myobj = '{"username": "John1", "pass": "12345", "role": "User", "description": "test record"}'
    headers = {'Content-type': 'application/json'}
    x = requests.post(url, data=myobj, headers = headers)
    print(x.content)
    return str(x.content)
def logUser():
    url = 'http://localhost:3000/api/login'
    myobj = '{"username": "John", "pass": "12345"}'
    headers = {'Content-type': 'application/json'}
    x = requests.post(url, data=myobj, headers=headers)
    print(x.content)
    return str(x.content)

class EmployeeAdvisorApp(App):

    def build(self):
        anchor_layout = AnchorLayout()

        box_layout = BoxLayout(orientation="vertical", size_hint=[None, None], size=[300, 300], spacing=20, padding=[0,-100])

        box_layout.add_widget(Image(source="User.png", size_hint=[None, None], size=[300, 300]))

        box_layout.add_widget(TextInput(text="Email", size_hint = [None, None], size=[300, 50], background_color=[.92, .92, .92, .92], halign="center"))
        box_layout.add_widget(TextInput(text="Password",size_hint=[None, None], size=[300, 50], background_color=[.92, .92, .92, .92], halign='center', password='1'))

        box_layout.add_widget(Button(
            text="Login",
            font_size=20,
            on_press=self.login_btn_press,
            background_color=[.13, .13, .13, .13],
            background_normal="",
            size_hint = [None, None],
            size=[300, 50],
            #pos=(1200 / 2 - 300, 400)
        ))

        self.lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        box_layout.add_widget(self.lbl)
        anchor_layout.add_widget(box_layout)
        return anchor_layout

    def login_btn_press(self, instance):
        #instance.text = "Result"
        self.lbl.text = logUser()
    def registration_btn_press(self, instance):
        #instance.text = "Result"
        self.lbl.text = regUser()
if __name__ == "__main__":
    EmployeeAdvisorApp().run()