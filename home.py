from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1) # Dark Black
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Center Text
        layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.lbl = Label(text="WELCOME HOME", font_size='30sp', color=(0.2, 0.6, 1.0, 1))
        layout.add_widget(self.lbl)
        self.add_widget(layout)

        # Logout Button
        btn = Button(text="LOGOUT", size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'center_x':0.5, 'y':0.1})
        with btn.canvas.before:
             Color(1, 0.3, 0.3, 1) # Red
             btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10])
        btn.bind(pos=lambda i,v: setattr(i.rect, 'pos', i.pos), size=lambda i,v: setattr(i.rect, 'size', i.size))
        btn.bind(on_release=self.logout)
        self.add_widget(btn)

    def update_bg(self, i, v):
        self.bg.pos = i.pos
        self.bg.size = i.size

    def logout(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'
