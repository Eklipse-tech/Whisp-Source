from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
import requests
import threading

# CONFIG
SERVER_URL = "https://malika-idioblastic-shawnda.ngrok-free.dev"

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Main Background
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1) # Dark Black
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 2. Layout Structure
        root = BoxLayout(orientation='vertical')
        
        # --- HEADER ---
        header = BoxLayout(size_hint=(1, None), height=dp(50), padding=[dp(15), 0])
        title = Label(text="Whisp Feed", font_size='20sp', bold=True, color=(0.2, 0.6, 1.0, 1), halign='left')
        title.bind(size=lambda i,v: setattr(i, 'text_size', i.size))
        header.add_widget(title)
        
        # Refresh Button
        refresh_btn = Button(text="R", size_hint=(None, None), size=(dp(40), dp(40)), pos_hint={'center_y': 0.5})
        refresh_btn.bind(on_release=self.refresh_feed)
        header.add_widget(refresh_btn)
        root.add_widget(header)

        # --- SCROLL VIEW ---
        self.scroll = ScrollView(size_hint=(1, 1), bar_width=dp(4))
        
        # The Feed Container (Holds the cards)
        self.feed_container = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(10), padding=dp(10))
        # Important: Allow container to grow with content
        self.feed_container.bind(minimum_height=self.feed_container.setter('height'))
        
        self.scroll.add_widget(self.feed_container)
        root.add_widget(self.scroll)

        # --- LOGOUT BUTTON ---
        footer = BoxLayout(size_hint=(1, None), height=dp(60), padding=dp(10))
        btn = Button(text="LOGOUT", size_hint=(1, 1), background_color=(0.8, 0.2, 0.2, 1))
        btn.bind(on_release=self.logout)
        footer.add_widget(btn)
        root.add_widget(footer)

        self.add_widget(root)

    def on_enter(self):
        # Trigger feed load when screen appears
        self.refresh_feed(None)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def refresh_feed(self, instance):
        self.feed_container.clear_widgets()
        lbl = Label(text="Loading...", size_hint=(1, None), height=dp(40), color=(0.5,0.5,0.5,1))
        self.feed_container.add_widget(lbl)
        threading.Thread(target=self.fetch_data).start()

    def fetch_data(self):
        try:
            headers = {"ngrok-skip-browser-warning": "true"}
            # Note: /feed endpoint
            resp = requests.get(f"{SERVER_URL}/feed", headers=headers, timeout=8)
            
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self.populate_feed(data), 0)
            else:
                Clock.schedule_once(lambda dt: self.show_error(f"Server Error: {resp.status_code}"), 0)
        except Exception as e:
            # Catch crashes here so app doesn't close
            Clock.schedule_once(lambda dt: self.show_error(f"Offline: {str(e)[:20]}"), 0)

    def show_error(self, msg):
        self.feed_container.clear_widgets()
        self.feed_container.add_widget(Label(text=msg, color=(1,0,0,1), size_hint=(1, None), height=dp(40)))

    def populate_feed(self, posts):
        self.feed_container.clear_widgets()
        if not posts:
            self.show_error("No posts yet!")
            return

        for post in posts:
            self.add_card(post)

    def add_card(self, post):
        # 1. Create Card Box
        card = BoxLayout(orientation='vertical', size_hint=(1, None), padding=dp(15), spacing=dp(5))
        
        # 2. Safe Background Drawing
        with card.canvas.before:
            Color(0.12, 0.15, 0.20, 1) # Slate Blueish
            # We save the reference to 'rect' inside the card object
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
        
        # 3. Update background when card moves/resizes
        def update_card(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        card.bind(pos=update_card, size=update_card)

        # 4. Username & Time
        meta_box = BoxLayout(size_hint=(1, None), height=dp(20))
        user_lbl = Label(text=f"@{post.get('user','?')}", color=(0.3, 0.7, 1, 1), bold=True, halign='left', font_size='14sp')
        user_lbl.bind(size=lambda i,v: setattr(i, 'text_size', i.size))
        
        time_lbl = Label(text=post.get('time','now'), color=(0.5, 0.5, 0.5, 1), halign='right', font_size='12sp')
        time_lbl.bind(size=lambda i,v: setattr(i, 'text_size', i.size))
        
        meta_box.add_widget(user_lbl)
        meta_box.add_widget(time_lbl)
        card.add_widget(meta_box)

        # 5. Content
        content = Label(
            text=post.get('content', '...'),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            font_size='15sp',
            valign='top'
        )
        # Magic text wrapping
        content.bind(width=lambda *x: content.setter('text_size')(content, (content.width, None)))
        content.bind(texture_size=lambda *x: content.setter('height')(content, content.texture_size[1]))
        
        card.add_widget(content)

        # 6. Set Card Height (Dynamic)
        # Wait for texture to calculate, then set height
        def set_height(*args):
            card.height = content.height + dp(45) # Padding + Header
        content.bind(height=set_height)

        self.feed_container.add_widget(card)

    def logout(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'
