from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
import requests
import threading

# CONFIG (Same Ngrok Link)
SERVER_URL = "https://malika-idioblastic-shawnda.ngrok-free.dev" # <--- No /login here, just base URL

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 1. Dark Background
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 2. Main Layout (Vertical)
        root = BoxLayout(orientation='vertical')
        
        # --- HEADER ---
        header = BoxLayout(size_hint=(1, None), height=dp(60), padding=[dp(20),0,dp(20),0])
        lbl = Label(text="Whisp Feed", font_size='24sp', bold=True, color=(0.2, 0.6, 1.0, 1), halign='left', valign='middle')
        lbl.bind(size=lambda i,v: setattr(i, 'text_size', i.size)) # Align text left
        header.add_widget(lbl)
        
        # Refresh Button
        refresh_btn = Button(text="R", size_hint=(None, None), size=(dp(40), dp(40)), pos_hint={'center_y': 0.5})
        refresh_btn.bind(on_release=self.refresh_feed)
        header.add_widget(refresh_btn)
        
        root.add_widget(header)

        # --- SCROLLABLE FEED ---
        self.scroll = ScrollView(size_hint=(1, 1), bar_width=dp(5))
        
        # The Container for posts (Grows vertically)
        self.feed_container = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(15), padding=[dp(15), dp(10)])
        self.feed_container.bind(minimum_height=self.feed_container.setter('height')) # Magic line: allows scrolling
        
        self.scroll.add_widget(self.feed_container)
        root.add_widget(self.scroll)

        # --- FOOTER (Logout) ---
        footer = FloatLayout(size_hint=(1, None), height=dp(60))
        btn = Button(text="LOGOUT", size_hint=(None, None), size=(dp(100), dp(40)), pos_hint={'center_x':0.5, 'center_y':0.5})
        with btn.canvas.before:
             Color(0.2, 0.2, 0.2, 1)
             btn.rect = RoundedRectangle(radius=[10])
        btn.bind(pos=lambda i,v: setattr(i.rect, 'pos', i.pos), size=lambda i,v: setattr(i.rect, 'size', i.size))
        btn.bind(on_release=self.logout)
        footer.add_widget(btn)
        root.add_widget(footer)

        self.add_widget(root)

    def on_enter(self):
        # Auto-load feed when screen appears
        self.refresh_feed(None)

    def refresh_feed(self, instance):
        # Clear old posts
        self.feed_container.clear_widgets()
        loading = Label(text="Loading...", size_hint=(1, None), height=dp(50), color=(0.5,0.5,0.5,1))
        self.feed_container.add_widget(loading)
        
        threading.Thread(target=self.fetch_data).start()

    def fetch_data(self):
        try:
            # Note: We hit /feed now
            headers = {"ngrok-skip-browser-warning": "true"}
            resp = requests.get(f"{SERVER_URL}/feed", headers=headers, timeout=5)
            if resp.status_code == 200:
                posts = resp.json()
                Clock.schedule_once(lambda dt: self.populate_feed(posts), 0)
            else:
                Clock.schedule_once(lambda dt: self.show_error("Feed Error"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(f"Offline: {e}"), 0)

    def populate_feed(self, posts):
        self.feed_container.clear_widgets()
        for post in posts:
            self.add_post_card(post)

    def add_post_card(self, post):
        # CARD BOX
        card = BoxLayout(orientation='vertical', size_hint=(1, None), padding=dp(15), spacing=dp(5))
        
        # Background for Card
        with card.canvas.before:
            Color(0.12, 0.14, 0.18, 1) # Dark Slate
            RoundedRectangle(pos=card.pos, size=card.size, radius=[15])
        
        # This trick ensures the background moves with the card when scrolling
        def update_card_bg(inst, val):
            inst.canvas.before.children[1].pos = inst.pos
            inst.canvas.before.children[1].size = inst.size
        card.bind(pos=update_card_bg, size=update_card_bg)

        # 1. USERNAME (Blue)
        top_line = BoxLayout(size_hint=(1, None), height=dp(25))
        user_lbl = Label(text=f"@{post['user']}", color=(0.2, 0.6, 1.0, 1), bold=True, font_size='16sp', halign='left')
        user_lbl.bind(size=lambda i,v: setattr(i, 'text_size', i.size))
        
        time_lbl = Label(text=post['time'], color=(0.5, 0.5, 0.5, 1), font_size='12sp', halign='right')
        time_lbl.bind(size=lambda i,v: setattr(i, 'text_size', i.size))
        
        top_line.add_widget(user_lbl)
        top_line.add_widget(time_lbl)
        card.add_widget(top_line)

        # 2. CONTENT (White)
        content_lbl = Label(
            text=post['content'], 
            color=(1, 1, 1, 1), 
            font_size='15sp',
            size_hint=(1, None),
            valign='top'
        )
        # Auto-height for text:
        content_lbl.bind(width=lambda *x: content_lbl.setter('text_size')(content_lbl, (content_lbl.width, None)))
        content_lbl.bind(texture_size=lambda *x: content_lbl.setter('height')(content_lbl, content_lbl.texture_size[1]))
        
        card.add_widget(content_lbl)
        
        # Set card height based on text height + padding
        # We start with a base height (60) and add the text height
        def resize_card(*args):
            card.height = content_lbl.height + dp(50)
        content_lbl.bind(height=resize_card)
        
        self.feed_container.add_widget(card)

    def show_error(self, msg):
        self.feed_container.clear_widgets()
        self.feed_container.add_widget(Label(text=msg, color=(1,0,0,1)))

    def update_bg(self, i, v): self.bg.pos = i.pos; self.bg.size = i.size
    def logout(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'
