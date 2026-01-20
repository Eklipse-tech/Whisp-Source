# --- WHISP "BLUE HORIZON" (Master Fix) ---
class WhispLogin(object):
    @staticmethod
    def build_ui():
        # 1. IMPORT EVERYTHING
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.graphics import Color, RoundedRectangle
        from kivy.metrics import dp
        from kivy.clock import Clock
        import requests
        import threading

        # --- CONFIGURATION ---
        SERVER_URL = "https://malika-idioblastic-shawnda.ngrok-free.dev/login"

        # --- THEME COLORS ---
        BG_COLOR = (0.08, 0.11, 0.18, 1)        # Deep Navy
        ACCENT_COLOR = (0.2, 0.6, 1.0, 1)       # Electric Blue
        INPUT_BG = (0.18, 0.22, 0.30, 1)        # Slate Blue
        TEXT_COLOR = (1, 1, 1, 1)               # White

        # 2. Main Layout
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(*BG_COLOR)
            layout.bg = RoundedRectangle(pos=layout.pos, size=layout.size, radius=[0])
        
        def update_bg(instance, value):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        layout.bind(pos=update_bg, size=update_bg)

        # 3. Card Container
        card = BoxLayout(
            orientation='vertical', 
            padding=[dp(25), dp(30), dp(25), dp(30)], 
            spacing=dp(15),
            size_hint=(0.85, 0.65), 
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        # 4. STATIC LOGO (Will never change)
        logo = Label(
            text="whisp", 
            font_size='50sp', 
            bold=True, 
            color=ACCENT_COLOR,
            size_hint=(1, 0.20),
            halign='center',
            valign='middle'
        )
        logo.bind(size=lambda *x: logo.setter('text_size')(logo, (logo.width, None)))
        card.add_widget(logo)

        # 5. NEW STATUS LABEL (Changes instead of logo)
        status_label = Label(
            text="", 
            font_size='16sp', 
            color=(1, 1, 0, 1), # Starts Yellow
            size_hint=(1, 0.10),
            halign='center'
        )
        card.add_widget(status_label)

        # 6. Helper for Inputs (Text Visibility Fix)
        def create_input(hint, is_password=False):
            box = BoxLayout(size_hint=(1, 0.15))
            
            inp = TextInput(
                hint_text=hint,
                password=is_password,
                multiline=False,
                write_tab=False,
                background_normal='', 
                background_active='', 
                background_color=(0,0,0,0), # Transparent
                foreground_color=TEXT_COLOR, # WHITE TEXT
                cursor_color=ACCENT_COLOR,
                hint_text_color=(0.6, 0.7, 0.8, 1),
                # FIX: Smaller padding ensures text stays visible inside the box
                padding=[dp(15), dp(12), dp(15), dp(12)],
                font_size='18sp'
            )
            
            # Custom Background
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

        # 7. Enter Button
        btn = Button(
            text="ENTER",
            background_color=(0,0,0,0),
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.15),
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
            
            # Update STATUS LABEL only
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
        layout.add_widget(card)

        return layout

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
