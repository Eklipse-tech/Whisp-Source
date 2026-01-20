# --- WHISP "BLUE HORIZON" (Nuclear Rebuild) ---
class WhispLogin(object):
    @staticmethod
    def build_ui():
        # 1. IMPORT EVERYTHING
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.anchorlayout import AnchorLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.graphics import Color, RoundedRectangle
        from kivy.metrics import dp
        from kivy.clock import Clock
        from kivy.core.window import Window
        import requests
        import threading

        # --- CONFIGURATION ---
        SERVER_URL = "https://malika-idioblastic-shawnda.ngrok-free.dev/login"

        # --- THEME COLORS ---
        BG_COLOR = (0.08, 0.11, 0.18, 1)        # Deep Navy
        ACCENT_COLOR = (0.2, 0.6, 1.0, 1)       # Electric Blue
        INPUT_BG = (0.18, 0.22, 0.30, 1)        # Slate Blue
        TEXT_COLOR = (1, 1, 1, 1)               # White

        # 2. ROOT LAYOUT (The Background)
        root = FloatLayout()
        
        with root.canvas.before:
            Color(*BG_COLOR)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        
        def update_bg(instance, value):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        root.bind(pos=update_bg, size=update_bg)

        # 3. ANCHOR (Holds the card in the center)
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        root.add_widget(anchor)

        # 4. THE CARD (Fixed Size = No Squishing)
        card = BoxLayout(
            orientation='vertical', 
            padding=[dp(25), dp(30), dp(25), dp(30)], 
            spacing=dp(15),
            size_hint=(None, None), # Disable auto-sizing
            width=dp(320),          # Fixed Width (Standard Phone)
            height=dp(450)          # Fixed Height (Tall enough)
        )

        # 5. STATIC LOGO (Top)
        logo = Label(
            text="whisp", 
            font_size='48sp', 
            bold=True, 
            color=ACCENT_COLOR,
            size_hint=(1, None),
            height=dp(60),
            halign='center',
            valign='middle'
        )
        logo.bind(size=lambda *x: logo.setter('text_size')(logo, (logo.width, None)))
        card.add_widget(logo)

        # 6. STATUS LABEL (Middle)
        status_label = Label(
            text="", 
            font_size='16sp', 
            color=(1, 1, 0, 1), 
            size_hint=(1, None),
            height=dp(30),
            halign='center'
        )
        card.add_widget(status_label)

        # 7. INPUT BUILDER (Precision Padding)
        def create_input(hint, is_password=False):
            # Wrapper Box
            box = BoxLayout(size_hint=(1, None), height=dp(50))
            
            inp = TextInput(
                hint_text=hint,
                password=is_password,
                multiline=False,
                write_tab=False,
                background_normal='', 
                background_active='', 
                background_color=(0,0,0,0),
                foreground_color=TEXT_COLOR,
                cursor_color=ACCENT_COLOR,
                hint_text_color=(0.6, 0.7, 0.8, 1),
                # CRITICAL FIX: Less vertical padding = Text is visible
                padding=[dp(15), dp(15), dp(15), dp(0)], 
                font_size='16sp'
            )
            
            with inp.canvas.before:
                Color(*INPUT_BG)
                inp.rect = RoundedRectangle(pos=inp.pos, size=inp.size, radius=[12])
            
            def update_rect(inst, val):
                inst.rect.pos = inst.pos
                inst.rect.size = inst.size
            inp.bind(pos=update_rect, size=update_rect)
            
            box.add_widget(inp)
            return inp, box

        user_in, user_box = create_input("Username")
        pass_in, pass_box = create_input("Password", True)
        
        card.add_widget(user_box)
        card.add_widget(pass_box)

        # 8. SPACER (Pushes button down slightly)
        card.add_widget(Label(size_hint=(1, None), height=dp(10)))

        # 9. ENTER BUTTON
        btn = Button(
            text="ENTER",
            background_color=(0,0,0,0),
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(55),
            color=(1, 1, 1, 1)
        )
        with btn.canvas.before:
            Color(*ACCENT_COLOR) 
            btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[25])
            
        def update_btn(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        btn.bind(pos=update_btn, size=update_btn)

        # --- LOGIC ---
        def on_enter(instance):
            u = user_in.text
            p = pass_in.text
            
            status_label.text = "Connecting..."
            status_label.color = (1, 1, 0, 1) # Yellow
            btn.disabled = True

            def send_request():
                try:
                    headers = {"ngrok-skip-browser-warning": "true"}
                    payload = {"username": u, "password": p}
                    
                    resp = requests.post(SERVER_URL, json=payload, headers=headers, timeout=5)
                    
                    if resp.status_code == 200:
                        Clock.schedule_once(lambda dt: success_ui(), 0)
                    elif resp.status_code == 401:
                        Clock.schedule_once(lambda dt: fail_ui("Wrong Password"), 0)
                    else:
                        Clock.schedule_once(lambda dt: fail_ui(f"Error {resp.status_code}"), 0)
                except Exception as e:
                    Clock.schedule_once(lambda dt: fail_ui("Server Offline"), 0)

            threading.Thread(target=send_request).start()

        def success_ui():
            status_label.text = "ACCESS GRANTED"
            status_label.color = (0, 1, 0, 1) # Green
            btn.disabled = False

        def fail_ui(msg):
            status_label.text = msg
            status_label.color = (1, 0, 0, 1) # Red
            btn.disabled = False

        btn.bind(on_release=on_enter)
        card.add_widget(btn)
        
        # Add Card to Anchor
        anchor.add_widget(card)

        return root

# --- ATTACHMENT ---
try:
    ui = WhispLogin.build_ui()
    target = locals().get('app_instance') or globals().get('app_instance')
    if target:
        target.layout.clear_widgets()
        target.layout.add_widget(ui)
    else:
        from kivy.app import App
        if App.get_running_app():
            App.get_running_app().layout.clear_widgets()
            App.get_running_app().layout.add_widget(ui)
except Exception as e:
    raise e
