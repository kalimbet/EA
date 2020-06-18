import kivy
from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen
import settings as settings
import requests
import json
import zipfile
import os
import shutil
import cv2
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from PIL import Image as ImagePIL
from PIL import ImageDraw
import datetime
from datetime import datetime as DT
from kivy.uix.label import Label
from kivy.lang.builder import Builder


kivy.require("1.10.1")

Builder.load_string('''
<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)

''')



class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class LoginPageFirst(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))
        self.box_layout_horizontal = BoxLayout(orientation="horizontal", size_hint=[1, .5])
        self.box_layout_vertical = BoxLayout(orientation="vertical", size_hint=[None, None], size=[300, 300],
                                             spacing=20)

        self.box_layout_vertical.add_widget(Image(source="user.png", size_hint=[None, None], size=[300, 300]))

        self.login_confirm_lbl = Label(text="", size_hint=[None, None], size=[300, 50], font_size='30sp')
        self.box_layout_vertical.add_widget(self.login_confirm_lbl)

        self.user_email = TextInput(text="Email", size_hint=[None, None], size=[300, 50],
                                    background_color=[.92, .92, .92, .92], halign="center", font_size='20sp',
                                    multiline=False)
        self.box_layout_vertical.add_widget(self.user_email)

        self.login_confirm_btn = Button(
            text="Confirm",
            font_size=30,
            on_press=self.login_confirm_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[300, 80],
        )
        self.box_layout_vertical.add_widget(self.login_confirm_btn)

        self.result_lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        self.box_layout_vertical.add_widget(self.result_lbl)

        self.box_layout_horizontal.add_widget(Widget())  # left space
        self.box_layout_horizontal.add_widget(self.box_layout_vertical)
        self.box_layout_horizontal.add_widget(Widget())  # Right space
        self.add_widget(self.box_layout_horizontal)

    def login_confirm_btn_press(self, instance):
        user_email = self.user_email.text
        if (self.getUser(user_email) == True):
            ea_app.screen_manager.current = "LoginPageSecond"
        else:
            self.result_lbl.text = self.getUser(user_email)

    def getUser(self, user_email):
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/check/' + str(user_email) + ''
        x = requests.get(url)
        #print(x.content)
        if x.status_code == 200:
            s = json.loads(x.content)
            settings.user_id = str(s["userid"])
            settings.name = str(s["name"])
            settings.surname = str(s["surname"])
            settings.email = str(s["email"])
            # ea_app.first_page_user.page_all_role()
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
        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))

        self.box_layout_horizontal = BoxLayout(orientation="horizontal", size_hint=[1, .5])
        self.box_layout_vertical = BoxLayout(orientation="vertical", size_hint=[None, None], size=[300, 300],
                                             spacing=20)

        self.showAvatar()

        self.login_confirm_lbl = Label(text="", size_hint=[None, None], size=[300, 50], font_size='30sp')
        self.box_layout_vertical.add_widget(self.login_confirm_lbl)

        self.password = TextInput(text="Password", size_hint=[None, None], size=[300, 50],
                                  background_color=[.92, .92, .92, .92], halign='center', password=1, font_size='20sp',
                                  multiline=False)
        self.box_layout_vertical.add_widget(self.password)

        self.login_btn = Button(
            text="Login",
            font_size=30,
            on_press=self.login_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[300, 80],
        )
        self.box_layout_vertical.add_widget(self.login_btn)

        self.result_lbl = Label(text="", size_hint=[None, None], size=[300, 50])
        self.box_layout_vertical.add_widget(self.result_lbl)

        self.box_layout_horizontal.add_widget(Widget())  # left space
        self.box_layout_horizontal.add_widget(self.box_layout_vertical)
        self.box_layout_horizontal.add_widget(Widget())  # Right space
        self.add_widget(self.box_layout_horizontal)

    def showAvatar(self):
        url = 'http://' + settings.host + ':' + settings.port + '/file/user-picture/' + 'user_' + settings.user_id + '.png'
        x = requests.get(url)
        if x.status_code == 200:
            self.box_layout_vertical.add_widget(
                AsyncImage(source=url, size_hint=[None, None], size=[300, 300]))
        else:
            self.box_layout_vertical.add_widget(Image(source="user.png", size_hint=[None, None], size=[300, 300]))

    def login_btn_press(self, instance):
        user_email = settings.email
        password = self.password.text
        if (self.logUser(user_email, password) == True):
            ea_app.screen_manager.current = "FirstPageUser"
        else:
            self.result_lbl.text = self.logUser(user_email, password)

    def logUser(self, user_email, password):
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/login'
        myobj = '{"email": "' + str(user_email) + '", "password": "' + str(password) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        if x.status_code == 200:
            result_server = json.loads(x.content)
            s = result_server[0]
            settings.role_id = str(s["roleid"])
            settings.name = str(s["name"])
            settings.registration_date = str(s['registrationdate'])
            ea_app.first_page_user.show_page()
            return True
        else:
            result_server = json.loads(x.content)
            return str(result_server["result"])

    def say_hi_user(self):
        name = settings.name
        self.login_confirm_lbl.text = str(settings.hi_user_str + name)


class GeneralPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_page(self):
        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))



        self.box_layout_general_vertical = BoxLayout(orientation="vertical")
        self.box_layout_general_horizontal_up = BoxLayout(orientation="horizontal", padding=[20, 10])
        self.box_layout_general_horizontal_down = BoxLayout(orientation="horizontal", padding=[20, 10])

        self.box_layout_general_vertical_left = BoxLayout(orientation="vertical", size_hint=(.3, 1))
        self.box_layout_general_vertical_right = BoxLayout(orientation="vertical", size_hint=(.7, 1))

        self.box_layout_horizontal_left_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_vertical_left_up_side = BoxLayout(orientation="vertical", size_hint=(1, .45))

        self.box_layout_horizontal_right_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_horizontal_right_up_side = BoxLayout(orientation="horizontal", size_hint=(1, .45))

        if settings.menuIndex == 1:
            self.page_all_avatar()
            self.page_1_down_side()
            self.page_1_right_up_side()
            self.up_menu_side()

        elif settings.menuIndex == 2:
            self.page_all_avatar()
            self.page_2_down_side()
            self.page_1_right_up_side()
            self.up_menu_side()
        elif settings.menuIndex == 10:
            print("Test test")

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_left)  # Left general side
        self.box_layout_general_vertical_left.add_widget(self.box_layout_horizontal_left_up_menu)
        self.box_layout_general_vertical_left.add_widget(self.box_layout_vertical_left_up_side)

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_right)  # Right general side
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_menu)
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_side)

        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_up)
        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_down)

        self.add_widget(self.box_layout_general_vertical)

    def page_all_role(self):
        self.role_lbl.text = settings.get_role_name(settings.role_id)

    def page_all_avatar(self):
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .1], padding=[10, 10, 10, 0])
        self.role_lbl = Label(text="", text_size=self.size, valign="middle", size_hint=[0, 1], halign='left',
                              font_size='15sp')
        self.box_layout_horizontal_left_up_menu.add_widget(self.role_lbl)

        url = 'http://' + settings.host + ':' + settings.port + '/file/user-picture/' + 'user_' + settings.user_id + '.png'
        x = requests.get(url)
        if x.status_code == 200:
            self.box_layout_vertical_left_up_side.add_widget(
                AsyncImage(source=url, size_hint=[1, .6]))
        else:
            self.box_layout_vertical_left_up_side.add_widget(Image(source="user.png", size_hint=[1, .6]))

        nam = settings.name + '  ' + settings.surname
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        self.box_layout_vertical_left_up_side.add_widget(box_layout_for_btn)
        self.page_all_role()

    def page_all_recomendation(self):
        self.recomendation_lbl = Label(text=settings.recomendation_text, text_size=(1100, 500), size_hint=[.7, 1],
                                       font_size='20sp', halign="left", valign="top")
        self.box_layout_general_horizontal_down.add_widget(self.recomendation_lbl)

    def page_1_down_side(self):
        if settings.role_id == "1":
            self.page_question_left_down_side()
            self.page_all_recomendation()
        elif settings.role_id == "2":
            self.page_1_admin_down_side()
        elif settings.role_id == "3":
            self.page_1_project_manager_down_side()
        elif settings.role_id == "4":
            self.page_question_left_down_side()
            self.page_all_recomendation()
        elif settings.role_id == "5":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[1, 1]))

    def page_question_left_down_side(self):
        self.get_task_status_employee()
        self.box_left_down = BoxLayout(orientation="vertical", size_hint=[.3, 1])
        if settings.question_status == '2':
            self.question_lbl = Label(text=settings.question_text, text_size=(300, 60), size_hint=[1, .3],
                                      font_size='20sp', halign="left", valign="top")
            self.box_left_down.add_widget(self.question_lbl)
            self.box_button = BoxLayout(orientation="horizontal", size_hint=[1, None])

            yes_btn = Button(
                text="Yes",
                font_size=30,
                #on_press=self.yes_btn_press,
                # background_color=[.13, .13, .13],
                background_normal='button.png',
                background_down='button_down.png',
                size_hint=[None, None],
                size=[200, 80],
            )
            yes_btn.bind(on_release=lambda btn: self.yes_btn_press())

            no_btn = Button(
                text="No",
                font_size=30,
                #on_press=self.no_btn_press,
                # background_color=[.13, .13, .13],
                background_normal='button.png',
                background_down='button_down.png',
                size_hint=[None, None],
                size=[200, 80],
            )
            no_btn.bind(on_release=lambda btn: self.no_btn_press())

            self.box_button.add_widget(BoxLayout(size_hint=[.1, 1]))
            self.box_button.add_widget(yes_btn)
            self.box_button.add_widget(BoxLayout(size_hint=[.1, 1]))
            self.box_button.add_widget(no_btn)
            self.box_button.add_widget(BoxLayout(size_hint=[.1, 1]))
            self.box_left_down.add_widget(self.box_button)
            self.box_left_down.add_widget(Widget())
        elif settings.question_status == '1':
            self.question_lbl_alt = Label(text=settings.question_text_yes, text_size=(300, 60), size_hint=[1, .3],
                                          font_size='20sp', halign="left", valign="top")
            self.box_left_down.add_widget(self.question_lbl_alt)
            self.box_left_down.add_widget(Widget())
        elif settings.question_status == '0':
            self.question_lbl_alt = Label(text=settings.question_text_no, text_size=(300, 60), size_hint=[1, .3],
                                          font_size='20sp', halign="left", valign="top")
            self.box_left_down.add_widget(self.question_lbl_alt)
            self.box_left_down.add_widget(Widget())

        self.box_layout_general_horizontal_down.add_widget(self.box_left_down)

    def page_1_right_up_side(self):
        if settings.role_id == "1":
            self.page_1_employee_right_side_section_a()
            self.page_1_employee_right_side_section_b()
            self.page_1_employee_right_side_section_c()
        elif settings.role_id == "2":
            self.page_1_admin_right_side_section_a()
            self.page_1_admin_right_side_section_b()
        elif settings.role_id == "3":
            self.page_1_project_manager_section_a()
            self.page_1_project_manager_section_b()
        elif settings.role_id == "4":
            self.page_1_leader_right_side_section_a()
            self.page_1_leader_right_side_section_b()
            self.page_1_leader_right_side_section_c()
        elif settings.role_id == "5":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="A"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="B"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="C"))

    def page_1_admin_right_side_section_a(self):
        box_admin_vertical_section_a = BoxLayout(orientation="vertical", size_hint=[.5, 1], padding=[0, 0, 0, 0])
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .28], padding=[10, 10, 10, 0])

        url = 'http://' + settings.host + ':' + settings.port + '/file/user-picture/' + 'user_' + str(
            settings.selected_user_id) + '.png'
        x = requests.get(url)
        if x.status_code == 200:
            box_admin_vertical_section_a.add_widget(Widget())
            box_admin_vertical_section_a.add_widget(
                AsyncImage(source=url, size_hint=[1, .8]))
        else:
            box_admin_vertical_section_a.add_widget(Widget())
            box_admin_vertical_section_a.add_widget(Image(source="user.png", size_hint=[1, .8]))

        nam = settings.selected_user_name
        #nam = settings.selected_user_name + "  " + settings.selected_user_surname
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[1, 1],
            size=[270, 100],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        box_admin_vertical_section_a.add_widget(box_layout_for_btn)
        self.box_layout_horizontal_right_up_side.add_widget(box_admin_vertical_section_a)

    def page_1_admin_right_side_section_b(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal")
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_vertical_section_1 = BoxLayout(orientation="vertical")
        box_vertical_section_2 = BoxLayout(orientation="vertical")
        box_vertical_section_3 = BoxLayout(orientation="vertical")

        registration_btn = Button(
            text="Register a new user",
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        registration_btn.bind(on_release=lambda btn: self.load_reg_page())

        update_btn = Button(
            text="Update user info",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        update_btn.bind(on_release=lambda btn: self.load_upd_page())

        # train_recognizer_btn = Button(
        #     text="",
        #     font_size=30,
        #     # on_press=self.no_btn_press,
        #     background_color=[.13, .13, .13, 1],
        #     background_normal='',
        #     #background_down='button_down.png',
        #     size_hint=[None, None],
        #     size=[270, 100],
        # )

        view_user_info_btn = Button(
            text="View user info",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )

        groups_btn = Button(
            text="Groups",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )

        delete_user_btn = Button(
            text="Delete user",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        delete_user_btn.bind(on_release=lambda btn: self.delete_user())

        box_vertical_section_1.add_widget(Widget())
        box_vertical_section_1.add_widget(registration_btn)
        box_vertical_section_1.add_widget(Widget())
        box_vertical_section_1.add_widget(update_btn)
        box_vertical_section_1.add_widget(Widget())


        box_vertical_section_2.add_widget(Widget())
        box_vertical_section_2.add_widget(groups_btn)
        box_vertical_section_2.add_widget(Widget())
        box_vertical_section_2.add_widget(delete_user_btn)
        box_vertical_section_2.add_widget(Widget())

        box_vertical_section_3.add_widget(Widget())
        box_vertical_section_3.add_widget(BoxLayout(size_hint=[None, None], size=[270, 100]))
        # box_vertical_section_2.add_widget(train_recognizer_btn)
        box_vertical_section_3.add_widget(Widget())
        #box_vertical_section_3.add_widget(view_user_info_btn)
        box_vertical_section_3.add_widget(BoxLayout(size_hint=[None, None], size=[270, 100]))
        box_vertical_section_3.add_widget(Widget())

        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)
        box_horizontal_section.add_widget(box_vertical_section_3)

        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_section_b)

    def page_1_admin_down_side(self):
        self.admin_load_all_users()
        bx_vertical_down_right_side = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx_header = BoxLayout(orientation="horizontal", size_hint=[1, .07])
        bx_content = BoxLayout(orientation="horizontal", size_hint=[1, .93])
        bx_header.add_widget(Button(text="Id", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Name", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Surname", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Registration date", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Email", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(1, None), width=500)


        layout.bind(minimum_height=layout.setter('height'))

        self.test = []

        for i in range(len(settings.list_of_users)):
            item = settings.list_of_users[i]
            if settings.user_id != str(item["userid"]):
                bx_item = BoxLayout(orientation="horizontal", size=(0, 40),
                                    size_hint=(1, None))


                btn = Button(text=str(item["userid"]), on_press=self.change_to_selected_user, font_size=25,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')
                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["name"]), on_press=self.change_to_selected_user, font_size=25,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')
                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["surname"]), on_press=self.change_to_selected_user, font_size=25,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')

                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["registrationdate"].split('T')[0]), font_size=25, on_press=self.change_to_selected_user,
                             id=str(item["email"].split('T')[0]),
                             background_color=(.01, .66, .96, 1), background_normal='')
                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["email"]), font_size=25, on_press=self.change_to_selected_user,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')

                self.test.append(btn)
                bx_item.add_widget(btn)
                layout.add_widget(bx_item)


        root = ScrollView(size_hint=(1, 1),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        bx_content.add_widget(root)

        bx_vertical_down_right_side.add_widget(bx_header)
        bx_vertical_down_right_side.add_widget(bx_content)

        self.change_color_selecter()
        self.box_layout_general_horizontal_down.add_widget(bx_vertical_down_right_side)

    def page_1_project_manager_down_side(self):
        self.get_all_groups()
        bx_vertical_down_right_side = BoxLayout(orientation="vertical", size_hint=[.7, 1])
        bx_header = BoxLayout(orientation="horizontal", size_hint=[1, .07])
        bx_content = BoxLayout(orientation="horizontal", size_hint=[1, .93])
        bx_header.add_widget(Button(text="Group id", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Name of group", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Leader id", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Leader name", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Leader surname", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="From date", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))

        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(1, None), width=500)

        layout.bind(minimum_height=layout.setter('height'))

        for i in range(len(settings.list_of_all_groups)):
            item = settings.list_of_all_groups[i]
            bx_item = BoxLayout(orientation="horizontal", size=(0, 40),
                                size_hint=(1, None))

            btn = Button(text=str(item["groupid"]), font_size=25,
                         background_color=(.01, .66, .96, 1), background_normal='')
            bx_item.add_widget(btn)

            btn = Button(text=str(item["groupname"]), font_size=25,
                         background_color=(.01, .66, .96, 1), background_normal='')
            bx_item.add_widget(btn)
            btn = Button(text=str(item["groupleaderid"]), font_size=25,
                         background_color=(.01, .66, .96, 1), background_normal='')

            bx_item.add_widget(btn)
            btn = Button(text=str(item["name"]), font_size=25,
                         background_color=(.01, .66, .96, 1), background_normal='')
            bx_item.add_widget(btn)
            btn = Button(text=str(item["surname"]), font_size=25,
                         background_color=(.01, .66, .96, 1), background_normal='')
            bx_item.add_widget(btn)

            btn = Button(text=str(item["registrationdate"]), font_size=25,
                         background_color=(.01, .66, .96, 1), background_normal='')
            bx_item.add_widget(btn)

            layout.add_widget(bx_item)


        root = ScrollView(size_hint=(1, 1),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        bx_content.add_widget(root)

        bx_vertical_down_right_side.add_widget(bx_header)
        bx_vertical_down_right_side.add_widget(bx_content)

        self.box_layout_general_horizontal_down.add_widget(bx_vertical_down_right_side)

    def page_1_project_manager_section_a(self):
        box_project_manager_vertical_section_a = BoxLayout(orientation="vertical", size_hint=[.5, 1], padding=[0, 0, 0, 0])
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .28], padding=[10, 10, 10, 0])

        if os.path.isfile("C:/Users/wikto/PycharmProjects/EA/user_" + str(settings.pm_selected_group_id) + ".png") == False:
            box_project_manager_vertical_section_a.add_widget(Widget())
            box_project_manager_vertical_section_a.add_widget(
                Image(source="user.png", size_hint=[1, .8]))
        else:
            box_project_manager_vertical_section_a.add_widget(Widget())
            box_project_manager_vertical_section_a.add_widget(
                Image(source="user_" + str(settings.selected_user_id) + ".png", size_hint=[1, .8]))
        nam = settings.pm_selected_group_leader_name + "  " + settings.pm_selected_group_leader_surname
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
            size=[270, 100],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        box_project_manager_vertical_section_a.add_widget(box_layout_for_btn)
        self.box_layout_horizontal_right_up_side.add_widget(box_project_manager_vertical_section_a)

    def page_1_project_manager_section_b(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal")
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_vertical_section_1 = BoxLayout(orientation="vertical", size_hint=[.5, 1])
        box_vertical_section_2 = BoxLayout(orientation="vertical", size_hint=[.5, 1])

        group_name_btn = Button(
            text="Name of group",
            font_size=30,
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, None],
            size=[0, 100],
        )
        box_vertical_section_1.add_widget(BoxLayout(size_hint=[1, .3]))
        box_vertical_section_1.add_widget(group_name_btn)
        box_vertical_section_1.add_widget(BoxLayout(size_hint=[1, .1]))
        group_description_btn = Button(
            text="Description",
            font_size=30,
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
        )

        box_vertical_section_1.add_widget(group_description_btn)

        group_name_btn = Button(
            text=settings.pm_selected_group_name,
            font_size=30,
            background_color=(.01, .66, .96, 1),
            background_normal='',
            size_hint=[1, None],
            size=[0, 100],
        )
        box_vertical_section_2.add_widget(BoxLayout(size_hint=[1, .3]))
        box_vertical_section_2.add_widget(group_name_btn)
        box_vertical_section_2.add_widget(BoxLayout(size_hint=[1, .1]))
        group_description_btn = Button(
            text=settings.pm_selected_group_description,
            font_size=30,
            # on_press=self.no_btn_press,
            background_color=(.01, .66, .96, 1),
            background_normal='',
            #background_down='button.png',
            size_hint=[1, 1],

        )

        box_vertical_section_2.add_widget(group_description_btn)


        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)

        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_section_b)

    def page_1_employee_right_side_section_a(self):
        self.get_average_for_week()
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        box_vertical_left.add_widget(
            Button(text="Average rating for week", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        box_vertical_left.add_widget(Button(text=settings.employee_average_rating_for_week + ' / ' + settings.average_max_week, background_color=[.13, .13, .13, 1],
            background_normal='', font_size=30))
        box_vertical_left.add_widget(
            Button(text="", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)
        print("test")

    def page_1_employee_right_side_section_b(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        box_vertical_left.add_widget(
            Button(text="Average rating for month", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        box_vertical_left.add_widget(Button(text=settings.employee_average_rating_for_month + ' / ' + settings.average_max_month,
                                     background_color=[.13, .13, .13, 1],
                                     background_normal='', font_size=30))
        box_vertical_left.add_widget(
            Button(text="", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_1_employee_right_side_section_c(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        box_vertical_left.add_widget(
            Button(text="Average rating for month", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        box_vertical_left.add_widget(Button(text=settings.employee_average_rating_for_year+ ' / ' + settings.average_max_year,
                                     background_color=[.13, .13, .13, 1],
                                     background_normal='', font_size=30))
        box_vertical_left.add_widget(
            Button(text="", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_1_leader_right_side_section_a(self):
        self.get_average_for_week()
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        box_vertical_left.add_widget(
            Button(text="Average rating for week", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        box_vertical_left.add_widget(Button(text=settings.employee_average_rating_for_week + ' / ' + settings.average_max_week, background_color=[.13, .13, .13, 1],
            background_normal='', font_size=30))
        box_vertical_left.add_widget(
            Button(text="", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)
        print("test")

    def page_1_leader_right_side_section_b(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        box_vertical_left.add_widget(
            Button(text="Average rating for month", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        box_vertical_left.add_widget(Button(text=settings.employee_average_rating_for_month + ' / ' + settings.average_max_month,
                                     background_color=[.13, .13, .13, 1],
                                     background_normal='', font_size=30))
        box_vertical_left.add_widget(
            Button(text="", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_1_leader_right_side_section_c(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        box_vertical_left.add_widget(
            Button(text="Average rating for month", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        box_vertical_left.add_widget(Button(text=settings.employee_average_rating_for_year+ ' / ' + settings.average_max_year,
                                     background_color=[.13, .13, .13, 1],
                                     background_normal='', font_size=30))
        box_vertical_left.add_widget(
            Button(text="", background_color=[0, 0, 0, 1],
                   background_normal='', font_size=30, size_hint=[1, .2]))
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_2_down_side(self):
        if settings.role_id == "1":
            self.page_question_left_down_side()
            self.page_2_employee_right_down_side()
        elif settings.role_id == "2":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.page_2_admin_right_down_side()
        elif settings.role_id == "3":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
        elif settings.role_id == "4":
            self.page_question_left_down_side()
            self.page_2_leader_right_down_side()
        elif settings.role_id == "5":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[8, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.2, 1]))

    def page_2_right_up_side(self):
        if settings.role_id == "1":
            self.page_2_employee_right_side_section_a()
        elif settings.role_id == "2":
            self.page_2_admin_right_side_section_a()
            self.page_2_admin_right_side_section_b()
        elif settings.role_id == "3":
            self.page_2_project_manager_section_a()
            self.page_2_project_manager_section_b()
        elif settings.role_id == "4":
            self.page_2_leader_right_side_section_a()
        elif settings.role_id == "5":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 2"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 2"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 2"))

    def page_2_employee_right_side_section_a(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx = BoxLayout(orientation="horizontal", size_hint=[.8, .05])
        for i in range(len(settings.list_employee_for_days)):
            bx.add_widget(Button(text=str(settings.list_employee_for_days[i]), size_hint=[None, None], size=[100, 30],
                                 background_color=(0, 0, 0, 1), background_normal=''))
            bx.add_widget(Button(text="", size_hint=[None, None], size=[100, 30], background_color=(0, 0, 0, 1),
                                 background_normal=''))
        box_vertical_left.add_widget(GraphWidgetForDays())
        box_vertical_left.add_widget(bx)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_2_leader_right_side_section_a(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx = BoxLayout(orientation="horizontal", size_hint=[.8, .05])

        for i in range(len(settings.list_leader_for_days)):
            bx.add_widget(Button(text=str(settings.list_leader_for_days[i]), size_hint=[None, None], size=[100, 30],
                                 background_color=(0, 0, 0, 1), background_normal=''))
            bx.add_widget(Button(text="", size_hint=[None, None], size=[100, 30], background_color=(0, 0, 0, 1),
                                 background_normal=''))

        box_vertical_left.add_widget(GraphWidgetForDays())
        box_vertical_left.add_widget(bx)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_2_employee_right_down_side(self):
        self.get_last_week()
        bx_vertical_down_right_side = BoxLayout(orientation="vertical", size_hint=[.7, 1])
        bx_header = BoxLayout(orientation="horizontal", size_hint=[1, .07])
        bx_content = BoxLayout(orientation="horizontal", size_hint=[1, .93])


        bx_header.add_widget(Button(text="Date", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Day", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Time on rest", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Time on work", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Rating for day", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(1, None), width=500)

        layout.bind(minimum_height=layout.setter('height'))

       # print(settings.list_user_last_week)

        for i in range(len(settings.list_user_last_week)):
            item = settings.list_user_last_week[i]
            if settings.user_id == str(item["userid"]):
                bx_item = BoxLayout(orientation="horizontal", size=(0, 40),
                                    size_hint=(1, None))

                dateConverted = DT.strptime(item["date"].split('T')[0], "%Y-%m-%d")
                weekDay = dateConverted.weekday()

                btn = Button(text=str(item["date"].split('T')[0]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(settings.get_name_week(str(weekDay))), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(item["timeonrest"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                btn = Button(text=str(item["timeonwork"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(item["rating"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                layout.add_widget(bx_item)

        root = ScrollView(size_hint=(1, 1),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        bx_content.add_widget(root)

        bx_vertical_down_right_side.add_widget(bx_header)
        bx_vertical_down_right_side.add_widget(bx_content)

        self.box_layout_general_horizontal_down.add_widget(bx_vertical_down_right_side)

    def page_2_admin_right_down_side(self):
        self.get_last_week()
        bx_vertical_down_right_side = BoxLayout(orientation="vertical", size_hint=[.7, 1])
        bx_header = BoxLayout(orientation="horizontal", size_hint=[1, .07])
        bx_content = BoxLayout(orientation="horizontal", size_hint=[1, .93])


        bx_header.add_widget(Button(text="Date", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Day", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Time on rest", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Time on work", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Rating for day", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(1, None), width=500)

        layout.bind(minimum_height=layout.setter('height'))

       # print(settings.list_user_last_week)

        for i in range(len(settings.list_user_last_week)):
            item = settings.list_user_last_week[i]
            if settings.selected_user_id == str(item["userid"]):
                bx_item = BoxLayout(orientation="horizontal", size=(0, 40),
                                    size_hint=(1, None))

                dateConverted = DT.strptime(item["date"].split('T')[0], "%Y-%m-%d")
                weekDay = dateConverted.weekday()

                btn = Button(text=str(item["date"].split('T')[0]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(settings.get_name_week(str(weekDay))), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(item["timeonrest"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                btn = Button(text=str(item["timeonwork"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(item["rating"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                layout.add_widget(bx_item)

        root = ScrollView(size_hint=(1, 1),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        bx_content.add_widget(root)

        bx_vertical_down_right_side.add_widget(bx_header)
        bx_vertical_down_right_side.add_widget(bx_content)

        self.box_layout_general_horizontal_down.add_widget(bx_vertical_down_right_side)

    def page_2_admin_right_side_section_a(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, .7])
        bx = BoxLayout(orientation="horizontal", size_hint=[.8, .05])
        for i in range(len(settings.list_employee_for_days)):
            bx.add_widget(Button(text=str(settings.list_employee_for_days[i]), size_hint=[None, None], size=[100, 30],
                                 background_color=(0, 0, 0, 1), background_normal=''))
            bx.add_widget(Button(text="", size_hint=[None, None], size=[100, 30], background_color=(0, 0, 0, 1),
                                 background_normal=''))
        box_vertical_left.add_widget(GraphWidgetForDays())
        box_vertical_left.add_widget(bx)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_2_admin_right_side_section_b(self):
        box_admin_vertical_section_a = BoxLayout(orientation="vertical", size_hint=[.3, 1], padding=[0, 0, 0, 0])
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .28], padding=[10, 10, 10, 0])

        url = 'http://' + settings.host + ':' + settings.port + '/file/user-picture/' + 'user_' + str(
            settings.selected_user_id) + '.png'
        x = requests.get(url)
        if x.status_code == 200:
            box_admin_vertical_section_a.add_widget(Widget())
            box_admin_vertical_section_a.add_widget(
                AsyncImage(source=url, size_hint=[1, .8]))
        else:
            box_admin_vertical_section_a.add_widget(Widget())
            box_admin_vertical_section_a.add_widget(Image(source="user.png", size_hint=[1, .8]))

        nam = settings.selected_user_name
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
            size=[270, 100],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        box_admin_vertical_section_a.add_widget(box_layout_for_btn)
        self.box_layout_horizontal_right_up_side.add_widget(box_admin_vertical_section_a)

    def page_2_project_manager_section_a(self):
        box_project_manager_vertical_section_a = BoxLayout(orientation="vertical", size_hint=[.5, 1], padding=[0, 0, 0, 0])
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .28], padding=[10, 10, 10, 0])

        if os.path.isfile("C:/Users/wikto/PycharmProjects/EA/user_" + str(settings.pm_selected_group_id) + ".png") == False:
            box_project_manager_vertical_section_a.add_widget(Widget())
            box_project_manager_vertical_section_a.add_widget(
                Image(source="user.png", size_hint=[1, .8]))
        else:
            box_project_manager_vertical_section_a.add_widget(Widget())
            box_project_manager_vertical_section_a.add_widget(
                Image(source="user_" + str(settings.selected_user_id) + ".png", size_hint=[1, .8]))
        nam = settings.pm_selected_group_leader_name + "  " + settings.pm_selected_group_leader_surname
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
            size=[270, 100],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        box_project_manager_vertical_section_a.add_widget(box_layout_for_btn)
        self.box_layout_horizontal_right_up_side.add_widget(box_project_manager_vertical_section_a)

    def page_2_project_manager_section_b(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal", padding=[20, 0, 0, 0])
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_vertical_section_1 = BoxLayout(orientation="vertical")
        box_vertical_section_2 = BoxLayout(orientation="vertical")

        view_leader_btn = Button(
            text="View user info",
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        view_leader_btn.bind(on_release=lambda btn: self.load_upd_page())

        set_leader_status_btn = Button(
            text="Update user info",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        set_leader_status_btn.bind(on_release=lambda btn: self.load_upd_page())

        delete_user_btn = Button(
            text="Delete user",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )

        box_vertical_section_1.add_widget(Widget())
        box_vertical_section_1.add_widget(view_leader_btn)
        box_vertical_section_1.add_widget(Widget())
        box_vertical_section_1.add_widget(set_leader_status_btn)

        box_vertical_section_2.add_widget(Widget())
        box_vertical_section_2.add_widget(BoxLayout(size_hint=[None, None], size=[270, 100],))
        box_vertical_section_2.add_widget(Widget())
        box_vertical_section_2.add_widget(delete_user_btn)

        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)


        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_section_b)

    def page_2_leader_right_down_side(self):
        #self.get_last_week()
        bx_vertical_down_right_side = BoxLayout(orientation="vertical", size_hint=[.7, 1])
        bx_header = BoxLayout(orientation="horizontal", size_hint=[1, .07])
        bx_content = BoxLayout(orientation="horizontal", size_hint=[1, .93])
        bx_header.add_widget(Button(text="Date", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Day", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Time on rest", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Time on work", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Rating for day", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(1, None), width=500)

        layout.bind(minimum_height=layout.setter('height'))

        print(settings.list_leader_last_week)

        for i in range(len(settings.list_leader_last_week)):
            item = settings.list_user_last_week[i]
            if settings.user_id == str(item["userid"]):
                bx_item = BoxLayout(orientation="horizontal", size=(0, 40),
                                    size_hint=(1, None))

                btn = Button(text=str(item["date"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                btn = Button(text=str(item["surname"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')

                bx_item.add_widget(btn)
                btn = Button(text=str(item["timeonrest"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                btn = Button(text=str(item["timeonwork"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)

                btn = Button(text=str(item["rating"]), font_size=25,
                             background_color=(.01, .66, .96, 1), background_normal='')
                bx_item.add_widget(btn)
                layout.add_widget(bx_item)

        root = ScrollView(size_hint=(1, 1),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        bx_content.add_widget(root)

        bx_vertical_down_right_side.add_widget(bx_header)
        bx_vertical_down_right_side.add_widget(bx_content)

        self.box_layout_general_horizontal_down.add_widget(bx_vertical_down_right_side)

    def page_3_down_side(self):
        if settings.role_id == "1":
            self.page_question_left_down_side()
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "2":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "3":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "4":
            self.page_question_left_down_side()
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "5":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))

    def page_3_right_up_side(self):
        if settings.role_id == "1":
            self.page_3_employee_right_side_section_a()
        elif settings.role_id == "2":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 3"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 3"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 3"))
        elif settings.role_id == "3":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 3"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 3"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 3"))
        elif settings.role_id == "4":
            self.page_3_leader_right_side_section_a()
        elif settings.role_id == "5":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 3"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 3"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 3"))

    def page_3_leader_right_side_section_a(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx = BoxLayout(orientation="horizontal", size_hint=[.8, .05])

        for i in range(len(settings.list_leader_for_weeks)):
            bx.add_widget(Button(text=str(settings.list_leader_for_weeks[i]), size_hint=[None, None], size=[100, 30],
                                 background_color=(0, 0, 0, 1), background_normal=''))
            bx.add_widget(Button(text="", size_hint=[None, None], size=[100, 30], background_color=(0, 0, 0, 1),
                                 background_normal=''))

        box_vertical_left.add_widget(GraphWidgetForWeeks())
        box_vertical_left.add_widget(bx)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_3_employee_right_side_section_a(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx = BoxLayout(orientation="horizontal", size_hint=[.8, .05])
        for i in range(len(settings.list_employee_for_weeks)):
            bx.add_widget(Button(text=str(settings.list_employee_for_weeks[0]), size_hint=[None, None], size=[100, 30],
                                 background_color=(0, 0, 0, 1), background_normal=''))
            bx.add_widget(Button(text="", size_hint=[None, None], size=[100, 30], background_color=(0, 0, 0, 1),
                                 background_normal=''))

        box_vertical_left.add_widget(GraphWidgetForWeeks())
        box_vertical_left.add_widget(bx)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_4_down_side(self):
        if settings.role_id == "1":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "2":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "3":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[1, 1]))
        elif settings.role_id == "4":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "5":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))

    def page_4_right_up_side(self):
        if settings.role_id == "1":
            self.page_4_employee_right_side_section_a()
        elif settings.role_id == "2":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 4"))
        elif settings.role_id == "3":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 4"))

        elif settings.role_id == "4":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 4"))
        elif settings.role_id == "5":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 4"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 4"))

    def page_4_employee_right_side_section_a(self):
        box_vertical_left = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx = BoxLayout(orientation="horizontal", size_hint=[.8, .05])

        for i in range(len(settings.list_employee_for_months)):
            bx.add_widget(Button(text=str(settings.list_employee_for_months[i]), size_hint=[None, None], size=[50, 30],
                                 background_color=(0, 0, 0, 1), background_normal=''))
            bx.add_widget(Button(text="", size_hint=[None, None], size=[50, 30], background_color=(0, 0, 0, 1),
                                 background_normal=''))

        box_vertical_left.add_widget(GraphWidgetForMonths())
        box_vertical_left.add_widget(bx)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_left)

    def page_5_down_side(self):
        if settings.role_id == "1":
            self.page_question_left_down_side()
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "2":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "3":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[1, 1]))
        elif settings.role_id == "4":
            self.page_question_left_down_side()
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.7, 1]))
        elif settings.role_id == "5":
            self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[1, 1]))

    def page_5_right_up_side(self):
        if settings.role_id == "1":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 5"))
        elif settings.role_id == "2":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 5"))
        elif settings.role_id == "3":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 5"))

        elif settings.role_id == "4":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 5"))
        elif settings.role_id == "5":
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="1 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="2 page 5"))
            self.box_layout_horizontal_right_up_side.add_widget(Button(text="3 page 5"))

    def up_menu_side(self):
        if settings.role_id == "1":
            #self.box_layout_horizontal_right_up_menu.add_widget(Button(text="Calendar"))
            self.calendar_left()
            self.box_layout_horizontal_right_up_menu.add_widget(Widget())
            self.menu_right()

        elif settings.role_id == "2":
            self.calendar_left()
            self.menu_center()
            self.menu_right()

        elif settings.role_id == "3":
            self.calendar_left()
            self.menu_center()
            self.menu_right()

        elif settings.role_id == "4":
            self.calendar_left()
            self.menu_center()
            self.menu_right()

        elif settings.role_id == "5":
            self.calendar_left()
            self.menu_center()
            self.menu_right()

    def menu_center(self):
        self.box_layout_search = BoxLayout(orientation="horizontal", padding=[20, 0, 0, 0])
        self.search_text = TextInput(text="Search", size_hint=[.7, .7],
                                     background_color=[.92, .92, .92, .92], halign='center', font_size='20sp',
                                     multiline=False)
        self.box_layout_search.add_widget(self.search_text)

        self.search_btn = Button(
            text="Go",
            font_size=30,
            on_press=self.search_btn_press,
            # background_color=[.13, .13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[.3, .7],
        )

        self.box_layout_search.add_widget(self.search_btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_search)

    def search_btn_press(self, instance):
        print("Search result")

    def menu_right(self):
        self.box_layout_menu_right = BoxLayout(orientation="horizontal")
        self.dropdown = DropDown()
        for index in range(5):
            if index == 0:
                name_of_page = 'General'
            elif index == 1:
                name_of_page = 'Days'
            elif index == 2:
                name_of_page = 'Weeks'
            elif index == 3:
                name_of_page = 'Months'
            elif index == 4:
                name_of_page = 'Years'

            self.dropdownButton= Button(text=name_of_page, size_hint_y=None, height=44,
                         font_size=30,
                         background_color=[0, 0, 0, .8],
                         #background_normal='button.png',
                         background_down='button_down.png',
                         size_hint=[1, None],
                         )
            self.dropdownButton.bind(on_release=lambda dropdownButton: self.dropdown.select(dropdownButton.text))
            if index == 0:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_first())
            elif index == 1:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_second())
            elif index == 2:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_third())
            elif index == 3:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_fourth())
            elif index == 4:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_fifth())

            self.dropdown.add_widget(self.dropdownButton)

        mainbutton = Button(text='General',
                            font_size=30,
                            #background_color=[.13, .13, .13, .13],
                            background_normal='button_menu.png',
                            background_down='button_down.png',
                            size_hint=[.7, .7],
                            )

        mainbutton.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.box_layout_menu_right.add_widget(Widget())
        self.box_layout_menu_right.add_widget(mainbutton)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_right)

    def calendar_left(self):
        date = datetime.datetime.now().date()
        weekDay = datetime.datetime.now().weekday()
        self.box_layout_menu_left = BoxLayout(orientation="horizontal")
        btn = Button(text=str(date),
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     background_down='button.png',
                     size_hint=[1, .7],
                     )
        self.box_layout_menu_left.add_widget(btn)
        btn = Button(text=settings.get_name_week(str(weekDay)),
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     background_down='button.png',
                     size_hint=[1, .7],
                     )
        self.box_layout_menu_left.add_widget(btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_left)

    def page_first(self):
        settings.menuIndex = 1
        self.box_layout_general_horizontal_down.clear_widgets()
        self.box_layout_horizontal_right_up_side.clear_widgets()
        self.page_1_down_side()
        self.page_1_right_up_side()

    def page_second(self):
        settings.menuIndex = 2
        self.box_layout_general_horizontal_down.clear_widgets()
        self.box_layout_horizontal_right_up_side.clear_widgets()
        self.page_2_down_side()
        self.page_2_right_up_side()

    def page_third(self):
        settings.menuIndex = 3
        self.box_layout_general_horizontal_down.clear_widgets()
        self.box_layout_horizontal_right_up_side.clear_widgets()
        self.page_3_down_side()
        self.page_3_right_up_side()

    def page_fourth(self):
        settings.menuIndex = 4
        self.box_layout_general_horizontal_down.clear_widgets()
        self.box_layout_horizontal_right_up_side.clear_widgets()
        self.page_4_down_side()
        self.page_4_right_up_side()

    def page_fifth(self):
        settings.menuIndex = 5
        self.box_layout_general_horizontal_down.clear_widgets()
        self.box_layout_horizontal_right_up_side.clear_widgets()
        self.page_5_down_side()
        self.page_5_right_up_side()

    def load_reg_page(self):
        ea_app.screen_manager.current = "RegistrationPage"
        ea_app.registration_page.show_page()

    def load_upd_page(self):
        ea_app.screen_manager.current = "UpdateUserPage"
        ea_app.update_user_page.show_page()

    def admin_load_all_users(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/admin/get-users'
        x = requests.get(url)
        settings.list_of_users = json.loads(x.content)
        print(settings.list_of_users)

    def get_average_for_week(self):
        self.get_last_week()
        avg_week = 0
        print(settings.list_employee_for_days)
        for i in range(len(settings.list_employee_for_days)):
            if len(settings.list_employee_for_days) == 5:
                x = settings.list_employee_for_days[i]
                avg_week = avg_week + float(x)

        settings.employee_average_rating_for_week = str(avg_week / len(settings.list_employee_for_days))

    def get_group(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/pm/get-controlled-groups/' + str(settings.user_id) + ''
        x = requests.get(url)
        if x.status_code == 200:
            print(x.content)
            #s = json.loads(x.content)
            #user_id = str(s["userid"])

    def get_all_groups(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/admin/get-all-groups'
        x = requests.get(url)
        print(x.content)
        if x.status_code == 200:
            settings.list_of_all_groups = json.loads(x.content)



    def get_last_week(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/get-last-week-rating'
        if settings.role_id == '1':
            myobj = '{"userid": "' + str(settings.user_id) + '"}'
        elif settings.role_id == '2':
            myobj = '{"userid": "' + str(settings.selected_user_id) + '"}'
        elif settings.role_id == '4':
            myobj = '{"userid": "' + str(settings.user_id) + '"}'


        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        if x.status_code == 200:
            settings.list_user_last_week = json.loads(x.content)
            self.save_rating_to_dist()

        else:
            print("Error: " + x.content)

    def save_rating_to_dist(self):
        for i in range(len(settings.list_employee_for_days)):
            settings.list_employee_for_days[i] = 0

        new_list = []
        if len(settings.list_user_last_week) == 5:
            for i in range(5):
                user = settings.list_user_last_week[i]
                new_list.append(user['rating'])


        for i in range(len(new_list)):
            settings.list_employee_for_days[i] = new_list[i]


    def change_to_selected_user(self, instance):
        settings.selected_user_email = str(instance.id)

        self.get_user()
        self.box_layout_horizontal_right_up_side.clear_widgets()
        if settings.selected_user_last_email != settings.selected_user_email:
            self.change_color_selecter()
            self.change_color_selecter_back()
            settings.selected_user_last_email = settings.selected_user_email

        self.page_1_right_up_side()

    def get_user(self):
        for i in range(len(settings.list_of_users)):
            user = settings.list_of_users[i]
            if settings.selected_user_email == user['email']:
                settings.selected_user_id = str(user["userid"])
                settings.selected_user_name = str(user["name"])
                settings.selected_user_surname = str(user["surname"])
                settings.selected_user_address = str(user["address"])
                settings.selected_nationality = str(user["nationality"])
                settings.selected_birthday_date = str(user["birthdaydate"].split('T')[0])
                settings.selected_residence_country = str(user["residencecountry"])
                settings.selected_sex = str(user["sex"])
                settings.selected_phone_number = str(user["phonenumber"])
                settings.selected_role_id = str(user["roleid"])
                settings.selected_registration_date = str(user["registrationdate"].split('T')[0])
                #settings.selected_password = str(user["password"])

    def delete_user(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/admin/remove-user'
        myobj = '{"userid": "' + settings.selected_user_id + '"}'
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, headers=headers, data=myobj)
        if response.status_code == 200:
            self.box_layout_general_horizontal_down.clear_widgets()
            self.page_1_down_side()

    def get_task_status_employee(self):
        date = datetime.datetime.now().date()
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/get-daily-task-status'
        myobj = '{"userid": "' + settings.user_id + '", "date": "' + str(date) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        if x.status_code == 200:
            status_dist = json.loads(x.content)
            settings.question_status = str(status_dist["workfinished"])

    def get_task_status_leader(self):
        date = datetime.datetime.now().date()

    def yes_btn_press(self):
        date = datetime.datetime.now().date()
        yes = '1'
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/set-daily-question'
        myobj = '{"userid": "' + settings.user_id + '", "workfinished": "' + yes + '", "date": "' + str(date) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)


        self.box_layout_general_horizontal_down.clear_widgets()
        if settings.menuIndex == 1:
            self.page_1_down_side()
        elif settings.menuIndex == 2:
            self.page_2_down_side()
        elif settings.menuIndex == 3:
            self.page_3_down_side()
        elif settings.menuIndex == 4:
            self.page_4_down_side()
        elif settings.menuIndex == 5:
            self.page_5_down_side()

    def no_btn_press(self):
        date = datetime.datetime.now().date()
        no = '0'
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/set-daily-question'
        myobj = '{"userid": "' + settings.user_id + '", "workfinished": "' + no + '", "date": "' + str(date) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        self.box_layout_general_horizontal_down.clear_widgets()
        if settings.menuIndex == 1:
            self.page_1_down_side()
        elif settings.menuIndex == 2:
            self.page_2_down_side()
        elif settings.menuIndex == 3:
            self.page_3_down_side()
        elif settings.menuIndex == 4:
            self.page_4_down_side()
        elif settings.menuIndex == 5:
            self.page_5_down_side()

    def change_color_selecter(self):
        for i in range(len(self.test)):
            if self.test[i].id == settings.selected_user_email:
                self.test[i].background_color = (.01, .66, .96, .6)

    def change_color_selecter_back(self):
            for i in range(len(self.test)):
                if self.test[i].id == settings.selected_user_last_email:
                    self.test[i].background_color = (.01, .66, .96, 1)

class GraphWidgetForDays(Widget):
    def __init__(self, **kwargs):
        super(GraphWidgetForDays, self).__init__(**kwargs)

        with self.canvas:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.draw_box()
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])


    def draw_box(self):
        size_window = Window.size
        window_x = size_window[0]
        window_y = size_window[1]
        pos_x = (window_x / 10) * 3.04
        pos_y = (window_y / 10) * 5.3
        posX = pos_x + 0
        posY = pos_y + 10

        if settings.role_id == "1":
            list_for_draw = settings.list_employee_for_days
        elif settings.role_id == "2":
            list_for_draw = settings.list_employee_for_days
        elif settings.role_id == "3":
            list_for_draw = settings.list_employee_for_days
        elif settings.role_id == "4":
            list_for_draw = settings.list_leader_for_days
        elif settings.role_id == "5":
            list_for_draw = settings.list_user_for_days

        final_list = []
        max_y = 350
        x = 100
        y0 = 0
        if len(list_for_draw) == 5:
            for i in list_for_draw:
                final_list.append(i * 14.28)
            y1 = max_y / 100 * final_list[0]
            y2 = max_y / 100 * final_list[1]
            y3 = max_y / 100 * final_list[2]
            y4 = max_y / 100 * final_list[3]
            y5 = max_y / 100 * final_list[4]

            with self.canvas.after:
                Color(.01, .66, .96, 1)
                Rectangle(pos=(posX, posY), size=(x, y1))
                Rectangle(pos=(posX + 100, posY), size=(x, y0))
                Rectangle(pos=(posX + 200, posY), size=(x, y2))
                Rectangle(pos=(posX + 300, posY), size=(x, y0))
                Rectangle(pos=(posX + 400, posY), size=(x, y3))
                Rectangle(pos=(posX + 500, posY), size=(x, y0))
                Rectangle(pos=(posX + 600, posY), size=(x, y4))
                Rectangle(pos=(posX + 700, posY), size=(x, y0))
                Rectangle(pos=(posX + 800, posY), size=(x, y5))
                Color(1, 1, 1, 1)
                #Rectangle(pos=(posX, posY), size=(1000, 2))
                Rectangle(pos=(posX, posY), size=(1, max_y))

class GraphWidgetForWeeks(Widget):
    def __init__(self, **kwargs):
        super(GraphWidgetForWeeks, self).__init__(**kwargs)

        with self.canvas:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.draw_box()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])


    def draw_box(self):
        size_window = Window.size
        window_x = size_window[0]
        window_y = size_window[1]
        pos_x = (window_x / 10) * 3.04
        pos_y = (window_y / 10) * 5.3
        posX = pos_x + 0
        posY = pos_y + 10

        if settings.role_id == "1":
            list_for_draw = settings.list_employee_for_weeks
        elif settings.role_id == "2":
            list_for_draw = settings.list_employee_for_weeks
        elif settings.role_id == "3":
            list_for_draw = settings.list_employee_for_weeks
        elif settings.role_id == "4":
            list_for_draw = settings.list_leader_for_weeks
        elif settings.role_id == "5":
            list_for_draw = settings.list_user_for_weeks

        final_list = []
        max_y = 350
        x = 100
        y0 = 0
        if len(list_for_draw) == 4:
            for i in list_for_draw:
                final_list.append(i * 2.85)
            y1 = max_y / 100 * final_list[0]
            y2 = max_y / 100 * final_list[1]
            y3 = max_y / 100 * final_list[2]
            y4 = max_y / 100 * final_list[3]

            with self.canvas.after:
                Color(.01, .66, .96, 1)
                Rectangle(pos=(posX, posY), size=(x, y1))
                Rectangle(pos=(posX + x*1, posY), size=(x, y0))
                Rectangle(pos=(posX + x*2, posY), size=(x, y2))
                Rectangle(pos=(posX + x*3, posY), size=(x, y0))
                Rectangle(pos=(posX + x*4, posY), size=(x, y3))
                Rectangle(pos=(posX + x*5, posY), size=(x, y0))
                Rectangle(pos=(posX + x*6, posY), size=(x, y4))
                Color(1, 1, 1, 1)
                #Rectangle(pos=(posX, posY), size=(x*8, 2))
                Rectangle(pos=(posX, posY), size=(1, max_y))

class GraphWidgetForMonths(Widget):
    def __init__(self, **kwargs):
        super(GraphWidgetForMonths, self).__init__(**kwargs)

        with self.canvas:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.draw_box()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])


    def draw_box(self):
        size_window = Window.size
        window_x = size_window[0]
        window_y = size_window[1]
        pos_x = (window_x / 10) * 3.04
        pos_y = (window_y / 10) * 5.3
        posX = pos_x + 0
        posY = pos_y + 10

        if settings.role_id == "1":
            list_for_draw = settings.list_employee_for_months
        elif settings.role_id == "2":
            list_for_draw = settings.list_employee_for_months
        elif settings.role_id == "3":
            list_for_draw = settings.list_employee_for_months
        elif settings.role_id == "4":
            list_for_draw = settings.list_leader_for_months
        elif settings.role_id == "5":
            list_for_draw = settings.list_user_for_months

        final_list = []
        max_y = 350
        x = 50
        y0 = 0
        if len(list_for_draw) == 12:
            for i in list_for_draw:
                final_list.append(i * 0.71)
            y1 = max_y / 100 * final_list[0]
            y2 = max_y / 100 * final_list[1]
            y3 = max_y / 100 * final_list[2]
            y4 = max_y / 100 * final_list[3]
            y5 = max_y / 100 * final_list[4]
            y6 = max_y / 100 * final_list[5]
            y7 = max_y / 100 * final_list[6]
            y8 = max_y / 100 * final_list[7]
            y9 = max_y / 100 * final_list[8]
            y10 = max_y / 100 * final_list[9]
            y11 = max_y / 100 * final_list[10]
            y12 = max_y / 100 * final_list[11]
            with self.canvas.after:
                Color(.01, .66, .96, 1)
                Rectangle(pos=(posX, posY), size=(x, y1))
                Rectangle(pos=(posX + x * 1, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 2, posY), size=(x, y2))
                Rectangle(pos=(posX + x * 3, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 4, posY), size=(x, y3))
                Rectangle(pos=(posX + x * 5, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 6, posY), size=(x, y4))
                Rectangle(pos=(posX + x * 7, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 8, posY), size=(x, y5))
                Rectangle(pos=(posX + x * 9, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 10, posY), size=(x, y6))
                Rectangle(pos=(posX + x * 11, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 12, posY), size=(x, y7))
                Rectangle(pos=(posX + x * 13, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 14, posY), size=(x, y8))
                Rectangle(pos=(posX + x * 15, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 16, posY), size=(x, y9))
                Rectangle(pos=(posX + x * 17, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 18, posY), size=(x, y10))
                Rectangle(pos=(posX + x * 19, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 20, posY), size=(x, y11))
                Rectangle(pos=(posX + x * 21, posY), size=(x, y0))
                Rectangle(pos=(posX + x * 22, posY), size=(x, y12))
                Color(1, 1, 1, 1)
                #Rectangle(pos=(posX, posY), size=(x*24, 2))
                Rectangle(pos=(posX, posY), size=(1, max_y))

class RegistrationPage(AnchorLayout):
    loadfile = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_page(self):
        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))

        self.box_layout_general_vertical = BoxLayout(orientation="vertical")
        self.box_layout_general_horizontal_up = BoxLayout(orientation="horizontal", padding=[20, 10])
        self.box_layout_general_horizontal_down = BoxLayout(orientation="horizontal", padding=[20, 10])

        self.box_layout_general_vertical_left = BoxLayout(orientation="vertical", size_hint=(.3, 1))
        self.box_layout_general_vertical_right = BoxLayout(orientation="vertical", size_hint=(.7, 1))

        self.box_layout_horizontal_left_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_vertical_left_up_side = BoxLayout(orientation="vertical", size_hint=(1, .45))

        self.box_layout_horizontal_right_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_horizontal_right_up_side = BoxLayout(orientation="horizontal", size_hint=(1, .45))

        self.page_admin_registration_down_side()
        self.page_admin_registration_right_up_side()
        self.up_menu_side()

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_left)  # Left general side
        self.box_layout_general_vertical_left.add_widget(self.box_layout_horizontal_left_up_menu)
        self.box_layout_general_vertical_left.add_widget(self.box_layout_vertical_left_up_side)

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_right)  # Right general side
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_menu)
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_side)

        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_up)
        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_down)

        self.add_widget(self.box_layout_general_vertical)

    def page_admin_registration_down_side(self):
        self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
        self.page_admin_registration_right_down_side()

    def page_admin_registration_right_down_side(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal", size_hint=[.7, 1], padding=[40, 0, 0, 0])
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_for_btn_vertical = BoxLayout(orientation="vertical", size_hint=[1, .7])
        box_for_btn_horizontal = BoxLayout(orientation="horizontal")

        box_vertical_section_1 = BoxLayout(orientation="vertical", spacing='10px')
        box_vertical_section_2 = BoxLayout(orientation="vertical", spacing='10px')

        box_sex = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_email = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_password = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_password_1 = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_phone_number = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_birthday_date = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50),
                                      padding=(0, 15, 0, 0))

        user_sex_lbl = Button(text="Sex", font_size=20, background_normal='button.png', background_down='button.png',
                              size_hint=[.3, 1])
        self.user_sex_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                        halign='center', font_size='20sp', multiline=False)

        user_email_lbl = Button(text="Email", font_size=20, background_normal='button.png',
                                background_down='button.png', size_hint=[.3, 1])
        self.user_email_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                          halign='center', font_size='20sp', multiline=False)

        user_password_lbl = Button(text="Password", font_size=20, background_normal='button.png',
                                   background_down='button.png', size_hint=[.3, 1])
        self.user_password_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                             halign='center', font_size='20sp', multiline=False, password=1)

        user_password_1_lbl = Button(text="Confirm password", font_size=20, background_normal='button.png',
                                   background_down='button.png', size_hint=[.3, 1])
        self.user_password_1_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                             halign='center', font_size='20sp', multiline=False, password=1)

        user_phone_number_lbl = Button(text="Phone number", font_size=20, background_normal='button.png',
                                       background_down='button.png', size_hint=[.3, 1])
        self.user_phone_number_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                                 halign='center', font_size='20sp', multiline=False)

        user_birthday_date_lbl = Button(text="Birthday date", font_size=20, background_normal='button.png',
                                        background_down='button.png', size_hint=[.3, 1])
        self.user_birthday_date_input = TextInput(text="1990-10-15", size_hint=[.5, 1],
                                                  background_color=[.92, .92, .92, .92], halign='center',
                                                  font_size='20sp', multiline=False)

        box_sex.add_widget(user_sex_lbl)
        box_sex.add_widget(self.user_sex_input)

        box_email.add_widget(user_email_lbl)
        box_email.add_widget(self.user_email_input)

        box_password.add_widget(user_password_lbl)
        box_password.add_widget(self.user_password_input)

        box_password_1.add_widget(user_password_1_lbl)
        box_password_1.add_widget(self.user_password_1_input)

        box_phone_number.add_widget(user_phone_number_lbl)
        box_phone_number.add_widget(self.user_phone_number_input)

        box_birthday_date.add_widget(user_birthday_date_lbl)
        box_birthday_date.add_widget(self.user_birthday_date_input)

        box_vertical_section_1.add_widget(box_sex)
        box_vertical_section_1.add_widget(box_email)
        box_vertical_section_1.add_widget(box_password)
        box_vertical_section_1.add_widget(box_password_1)
        box_vertical_section_1.add_widget(box_phone_number)
        box_vertical_section_1.add_widget(box_birthday_date)
        box_vertical_section_1.add_widget(Widget())

        registration_btn = Button(
            text='Register a user',
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        registration_btn.bind(on_release=lambda btn: self.registration_new_user())

        # record_face_btn = Button(
        #     text='Record face',
        #     font_size=30,
        #     background_normal='button.png',
        #     background_down='button_down.png',
        #     size_hint=[None, None],
        #     size=[270, 100],
        # )
        # record_face_btn.bind(on_release=lambda btn: self.record_face())

        back_btn = Button(
            text='Back',
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        back_btn.bind(on_release=lambda btn: self.load_general_page())

        box_for_btn_vertical.add_widget(back_btn)
        box_for_btn_vertical.add_widget(BoxLayout(size_hint=[1, .2]))
        #box_for_btn_vertical.add_widget(record_face_btn)
        box_for_btn_vertical.add_widget(BoxLayout(size_hint=[1, .2]))
        box_for_btn_vertical.add_widget(registration_btn)

        box_for_btn_horizontal.add_widget(BoxLayout(size_hint=[1, .5]))
        box_for_btn_horizontal.add_widget(box_for_btn_vertical)
        box_vertical_section_2.add_widget(box_for_btn_horizontal)

        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)

        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_general_horizontal_down.add_widget(box_vertical_section_b)

    def add_dataset_to_zip(self):
        path = 'dataset'
        list_paths = [os.path.join(path, f) for f in os.listdir(path)]
        if os._exists(settings.zip_name):
            os.remove(settings.zip_name)
        else:
            newzip = zipfile.ZipFile(settings.zip_name, 'w')
            for i in list_paths:
                newzip.write(i)
            newzip.close()

    def send_zip_to_server(self):
        url = 'http://' + settings.host + ':' + settings.port + '/file/upload-training-set'
        files = {
            'file': (settings.zip_name, open(settings.zip_name, 'rb')),
        }

        x = requests.post(url, files=files)

    def send_to_server(self, user_id):
        url = 'http://' + settings.host + ':' + settings.port + '/file/upload-user-picture'
        files = {
            'file': ('user_' + user_id + '.png', open('user_' + user_id + '.png', 'rb')),
        }

        x = requests.post(url, files=files)


    def page_admin_registration_right_up_side(self):
        self.select_avatar_for_new_user()
        self.page_admin_registration_right_side_section_b()

    def page_admin_registration_right_side_section_b(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal", padding=[40, 0, 0, 0])
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_vertical_section_1 = BoxLayout(orientation="vertical", spacing='10px')
        box_vertical_section_2 = BoxLayout(orientation="vertical", spacing='10px')

        box_name = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_surname = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_address = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_residence_country = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_nationality = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_role_id = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))

        user_name_lbl = Button(text="Name", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_name_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_surname_lbl = Button(text="Surname", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_surname_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_address_lbl = Button(text="Address", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_address_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_residence_country_lbl = Button(text="Residence country", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_rezidence_country_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_nationality_lbl = Button(text="Nationality", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_nationality_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)


        user_role_id_lbl = Button(text="Role id", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_role_id_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)


        box_name.add_widget(user_name_lbl)
        box_name.add_widget(self.user_name_input)

        box_surname.add_widget(user_surname_lbl)
        box_surname.add_widget(self.user_surname_input)

        box_address.add_widget(user_address_lbl)
        box_address.add_widget(self.user_address_input)

        box_residence_country.add_widget(user_residence_country_lbl)
        box_residence_country.add_widget(self.user_rezidence_country_input)

        box_nationality.add_widget(user_nationality_lbl)
        box_nationality.add_widget(self.user_nationality_input)


        box_role_id.add_widget(user_role_id_lbl)
        box_role_id.add_widget(self.user_role_id_input)


        box_vertical_section_1.add_widget(box_name)
        box_vertical_section_1.add_widget(box_surname)
        box_vertical_section_1.add_widget(box_address)
        box_vertical_section_1.add_widget(box_residence_country)
        box_vertical_section_1.add_widget(box_nationality)
        box_vertical_section_1.add_widget(box_role_id)



        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)


        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_section_b)

    def registration_new_user(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/admin/register-user'
        name = self.user_name_input.text
        surname = self.user_surname_input.text
        address = self.user_address_input.text
        rezidenceCountry = self.user_rezidence_country_input.text
        nationality = self.user_nationality_input.text
        sex = self.user_sex_input.text
        email = self.user_email_input.text
        password = self.user_password_input.text
        phoneNumber = self.user_phone_number_input.text
        birthdayDate = self.user_birthday_date_input.text
        roleId = self.user_role_id_input.text

        myobj = '{"name": "' + str(name) + '", "surname": "' + str(surname) + '", "address": "' + str(address) + '", "residencecountry": "' + str(rezidenceCountry) + '", "nationality": "' + str(nationality) + '", "sex": "' + str(sex) + '", "email": "' + str(email) + '", "password": "' + str(password) + '", "phonenumber": "' + str(phoneNumber) + '", "birthdaydate": "' + str(birthdayDate) + '", "roleid": "' + str(roleId) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        if x.status_code == 200:
            if os.path.isfile("C:/Users/wikto/PycharmProjects/EA/new_user_photo.png") == True:
                self.rename_and_send_avatar(email)
            #self.add_dataset_to_zip()
            #self.send_zip_to_server()
            #os.remove(settings.zip_name)
            #shutil.rmtree('dataset')
            self.load_general_page()
        else:
            print("Error: " + x.content)

    def rename_and_send_avatar(self, user_email):
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/check/' + str(user_email) + ''
        x = requests.get(url)
        if x.status_code == 200:
            print(x.content)
            s = json.loads(x.content)
            user_id = str(s["userid"])
            os.rename('new_user_photo.png', 'user_' + user_id + '.png')
            self.send_to_server(user_id)
            os.remove('user_' + user_id + '.png')
        else:
            print("Error: " + x.content)

    def select_avatar_for_new_user(self):
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .1], padding=[10, 10, 10, 0])
        if settings.new_user_photo == False:
            self.box_layout_vertical_left_up_side.add_widget(
                Image(source="user.png", size_hint=[1, .6]))
            # if os._exists('new_user_photo.png'):
            #     os.remove('new_user_photo.png')
        else:
            self.box_layout_vertical_left_up_side.add_widget(
                Image(source="new_user_photo.png", size_hint=[1, .6]))

        select_avatar_btn = Button(
            text="Select_photo",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[1, 1],

        )
        select_avatar_btn.bind(on_release=lambda btn: self.show_load())
        box_layout_for_btn.add_widget(select_avatar_btn)
        self.box_layout_vertical_left_up_side.add_widget(box_layout_for_btn)

    def up_menu_side(self):

        if settings.role_id == "2":
            self.calendar_left()
            self.box_layout_horizontal_right_up_menu.add_widget(Widget())
            self.menu_right()
        else:
            print("Wrong role_id")

    def menu_center(self):
        self.box_layout_search = BoxLayout(orientation="horizontal", padding=[20, 0, 0, 0])
        self.search_text = TextInput(text="Search", size_hint=[.7, .7],
                                     background_color=[.92, .92, .92, .92], halign='center', font_size='20sp',
                                     multiline=False)
        self.box_layout_search.add_widget(self.search_text)

        self.search_btn = Button(
            text="Go",
            font_size=30,
            on_press=self.search_btn_press,
            # background_color=[.13, .13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[.3, .7],
        )

        self.box_layout_search.add_widget(self.search_btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_search)

    def search_btn_press(self, instance):
        print("Search result")

    def menu_right(self):
        self.box_layout_menu_right = BoxLayout(orientation="horizontal")
        btn = Button(text='Registration',
                            font_size=30,
                            # background_color=[.13, .13, .13, .13],
                            background_normal='button.png',
                            # background_down='',
                            size_hint=[.7, .7],
                            )

        self.box_layout_menu_right.add_widget(Widget())
        self.box_layout_menu_right.add_widget(btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_right)

    def calendar_left(self):
        date = datetime.datetime.now().date()
        weekDay = datetime.datetime.now().weekday()
        self.box_layout_menu_left = BoxLayout(orientation="horizontal")
        btn = Button(text=str(date),
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     background_down='button.png',
                     size_hint=[1, .7],
                     )
        self.box_layout_menu_left.add_widget(btn)
        btn = Button(text=settings.get_name_week(str(weekDay)),
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     background_down='button.png',
                     size_hint=[1, .7],
                     )
        self.box_layout_menu_left.add_widget(btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_left)

    def load_general_page(self):
        settings.new_user_photo = False
        ea_app.screen_manager.current = "FirstPageUser"
        ea_app.first_page_user.show_page()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        imgPath = str(os.path.join(path, filename[0]))
        self.start_crop(imgPath)
        self.dismiss_popup()
        self.update_selected_photo()

    def update_selected_photo(self):
        self.box_layout_vertical_left_up_side.clear_widgets()
        settings.new_user_photo = True
        self.select_avatar_for_new_user()

    # Crop image and save
    def prepare_mask(self, size, antialias=2):
        mask = ImagePIL.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, ImagePIL.ANTIALIAS)

    def crop(self, im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0:
            im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0:
            im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, ImagePIL.ANTIALIAS)

    def start_crop(self, imgPath):
        size = (500, 500)
        im = ImagePIL.open(imgPath)
        im = self.crop(im, size)
        im.putalpha(self.prepare_mask(size, 4))
        im.save("new_user_photo.png")

    def record_face(self):
        if not os.path.exists('dataset'):
            os.makedirs('dataset')
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        uid = settings.selected_user_id
        sampleNum = 0
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/User." + str(uid) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.waitKey(100)
            cv2.imshow('img', img)
            cv2.waitKey(1);
            if sampleNum > 40:
                break
        cap.release()
        cv2.destroyAllWindows()

class UpdateUserPage(AnchorLayout):
    loadfile = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_page(self):
        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))

        self.box_layout_general_vertical = BoxLayout(orientation="vertical")
        self.box_layout_general_horizontal_up = BoxLayout(orientation="horizontal", padding=[20, 10])
        self.box_layout_general_horizontal_down = BoxLayout(orientation="horizontal", padding=[20, 10])

        self.box_layout_general_vertical_left = BoxLayout(orientation="vertical", size_hint=(.3, 1))
        self.box_layout_general_vertical_right = BoxLayout(orientation="vertical", size_hint=(.7, 1))

        self.box_layout_horizontal_left_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_vertical_left_up_side = BoxLayout(orientation="vertical", size_hint=(1, .45))

        self.box_layout_horizontal_right_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_horizontal_right_up_side = BoxLayout(orientation="horizontal", size_hint=(1, .45))

        self.select_avatar_for_new_user()
        self.page_admin_registration_down_side()
        self.page_admin_registration_right_up_side()
        self.up_menu_side()

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_left)  # Left general side
        self.box_layout_general_vertical_left.add_widget(self.box_layout_horizontal_left_up_menu)
        self.box_layout_general_vertical_left.add_widget(self.box_layout_vertical_left_up_side)

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_right)  # Right general side
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_menu)
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_side)

        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_up)
        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_down)

        self.add_widget(self.box_layout_general_vertical)

    def page_admin_registration_down_side(self):
        self.box_layout_general_horizontal_down.add_widget(BoxLayout(orientation="vertical", size_hint=[.3, 1]))
        self.page_admin_registration_right_down_side()

    def page_admin_registration_right_down_side(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal", size_hint=[.7, 1], padding=[40, 0, 0, 0])
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_for_btn_vertical = BoxLayout(orientation="vertical", size_hint=[1, .7])
        box_for_btn_horizontal = BoxLayout(orientation="horizontal")

        box_vertical_section_1 = BoxLayout(orientation="vertical", spacing='10px')
        box_vertical_section_2 = BoxLayout(orientation="vertical", spacing='10px')

        box_sex = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_email = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_password = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_phone_number = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_birthday_date = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50),
                                      padding=(0, 15, 0, 0))

        user_sex_lbl = Button(text="Sex", font_size=20, background_normal='button.png', background_down='button.png',
                              size_hint=[.3, 1])
        self.user_sex_input = TextInput(text=str(settings.selected_sex), size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                        halign='center', font_size='20sp', multiline=False)

        user_email_lbl = Button(text="Email", font_size=20, background_normal='button.png',
                                background_down='button.png', size_hint=[.3, 1])
        self.user_email_input = TextInput(text=settings.selected_user_email, size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                          halign='center', font_size='20sp', multiline=False)

        user_password_lbl = Button(text="Password", font_size=20, background_normal='button.png',
                                   background_down='button.png', size_hint=[.3, 1])
        self.user_password_input = TextInput(text="", size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                             halign='center', font_size='20sp', multiline=False)

        user_phone_number_lbl = Button(text="Phone number", font_size=20, background_normal='button.png',
                                       background_down='button.png', size_hint=[.3, 1])
        self.user_phone_number_input = TextInput(text=settings.selected_phone_number, size_hint=[.5, 1], background_color=[.92, .92, .92, .92],
                                                 halign='center', font_size='20sp', multiline=False)

        user_birthday_date_lbl = Button(text="Birthday date", font_size=20, background_normal='button.png',
                                        background_down='button.png', size_hint=[.3, 1])
        self.user_birthday_date_input = TextInput(text=str(settings.selected_birthday_date), size_hint=[.5, 1],
                                                  background_color=[.92, .92, .92, .92], halign='center',
                                                  font_size='20sp', multiline=False)

        box_sex.add_widget(user_sex_lbl)
        box_sex.add_widget(self.user_sex_input)

        box_email.add_widget(user_email_lbl)
        box_email.add_widget(self.user_email_input)

        box_password.add_widget(user_password_lbl)
        box_password.add_widget(self.user_password_input)

        box_phone_number.add_widget(user_phone_number_lbl)
        box_phone_number.add_widget(self.user_phone_number_input)

        box_birthday_date.add_widget(user_birthday_date_lbl)
        box_birthday_date.add_widget(self.user_birthday_date_input)

        box_vertical_section_1.add_widget(box_sex)
        box_vertical_section_1.add_widget(box_email)
        box_vertical_section_1.add_widget(box_password)
        box_vertical_section_1.add_widget(box_phone_number)
        box_vertical_section_1.add_widget(box_birthday_date)
        box_vertical_section_1.add_widget(Widget())

        registration_btn = Button(
            text="Update a user",
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        registration_btn.bind(on_release=lambda btn: self.update_info_user())

        record_face_btn = Button(
            text="Rerecord face",
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        record_face_btn.bind(on_release=lambda btn: self.record_face())

        back_btn = Button(
            text="Back",
            font_size=30,
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[None, None],
            size=[270, 100],
        )
        back_btn.bind(on_release=lambda btn: self.load_general_page())



        box_for_btn_vertical.add_widget(back_btn)
        box_for_btn_vertical.add_widget(BoxLayout(size_hint=[1, .2]))
        box_for_btn_vertical.add_widget(record_face_btn)
        box_for_btn_vertical.add_widget(BoxLayout(size_hint=[1, .2]))
        box_for_btn_vertical.add_widget(registration_btn)

        box_for_btn_horizontal.add_widget(BoxLayout(size_hint=[1, .5]))
        box_for_btn_horizontal.add_widget(box_for_btn_vertical)
        box_vertical_section_2.add_widget(box_for_btn_horizontal)

        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)

        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_general_horizontal_down.add_widget(box_vertical_section_b)

    def page_admin_registration_right_side_section_b(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal", padding=[40, 0, 0, 0])
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_vertical_section_1 = BoxLayout(orientation="vertical", spacing='10px')
        box_vertical_section_2 = BoxLayout(orientation="vertical", spacing='10px')

        box_name = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_surname = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_address = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_residence_country = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_nationality = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))
        box_role_id = BoxLayout(orientation="horizontal", size_hint=[1, None], size=(0, 50), padding=(0, 15, 0, 0))

        user_name_lbl = Button(text="Name", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_name_input = TextInput(text=settings.selected_user_name, size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_surname_lbl = Button(text="Surname", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_surname_input = TextInput(text=settings.selected_user_surname, size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_address_lbl = Button(text="Address", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_address_input = TextInput(text=settings.selected_user_address, size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_residence_country_lbl = Button(text="Residence country", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_rezidence_country_input = TextInput(text=settings.selected_residence_country, size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)

        user_nationality_lbl = Button(text="Nationality", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_nationality_input = TextInput(text=settings.selected_nationality, size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)


        user_role_id_lbl = Button(text="Role id", font_size=20,  background_normal='button.png', background_down='button.png',  size_hint=[.3, 1])
        self.user_role_id_input = TextInput(text=str(settings.selected_role_id), size_hint=[.5, 1], background_color=[.92, .92, .92, .92], halign='center', font_size='20sp', multiline=False)


        box_name.add_widget(user_name_lbl)
        box_name.add_widget(self.user_name_input)

        box_surname.add_widget(user_surname_lbl)
        box_surname.add_widget(self.user_surname_input)

        box_address.add_widget(user_address_lbl)
        box_address.add_widget(self.user_address_input)

        box_residence_country.add_widget(user_residence_country_lbl)
        box_residence_country.add_widget(self.user_rezidence_country_input)

        box_nationality.add_widget(user_nationality_lbl)
        box_nationality.add_widget(self.user_nationality_input)


        box_role_id.add_widget(user_role_id_lbl)
        box_role_id.add_widget(self.user_role_id_input)


        box_vertical_section_1.add_widget(box_name)
        box_vertical_section_1.add_widget(box_surname)
        box_vertical_section_1.add_widget(box_address)
        box_vertical_section_1.add_widget(box_residence_country)
        box_vertical_section_1.add_widget(box_nationality)
        box_vertical_section_1.add_widget(box_role_id)



        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)


        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_section_b)

    def select_avatar_for_new_user(self):
        self.box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .1], padding=[10, 10, 10, 0])

        url = 'http://' + settings.host + ':' + settings.port + '/file/user-picture/' + 'user_' + str(
            settings.selected_user_id) + '.png'
        x = requests.get(url)
        if settings.new_user_photo == False:
            if x.status_code == 200:
                self.box_layout_vertical_left_up_side.add_widget(
                    AsyncImage(source=url, size_hint=[1, .6]))
                # if os._exists('new_user_photo.png'):
                #     os.remove('new_user_photo.png')
            else:
                self.box_layout_vertical_left_up_side.add_widget(Image(source="user.png", size_hint=[1, .6]))
                os.remove('new_user_photo.png')
        else:
            self.box_layout_vertical_left_up_side.add_widget(
                Image(source="new_user_photo.png", size_hint=[1, .6]))



        select_avatar_btn = Button(
            text="Select_photo",
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[1, 1],
            size=[270, 100],
        )
        select_avatar_btn.bind(on_release=lambda btn: self.show_load())
        self.box_layout_for_btn.add_widget(select_avatar_btn)
        self.box_layout_vertical_left_up_side.add_widget(self.box_layout_for_btn)

    def page_admin_registration_right_up_side(self):
        self.page_admin_registration_right_side_section_b()

    def update_info_user(self):
        url = 'http://' + settings.host + ':' + settings.port + '/api/admin/update-user-data'
        name = self.user_name_input.text
        userid = settings.selected_user_id
        surname = self.user_surname_input.text
        address = self.user_address_input.text
        rezidenceCountry = self.user_rezidence_country_input.text
        nationality = self.user_nationality_input.text
        sex = self.user_sex_input.text
        email = self.user_email_input.text
        password = self.user_password_input.text
        phoneNumber = self.user_phone_number_input.text
        birthdayDate = self.user_birthday_date_input.text
        roleId = self.user_role_id_input.text

        myobj = '{"userid": "' + str(userid) + '", "name": "' + str(name) + '", "surname": "' + str(surname) + '", "address": "' + str(address) + '", "residencecountry": "' + str(rezidenceCountry) + '", "nationality": "' + str(nationality) + '", "sex": "' + str(sex) + '", "email": "' + str(email) + '", "password": "' + str(password) + '", "phonenumber": "' + str(phoneNumber) + '", "birthdaydate": "' + str(birthdayDate) + '", "roleid": "' + str(roleId) + '"}'
        print(myobj)
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        print(x.content)
        if x.status_code == 200:
            if os._exists('new_user_photo.png'):
                self.rename_and_save_avatar(email)
            self.add_dataset_to_zip()
            self.send_zip_to_server()
            os.remove(settings.zip_name)
            shutil.rmtree('dataset')
            self.load_general_page()
        else:
            print(x.content)

    def add_dataset_to_zip(self):
        path = 'dataset'
        list_paths = [os.path.join(path, f) for f in os.listdir(path)]
        if os._exists(settings.zip_name):
            os.remove(settings.zip_name)
        else:
            newzip = zipfile.ZipFile(settings.zip_name, 'w')
            for i in list_paths:
                newzip.write(i)
            newzip.close()

    def send_zip_to_server(self):
        url = 'http://' + settings.host + ':' + settings.port + '/file/upload-training-set'
        files = {
            'file': (settings.zip_name, open(settings.zip_name, 'rb')),
        }

        x = requests.post(url, files=files)

    def send_to_server(self, user_id):
        url = 'http://' + settings.host + ':' + settings.port + '/file/upload-user-picture'
        files = {
            'file': ('user_' + user_id + '.png', open('user_' + user_id + '.png', 'rb')),
        }

        x = requests.post(url, files=files)

        if x.status_code == 200:
            print("On server:")
        else:
            print("Error: " + x.content)

    def rename_and_save_avatar(self, user_email):
        url = 'http://' + settings.host + ':' + settings.port + '/api/user/check/' + str(user_email) + ''
        x = requests.get(url)
        if x.status_code == 200:
            print(x.content)
            s = json.loads(x.content)
            user_id = str(s["userid"])
            os.rename('new_user_photo.png', 'user_' + user_id + '.png')
            self.send_to_server(user_id)
            os.remove('user_' + user_id + '.png')
        else:
            print("Error: " + x.content)

    def up_menu_side(self):

        if settings.role_id == "2":
            self.calendar_left()
            self.box_layout_horizontal_right_up_menu.add_widget(Widget())
            self.menu_right()
        else:
            print("Wrong role_id")

    def menu_center(self):
        self.box_layout_search = BoxLayout(orientation="horizontal", padding=[20, 0, 0, 0])
        self.search_text = TextInput(text="Search", size_hint=[.7, .7],
                                     background_color=[.92, .92, .92, .92], halign='center', font_size='20sp',
                                     multiline=False)
        self.box_layout_search.add_widget(self.search_text)

        self.search_btn = Button(
            text="Go",
            font_size=30,
            on_press=self.search_btn_press,
            # background_color=[.13, .13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[.3, .7],
        )

        self.box_layout_search.add_widget(self.search_btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_search)

    def search_btn_press(self, instance):
        print("Search result")

    def menu_right(self):
        self.box_layout_menu_right = BoxLayout(orientation="horizontal")
        btn = Button(text='Registration',
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     # background_down='',
                     size_hint=[.7, .7],
                     )

        self.box_layout_menu_right.add_widget(Widget())
        self.box_layout_menu_right.add_widget(btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_right)

    def calendar_left(self):
        date = datetime.datetime.now().date()
        weekDay = datetime.datetime.now().weekday()
        self.box_layout_menu_left = BoxLayout(orientation="horizontal")
        btn = Button(text=str(date),
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     background_down='button.png',
                     size_hint=[1, .7],
                     )
        self.box_layout_menu_left.add_widget(btn)
        btn = Button(text=settings.get_name_week(str(weekDay)),
                     font_size=30,
                     # background_color=[.13, .13, .13, .13],
                     background_normal='button.png',
                     background_down='button.png',
                     size_hint=[1, .7],
                     )
        self.box_layout_menu_left.add_widget(btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_left)

    def load_general_page(self):
        settings.new_user_photo = False
        ea_app.screen_manager.current = "FirstPageUser"
        ea_app.first_page_user.show_page()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        imgPath = str(os.path.join(path, filename[0]))
        self.start_crop(imgPath)
        self.dismiss_popup()

    def update_selected_photo(self):
        self.box_layout_vertical_left_up_side.clear_widgets()
        settings.new_user_photo = True
        self.select_avatar_for_new_user()
        print("update")

    # Crop image and save
    def prepare_mask(self, size, antialias=2):
        mask = ImagePIL.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, ImagePIL.ANTIALIAS)

    def crop(self, im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0:
            im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0:
            im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, ImagePIL.ANTIALIAS)

    def start_crop(self, imgPath):
        size = (500, 500)
        im = ImagePIL.open(imgPath)
        im = self.crop(im, size)
        im.putalpha(self.prepare_mask(size, 4))
        im.save("new_user_photo.png")
        self.update_selected_photo()


    def record_face(self):
        if not os.path.exists('dataset'):
            os.makedirs('dataset')
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        uid = settings.selected_user_id
        sampleNum = 0
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/User." + str(uid) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.waitKey(100)
            cv2.imshow('img', img)
            cv2.waitKey(1);
            if sampleNum > 40:
                break
        cap.release()
        cv2.destroyAllWindows()

class ShowUserInfo(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_page(self):
        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))

        self.box_layout_general_vertical = BoxLayout(orientation="vertical")
        self.box_layout_general_horizontal_up = BoxLayout(orientation="horizontal", padding=[20, 10])
        self.box_layout_general_horizontal_down = BoxLayout(orientation="horizontal", padding=[20, 10])

        self.box_layout_general_vertical_left = BoxLayout(orientation="vertical", size_hint=(.3, 1))
        self.box_layout_general_vertical_right = BoxLayout(orientation="vertical", size_hint=(.7, 1))

        self.box_layout_horizontal_left_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_vertical_left_up_side = BoxLayout(orientation="vertical", size_hint=(1, .45))

        self.box_layout_horizontal_right_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_horizontal_right_up_side = BoxLayout(orientation="horizontal", size_hint=(1, .45))

        self.page_admin_registration_down_side()
        self.page_admin_registration_right_up_side()
        self.up_menu_side()

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_left)  # Left general side
        self.box_layout_general_vertical_left.add_widget(self.box_layout_horizontal_left_up_menu)
        self.box_layout_general_vertical_left.add_widget(self.box_layout_vertical_left_up_side)

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_right)  # Right general side
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_menu)
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_side)

        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_up)
        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_down)

        self.add_widget(self.box_layout_general_vertical)

class Group_info(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_page(self):
        size_window = Window.size
        self.canvas.add(Color(.13, .13, .13, ))
        self.canvas.add(Rectangle(size=size_window))

        self.box_layout_general_vertical = BoxLayout(orientation="vertical")
        self.box_layout_general_horizontal_up = BoxLayout(orientation="horizontal", padding=[20, 10])
        self.box_layout_general_horizontal_down = BoxLayout(orientation="horizontal", padding=[20, 10])

        self.box_layout_general_vertical_left = BoxLayout(orientation="vertical", size_hint=(.3, 1))
        self.box_layout_general_vertical_right = BoxLayout(orientation="vertical", size_hint=(.7, 1))

        self.box_layout_horizontal_left_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_vertical_left_up_side = BoxLayout(orientation="vertical", size_hint=(1, .45))

        self.box_layout_horizontal_right_up_menu = BoxLayout(orientation="horizontal", size_hint=(1, .05))
        self.box_layout_horizontal_right_up_side = BoxLayout(orientation="horizontal", size_hint=(1, .45))

        self.page_all_avatar()
        self.page_1_admin_down_side()
        self.page_1_project_manager_section_a()
        self.page_1_project_manager_section_b()
        self.up_menu_side()


        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_left)  # Left general side
        self.box_layout_general_vertical_left.add_widget(self.box_layout_horizontal_left_up_menu)
        self.box_layout_general_vertical_left.add_widget(self.box_layout_vertical_left_up_side)

        self.box_layout_general_horizontal_up.add_widget(self.box_layout_general_vertical_right)  # Right general side
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_menu)
        self.box_layout_general_vertical_right.add_widget(self.box_layout_horizontal_right_up_side)

        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_up)
        self.box_layout_general_vertical.add_widget(self.box_layout_general_horizontal_down)

        self.add_widget(self.box_layout_general_vertical)


    def page_all_avatar(self):
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .1], padding=[10, 10, 10, 0])
        self.role_lbl = Label(text="", text_size=self.size, valign="middle", size_hint=[0, 1], halign='left',
                              font_size='15sp')
        self.box_layout_horizontal_left_up_menu.add_widget(self.role_lbl)

        url = 'http://' + settings.host + ':' + settings.port + '/file/user-picture/' + 'user_' + settings.user_id + '.png'
        x = requests.get(url)
        if x.status_code == 200:
            self.box_layout_vertical_left_up_side.add_widget(
                AsyncImage(source=url, size_hint=[1, .6]))
        else:
            self.box_layout_vertical_left_up_side.add_widget(Image(source="user.png", size_hint=[1, .6]))

        nam = settings.name + '  ' + settings.surname
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        self.box_layout_vertical_left_up_side.add_widget(box_layout_for_btn)
        self.page_all_role()

    def page_1_admin_down_side(self):
        self.admin_load_all_users()
        bx_vertical_down_right_side = BoxLayout(orientation="vertical", size_hint=[1, 1])
        bx_header = BoxLayout(orientation="horizontal", size_hint=[1, .07])
        bx_content = BoxLayout(orientation="horizontal", size_hint=[1, .93])
        bx_header.add_widget(Button(text="Id", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Name", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Surname", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Registration date", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        bx_header.add_widget(Button(text="Email", size_hint=[1, None], size=[0, 40], font_size=30,
                                    background_color=(0, 0, 0, 1), background_normal=''))
        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(1, None), width=500)


        layout.bind(minimum_height=layout.setter('height'))

        self.test = []

        for i in range(len(settings.list_of_users)):
            item = settings.list_of_users[i]
            if settings.user_id != str(item["userid"]):
                bx_item = BoxLayout(orientation="horizontal", size=(0, 40),
                                    size_hint=(1, None))


                btn = Button(text=str(item["userid"]), on_press=self.change_to_selected_user, font_size=25,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')
                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["name"]), on_press=self.change_to_selected_user, font_size=25,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')
                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["surname"]), on_press=self.change_to_selected_user, font_size=25,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')

                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["registrationdate"].split('T')[0]), font_size=25, on_press=self.change_to_selected_user,
                             id=str(item["email"].split('T')[0]),
                             background_color=(.01, .66, .96, 1), background_normal='')
                self.test.append(btn)
                bx_item.add_widget(btn)
                btn = Button(text=str(item["email"]), font_size=25, on_press=self.change_to_selected_user,
                             id=str(item["email"]),
                             background_color=(.01, .66, .96, 1), background_normal='')

                self.test.append(btn)
                bx_item.add_widget(btn)
                layout.add_widget(bx_item)


        root = ScrollView(size_hint=(1, 1),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        bx_content.add_widget(root)

        bx_vertical_down_right_side.add_widget(bx_header)
        bx_vertical_down_right_side.add_widget(bx_content)

        self.change_color_selecter()
        self.box_layout_general_horizontal_down.add_widget(bx_vertical_down_right_side)


    def page_1_project_manager_section_a(self):
        box_project_manager_vertical_section_a = BoxLayout(orientation="vertical", size_hint=[.5, 1], padding=[0, 0, 0, 0])
        box_layout_for_btn = BoxLayout(orientation="horizontal", size_hint=[1, .28], padding=[10, 10, 10, 0])

        if os.path.isfile("C:/Users/wikto/PycharmProjects/EA/user_" + str(settings.pm_selected_group_id) + ".png") == False:
            box_project_manager_vertical_section_a.add_widget(Widget())
            box_project_manager_vertical_section_a.add_widget(
                Image(source="user.png", size_hint=[1, .8]))
        else:
            box_project_manager_vertical_section_a.add_widget(Widget())
            box_project_manager_vertical_section_a.add_widget(
                Image(source="user_" + str(settings.selected_user_id) + ".png", size_hint=[1, .8]))
        nam = settings.pm_selected_group_leader_name + "  " + settings.pm_selected_group_leader_surname
        name_surname_btn = Button(
            text=nam,
            font_size=30,
            # on_press=self.no_btn_press,
            # background_color=[.13, .13, .13],
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
            size=[270, 100],
        )
        box_layout_for_btn.add_widget(name_surname_btn)
        box_project_manager_vertical_section_a.add_widget(box_layout_for_btn)
        self.box_layout_horizontal_right_up_side.add_widget(box_project_manager_vertical_section_a)

    def page_1_project_manager_section_b(self):
        box_vertical_section_b = BoxLayout(orientation="horizontal")
        box_horizontal_section = BoxLayout(orientation="horizontal")
        box_vertical_section_1 = BoxLayout(orientation="vertical", size_hint=[.5, 1])
        box_vertical_section_2 = BoxLayout(orientation="vertical", size_hint=[.5, 1])

        group_name_btn = Button(
            text="Name of group",
            font_size=30,
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, None],
            size=[0, 100],
        )
        box_vertical_section_1.add_widget(BoxLayout(size_hint=[1, .3]))
        box_vertical_section_1.add_widget(group_name_btn)
        box_vertical_section_1.add_widget(BoxLayout(size_hint=[1, .1]))
        group_description_btn = Button(
            text="Description",
            font_size=30,
            background_normal='button.png',
            background_down='button.png',
            size_hint=[1, 1],
        )

        box_vertical_section_1.add_widget(group_description_btn)

        group_name_btn = Button(
            text=settings.pm_selected_group_name,
            font_size=30,
            background_color=(.01, .66, .96, 1),
            background_normal='',
            size_hint=[1, None],
            size=[0, 100],
        )
        box_vertical_section_2.add_widget(BoxLayout(size_hint=[1, .3]))
        box_vertical_section_2.add_widget(group_name_btn)
        box_vertical_section_2.add_widget(BoxLayout(size_hint=[1, .1]))
        group_description_btn = Button(
            text=settings.pm_selected_group_description,
            font_size=30,
            # on_press=self.no_btn_press,
            background_color=(.01, .66, .96, 1),
            background_normal='',
            # background_down='button.png',
            size_hint=[1, 1],

        )

        box_vertical_section_2.add_widget(group_description_btn)

        box_horizontal_section.add_widget(box_vertical_section_1)
        box_horizontal_section.add_widget(box_vertical_section_2)

        box_vertical_section_b.add_widget(box_horizontal_section)
        self.box_layout_horizontal_right_up_side.add_widget(box_vertical_section_b)

    def up_menu_side(self):
        self.calendar_left()
        self.menu_center()
        self.menu_right()

    def menu_center(self):
        self.box_layout_search = BoxLayout(orientation="horizontal", padding=[20, 0, 0, 0])
        self.search_text = TextInput(text="Search", size_hint=[.7, .7],
                                     background_color=[.92, .92, .92, .92], halign='center', font_size='20sp',
                                     multiline=False)
        self.box_layout_search.add_widget(self.search_text)

        self.search_btn = Button(
            text="Go",
            font_size=30,
            on_press=self.search_btn_press,
            # background_color=[.13, .13, .13, .13],
            background_normal='button.png',
            background_down='button_down.png',
            size_hint=[.3, .7],
        )

        self.box_layout_search.add_widget(self.search_btn)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_search)

    def search_btn_press(self, instance):
        print("Search result")

    def menu_right(self):
        self.box_layout_menu_right = BoxLayout(orientation="horizontal")
        self.dropdown = DropDown()
        for index in range(5):
            if index == 0:
                name_of_page = 'General'
            elif index == 1:
                name_of_page = 'Days'
            elif index == 2:
                name_of_page = 'Weeks'
            elif index == 3:
                name_of_page = 'Months'
            elif index == 4:
                name_of_page = 'Years'

            self.dropdownButton= Button(text=name_of_page, size_hint_y=None, height=44,
                         font_size=30,
                         background_color=[0, 0, 0, .8],
                         #background_normal='button.png',
                         background_down='button_down.png',
                         size_hint=[1, None],
                         )
            self.dropdownButton.bind(on_release=lambda dropdownButton: self.dropdown.select(dropdownButton.text))
            if index == 0:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_first())
            elif index == 1:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_second())
            elif index == 2:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_third())
            elif index == 3:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_fourth())
            elif index == 4:
                self.dropdownButton.bind(on_release=lambda dropdownButton: self.page_fifth())

            self.dropdown.add_widget(self.dropdownButton)

        mainbutton = Button(text='General',
                            font_size=30,
                            #background_color=[.13, .13, .13, .13],
                            background_normal='button_menu.png',
                            background_down='button_down.png',
                            size_hint=[.7, .7],
                            )

        mainbutton.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.box_layout_menu_right.add_widget(Widget())
        self.box_layout_menu_right.add_widget(mainbutton)
        self.box_layout_horizontal_right_up_menu.add_widget(self.box_layout_menu_right)

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

        self.first_page_user = GeneralPage()
        screen = Screen(name="FirstPageUser")
        screen.add_widget(self.first_page_user)
        self.screen_manager.add_widget(screen)

        self.registration_page = RegistrationPage()
        screen = Screen(name="RegistrationPage")
        screen.add_widget(self.registration_page)
        self.screen_manager.add_widget(screen)

        self.update_user_page = UpdateUserPage()
        screen = Screen(name="UpdateUserPage")
        screen.add_widget(self.update_user_page)
        self.screen_manager.add_widget(screen)

        self.show_user_info_page = ShowUserInfo()
        screen = Screen(name="ShowUserInfoPage")
        screen.add_widget(self.show_user_info_page)
        self.screen_manager.add_widget(screen)

        self.group_info_page = Group_info()
        screen = Screen(name="UpdateUserPage")
        screen.add_widget(self.group_info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":
    ea_app = EmployeeAdvisor()
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    ea_app.run()
