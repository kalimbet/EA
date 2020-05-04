from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
#from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
import requests

class LoginPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.box_layout1 = BoxLayout(orientation="horizontal", size_hint=[1, .5])
        self.box_layout = BoxLayout(orientation="vertical", size_hint=[None, None], size=[300, 300], spacing=10)

        self.box_layout.add_widget(Image(source="user.png", size_hint=[None, None], size=[300, 300]))

        self.box_layout.add_widget(
            TextInput(text="Email", size_hint=[None, None], size=[300, 50], background_color=[.92, .92, .92, .92],
                      halign="center"))
        self.box_layout.add_widget(
            TextInput(text="Password", size_hint=[None, None], size=[300, 50], background_color=[.92, .92, .92, .92],
                      halign='center', password=1))

        self.box_layout.add_widget(Button(
            text="Login",
            font_size=20,
            on_press=self.login_btn_press,
            background_color=[.13, .13, .13, .13],
            background_normal="",
            size_hint=[None, None],
            size=[300, 50],
            # pos=(1200 / 2 - 300, 400)
        ))

        self.box_layout.add_widget(Button(
            text="Registration",
            font_size=20,
            on_press=self.registration_btn_press,
            background_color=[.13, .13, .13, .13],
            background_normal="",
            size_hint=[None, None],
            size=[300, 50],
            # pos=(1200 / 2 - 300, 400)
        ))

        self.lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        self.box_layout.add_widget(self.lbl)
        self.box_layout1.add_widget(Widget())  # left space
        self.box_layout1.add_widget(self.box_layout)
        self.box_layout1.add_widget(Widget())  # Right space
        self.add_widget(self.box_layout1)

    def regUser(self):
        url = 'http://localhost:3000/api/register-user'
        myobj = '{"username": "John2", "pass": "12345", "role": "User", "description": "test record"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        return str(x.content)

    def logUser(self):
        url = 'http://localhost:3000/api/login'
        myobj = '{"username": "John2", "pass": "12345"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        return str(x.content)

    def login_btn_press(self, instance):
        #instance.text = "Result"
        self.lbl.text = self.logUser()
    def registration_btn_press(self, instance):
        #instance.text = "Result"
        self.lbl.text = self.regUser()