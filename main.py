import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
#from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import settings as settings
import requests
import json
import os

kivy.require("1.10.1")

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width','1200')
Config.set('graphics', 'height', '860')



class LoginPageFirst(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.box_layout1 = BoxLayout(orientation="horizontal", size_hint=[1, .5])
        self.box_layout = BoxLayout(orientation="vertical", size_hint=[None, None], size=[300, 300], spacing=20)

        self.box_layout.add_widget(Image(source="user.png", size_hint=[None, None], size=[300, 300]))

        self.login_confirm_lbl = Label(text="", size_hint=[None, None], size=[300, 50], font_size='30sp')
        self.box_layout.add_widget(self.login_confirm_lbl)

        self.user_email = TextInput(text="Email", size_hint=[None, None], size=[300, 50], background_color=[.92, .92, .92, .92], halign="center", font_size='20sp')
        self.box_layout.add_widget(self.user_email)



        self.login_confirm_btn = Button(
            text="Confirm",
            font_size=30,
            on_press=self.login_confirm_btn_press,
            background_color=[.13, .13, .13, .13],
            background_normal="",
            size_hint=[None, None],
            size=[300, 80],
        )
        self.box_layout.add_widget(self.login_confirm_btn)


        self.result_lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        self.box_layout.add_widget(self.result_lbl)
        self.box_layout1.add_widget(Widget())  # left space
        self.box_layout1.add_widget(self.box_layout)
        self.box_layout1.add_widget(Widget())  # Right space
        self.add_widget(self.box_layout1)

    def login_confirm_btn_press(self, instance):
        user_email = self.user_email.text
        if(self.getUser(user_email) == True):
            ea_app.screen_manager.current = "LoginPageSecond"
        else:
            self.result_lbl.text = self.getUser(user_email)



    def getUser(self, user_email):
        url = 'http://localhost:3000/api/user/' + str(user_email) +''
        x = requests.get(url)
        print(x.content)
        if(str(b'{"result":"User with specified email not found."}') != str(x.content)):
            s = json.loads(x.content)
            settings.user_id = str(s["userid"])
            settings.name = str(s["name"])
            settings.surname = str(s["surname"])
            settings.email = str(s["email"])
            #ea_app.first_page_user.show_info_about_user()
            ea_app.login_page_second.show_page()
            ea_app.login_page_second.say_hi_user()
            return True
        else:
            result_server = json.loads(x.content)
            return str(result_server["result"])



class LoginPageSecond(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def show_page(self):
        self.box_layout1 = BoxLayout(orientation="horizontal", size_hint=[1, .5])
        self.box_layout = BoxLayout(orientation="vertical", size_hint=[None, None], size=[300, 300], spacing=20)

        if os.path.isfile("C:/Users/wikto/PycharmProjects/EA/user_" + settings.user_id + ".png") == False:
            self.box_layout.add_widget(Image(source="user.png", size_hint=[None, None], size=[300, 300]))
        else:
            self.box_layout.add_widget(
                Image(source="user_" + settings.user_id + ".png", size_hint=[None, None], size=[300, 300]))


        self.login_confirm_lbl = Label(text="", size_hint=[None, None], size=[300, 50], font_size='30sp')
        self.box_layout.add_widget(self.login_confirm_lbl)

        self.password = TextInput(text="Password", size_hint=[None, None], size=[300, 50],
                                  background_color=[.92, .92, .92, .92], halign='center', password=1, font_size='20sp')
        self.box_layout.add_widget(self.password)

        self.login_btn = Button(
            text="Login",
            font_size=30,
            on_press=self.login_btn_press,
            background_color=[.13, .13, .13, .13],
            background_normal="",
            size_hint=[None, None],
            size=[300, 80],
        )
        self.box_layout.add_widget(self.login_btn)

        self.result_lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        self.box_layout.add_widget(self.result_lbl)

        self.box_layout1.add_widget(Widget())  # left space
        self.box_layout1.add_widget(self.box_layout)
        self.box_layout1.add_widget(Widget())  # Right space
        self.add_widget(self.box_layout1)


    def login_btn_press(self, instance):
        user_email = settings.email
        password = self.password.text
        if(self.logUser(user_email, password) == True):
            ea_app.screen_manager.current = "FirstPageUser"
        else:
            self.result_lbl.text = self.logUser(user_email, password)


    def logUser(self, user_email, password):
        url = 'http://localhost:3000/api/login'
        #myobj = '{"username":' + ' "' + str(user_email) + '", "pass": "'+ str(password) + '"}' # 0.0.3
        myobj = '{"email": "' + str(user_email) + '", "password": "' + str(password) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        if(str(b'{"result":"Incorrect username or password."}') != str(x.content)):
            result_server = json.loads(x.content)
            s = result_server[0]
            settings.role_id = str(s["roleid"])
            settings.name = str(s["name"])
            settings.registration_date = str(s['registrationdate'])
            ea_app.first_page_user.show_page()
            ea_app.first_page_user.show_info_about_user()
            return True
        else:
            result_server = json.loads(x.content)
            return str(result_server["result"])

    def say_hi_user(self):
        name = settings.name
        self.login_confirm_lbl.text = str(settings.hi_user_str + name)



class FirstPageUser(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def show_page(self):

        self.box_layout = BoxLayout(orientation="vertical", size_hint=[1, 1], spacing=20)
        self.box_layout1 = BoxLayout(orientation="horizontal", size_hint=[1, 1])

        self.role_lbl = Label(text="", text_size=self.size, valign="middle", size_hint=[.1, None], halign='left', font_size='20sp')
        self.box_layout.add_widget(self.role_lbl)

        if os.path.isfile("C:/Users/wikto/PycharmProjects/EA/user_" + settings.user_id + ".png") == False:
            self.box_layout.add_widget(Image(source="user.png", size_hint=[None, None], size=[300, 300]))
        else:
            self.box_layout.add_widget(
                Image(source="user_" + settings.user_id + ".png", size_hint=[None, None], size=[300, 300]))

        self.name_surname_lbl = Label(text="", size_hint=[None, None], size=[300, 50], font_size='30sp')
        self.box_layout.add_widget(self.name_surname_lbl)

        self.date_reg_lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        self.box_layout.add_widget(self.date_reg_lbl)

        self.box_layout.add_widget(self.box_layout1)


        self.box_layout.add_widget(Widget())  # Right space
        self.add_widget(self.box_layout)

    def regUser(self):
        url = 'http://localhost:3000/api/register-user'
        #myobj = '{"username": "John2", "pass": "12345", "role": "User", "description": "test record"}' # 0.0.3
        myobj = '{"name": "John", "surname": "Smith", "address": "128 East Greenview Street West Lafayette", "residencecountry": "USA", "nationality": "American", "sex": 1, "email": "abcdef@mail.com", "password": "123456", "phonenumber": "+777712345678", "birthdaydate": "1990-10-15", "roleid": 1}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        return str(x.content)


    def show_info_about_user(self):
        self.role_lbl.text = settings.get_role_name()
        self.name_surname_lbl.text = settings.name + " " + settings.surname



class EmployeeAdvisor(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.login_page_first = LoginPageFirst()
        screen = Screen(name="LoginPageFirst")
        screen.add_widget(self.login_page_first)
        self.screen_manager.add_widget(screen)

        self.login_page_second = LoginPageSecond()
        screen = Screen(name="LoginPageSecond")
        screen.add_widget(self.login_page_second)
        self.screen_manager.add_widget(screen)

        self.first_page_user = FirstPageUser()
        screen = Screen(name="FirstPageUser")
        screen.add_widget(self.first_page_user)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    ea_app = EmployeeAdvisor()
    ea_app.run()
