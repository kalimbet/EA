from kivy.app import App
from kivy.uix.button import Button
import requests



def regUser():
    url = 'http://localhost:3000/api/register-user'
    myobj = "{\"username\": \"John\", \"pass\": \"12345\", \"role\": \"User\", \"description\": \"test record\"}"
    headers = {'Content-type': 'application/json'}
    requests.post(url, data=myobj, headers = headers)

def logUser():
    url = 'http://localhost:3000/api/login'
    myobj = "{\"username\": \"John\", \"pass\": \"12345\"}"
    headers = {'Content-type': 'application/json'}
    x = requests.post(url, data=myobj, headers = headers)

    print(x.content)

class MyApp(App):
    def build(self):
        return Button(text= "Registration",
                      font_size = 24,
                      on_press = self.btn_press,
                      background_color = [1,0,0,1],
                      background_normal = "")
    def btn_press(self, instance):
        instance.text = "Result"
        regUser()
        #logUser()
if __name__ == "__main__":
    MyApp().run()