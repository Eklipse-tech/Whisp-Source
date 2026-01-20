# --- WHISP "BLUE HORIZON" (Safe Mode & Auto-Centering) ---
class WhispLogin(object):
    @staticmethod
    def build_ui():
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.anchorlayout import AnchorLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.uix.widget import Widget
        from kivy.graphics import Color, RoundedRectangle
        from kivy.metrics import dp
        from kivy.clock import Clock
        import requests
        import threading

        # --- CONFIGURATION ---
        SERVER_URL = "https://malika-idioblastic-shawnda.ngrok-free.dev/login"

        # --- THEME COLORS ---
        BG_COLOR = (0.08, 0.11, 0.18, 1)
        ACCENT_COLOR = (0.2, 0.6, 1.0, 1)
        INPUT_BG = (0.18, 0.22, 0.30, 1)
        TEXT_COLOR = (1, 1, 1, 1) # Pure White

        # 1. ROOT
        root = FloatLayout()
        with root.canvas.before:
            Color(*BG_COLOR)
            root.bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        
        def update_bg(instance, value):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        root.bind(pos=update_bg, size=update_bg)

        # 2. ANCHOR (Keeps everything centered)
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        root.add_widget(anchor)

        # 3. CARD (Fixed Dimensions)
        card = BoxLayout(
            orientation='vertical', 
            padding=[dp(25), dp(30), dp(25), dp(30)], 
            spacing=dp(15),
            size_hint=(None, None),
            width=dp(320),
            height=dp(460)
        )

        # 4. LOGO
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

        status_label = Label(
            text="", 
            font_size='16sp', 
            color=(1, 1, 0, 1), 
            size_hint=(1, None),
            height=dp(30)
        )
        card.add_widget(status_label)

        # 5. INPUT BUILDER (With Auto-Centering)
        def create_input(hint, is_password=False):
            # Fixed Height Container
            stack = FloatLayout(size_hint=(1, None), height=dp(55))
            
            # Layer 1: The Background Box
            bg_widget = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
            with bg_widget.canvas.before:
                Color(*INPUT_BG)
                bg_widget.rect = RoundedRectangle(pos=bg_widget.pos, size=bg_widget.size, radius=[15])
            
            def update_rect(inst, val):
                inst.rect.pos = inst.pos
                inst.rect.size = inst.size
            bg_widget.bind(pos=update_rect, size=update_rect)
            stack.add_widget(bg_widget)

            # Layer 2: The Input (Transparent)
            inp = TextInput(
                hint_text=hint,
                password=is_password,
                multiline=False,
                write_tab=False,
                background_normal='', 
                background_active='', 
                background_color=(0,0,0,0), # Invisible BG
                foreground_color=TEXT_COLOR, # WHITE TEXT
                cursor_color=ACCENT_COLOR,
                hint_text_color=(0.6, 0.7, 0.8, 1),
                font_size='16sp',
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0}
            )

            # --- THE MAGIC FIX: Auto-Calculate Padding ---
            # This forces the text to stay in the middle vertically
            def center_text(instance, value):
                # Padding = [Left, Top, Right, Bottom]
                # Top Padding = (Box Height - Text Height) / 2
                pad_top = (instance.height - instance.line_height) / 2
                instance.padding = [dp(15), pad_top, dp(15), 0]
            
            # Run calculation whenever the box changes size
            inp.bind(size=center_text, line_height=center_text)
            
            stack.add_widget(inp)
            return inp, stack

        user_in, user_box = create_input("Username")
        pass_in, pass_box = create_input("Password", True)
        
        card.add_widget(user_box)
        card.add_widget(pass_box)

        # 6. SPACER
        card.add_widget(Label(size_hint=(1, None), height=dp(10)))

        # 7. BUTTON
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
            btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[28])
            
        def update_btn(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        btn.bind(pos=update_btn, size=update_btn)

        # --- LOGIC ---
        def on_enter(instance):
            u = user_in.text
            p = pass_in.text
            
            status_label.text = "Connecting..."
            status_label.color = (1, 1, 0, 1)
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
            status_label.color = (0, 1, 0, 1)
            btn.disabled = False

        def fail_ui(msg):
            status_label.text = msg
            status_label.color = (1, 0, 0, 1)
            btn.disabled = False

        btn.bind(on_release=on_enter)
        card.add_widget(btn)
        
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
