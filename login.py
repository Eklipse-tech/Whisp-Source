from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
import requests
import threading

# CONFIG
SERVER_URL = "https://malika-idioblastic-shawnda.ngrok-free.dev/login"
LOGO_URL = "https://github.com/Eklipse-tech/Whisp-Source/blob/main/assets/pixel_ghost.png?raw=true"
BG_COLOR = (0.08, 0.11, 0.18, 1)
ACCENT_COLOR = (0.2, 0.6, 1.0, 1)
INPUT_BG = (0.18, 0.22, 0.30, 1)
TEXT_COLOR = (1, 1, 1, 1)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(*BG_COLOR)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self.update_bg, size=self.update_bg)

        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.add_widget(anchor)

        card = BoxLayout(orientation='vertical', padding=[dp(25),dp(30),dp(25),dp(30)], 
                         spacing=dp(15), size_hint=(None, None), width=dp(320), height=dp(460))

        # Logo
        logo = AsyncImage(source=LOGO_URL, size_hint=(1, None), height=dp(80), allow_stretch=True, keep_ratio=True)
        logo.bind(texture=self.make_sharp)
        card.add_widget(logo)

        self.status = Label(text="", font_size='16sp', color=(1,1,0,1), size_hint=(1,None), height=dp(30))
        card.add_widget(self.status)

        self.user_in, u_box = self.create_input("Username")
        self.pass_in, p_box = self.create_input("Password", True)
        card.add_widget(u_box)
        card.add_widget(p_box)

        card.add_widget(Label(size_hint=(1, None), height=dp(10)))

        self.btn = Button(text="ENTER", background_color=(0,0,0,0), font_size='18sp', bold=True, size_hint=(1, None), height=dp(55))
        with self.btn.canvas.before:
            Color(*ACCENT_COLOR)
            self.btn.rect = RoundedRectangle(pos=self.btn.pos, size=self.btn.size, radius=[28])
        self.btn.bind(pos=self.update_btn, size=self.update_btn)
        self.btn.bind(on_release=self.attempt_login)
        card.add_widget(self.btn)
        
        anchor.add_widget(card)

    def create_input(self, hint, is_pwd=False):
        stack = FloatLayout(size_hint=(1, None), height=dp(55))
        bg = Widget(size_hint=(1, 1))
        with bg.canvas.before:
            Color(*INPUT_BG)
            bg.rect = RoundedRectangle(radius=[15])
        bg.bind(pos=lambda i,v: setattr(i.rect, 'pos', i.pos), size=lambda i,v: setattr(i.rect, 'size', i.size))
        stack.add_widget(bg)
        
        inp = TextInput(hint_text=hint, password=is_pwd, multiline=False, background_color=(0,0,0,0), 
                        foreground_color=TEXT_COLOR, cursor_color=ACCENT_COLOR, font_size='16sp',
                        padding=[dp(15), dp(15), dp(15), 0])
        stack.add_widget(inp)
        return inp, stack

    def attempt_login(self, instance):
        u = self.user_in.text
        p = self.pass_in.text
        self.status.text = "Connecting..."
        self.btn.disabled = True
        threading.Thread(target=self.do_login, args=(u,p)).start()

    def do_login(self, u, p):
        try:
            headers = {"ngrok-skip-browser-warning": "true"}
            resp = requests.post(SERVER_URL, json={"username":u, "password":p}, headers=headers, timeout=5)
            if resp.status_code == 200:
                Clock.schedule_once(self.success, 0)
            else:
                Clock.schedule_once(lambda dt: self.fail("Access Denied"), 0)
        except:
            Clock.schedule_once(lambda dt: self.fail("Offline"), 0)

    def success(self, dt):
        self.status.text = "SUCCESS"
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'home'
        self.btn.disabled = False

    def fail(self, msg):
        self.status.text = msg
        self.status.color = (1, 0, 0, 1)
        self.btn.disabled = False
        
    def update_bg(self, i, v): self.bg.pos = i.pos; self.bg.size = i.size
    def update_btn(self, i, v): self.btn.rect.pos = i.pos; self.btn.rect.size = i.size
    def make_sharp(self, i, t): 
        if t: t.mag_filter = 'nearest'; t.min_filter = 'nearest'
