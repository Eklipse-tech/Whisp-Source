# --- WHISP "BLUE HORIZON" THEME ---
class WhispLogin(object):
    @staticmethod
    def build_ui():
        # 1. IMPORT EVERYTHING (Scope Safety)
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.graphics import Color, RoundedRectangle
        from kivy.metrics import dp

        # --- THEME COLORS ---
        BG_COLOR = (0.08, 0.11, 0.18, 1)        # Deep Navy Blue
        CARD_COLOR = (0.12, 0.16, 0.24, 1)      # Lighter Slate Blue
        ACCENT_COLOR = (0.2, 0.6, 1.0, 1)       # Electric Blue
        INPUT_BG = (0.18, 0.22, 0.30, 1)        # Input Field Background
        TEXT_COLOR = (1, 1, 1, 1)               # Pure White

        # 2. Main Background
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(*BG_COLOR)
            layout.bg = RoundedRectangle(pos=layout.pos, size=layout.size, radius=[0])
        
        def update_bg(instance, value):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        layout.bind(pos=update_bg, size=update_bg)

        # 3. The "Card" Container
        card = BoxLayout(
            orientation='vertical', 
            padding=[dp(25), dp(40), dp(25), dp(40)], 
            spacing=dp(20),
            size_hint=(0.85, 0.55), 
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        # 4. Logo
        card.add_widget(Label(
            text="whisp", 
            font_size='50sp', 
            bold=True, 
            color=ACCENT_COLOR,
            size_hint=(1, 0.3)
        ))

        # 5. USERNAME INPUT (Fixed)
        user_box = BoxLayout(size_hint=(1, 0.18))
        user_in = TextInput(
            hint_text="Username",
            multiline=False,
            write_tab=False,
            background_color=(0,0,0,0), # Transparent standard BG
            foreground_color=TEXT_COLOR, # Force White Text
            cursor_color=ACCENT_COLOR,
            hint_text_color=(0.6, 0.7, 0.8, 1), # Light Blue Hint
            padding=[dp(15), dp(15), dp(15), dp(15)],
            font_size='18sp'
        )
        
        # Custom Rounded Background
        with user_in.canvas.before:
            Color(*INPUT_BG)
            user_in.rect = RoundedRectangle(pos=user_in.pos, size=user_in.size, radius=[12])
            
        def update_user_rect(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        user_in.bind(pos=update_user_rect, size=update_user_rect)
        
        user_box.add_widget(user_in)
        card.add_widget(user_box)

        # 6. PASSWORD INPUT (Fixed)
        pass_box = BoxLayout(size_hint=(1, 0.18))
        pass_in = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            write_tab=False,
            background_color=(0,0,0,0),
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT_COLOR,
            hint_text_color=(0.6, 0.7, 0.8, 1),
            padding=[dp(15), dp(15), dp(15), dp(15)],
            font_size='18sp'
        )
        
        with pass_in.canvas.before:
            Color(*INPUT_BG)
            pass_in.rect = RoundedRectangle(pos=pass_in.pos, size=pass_in.size, radius=[12])
            
        def update_pass_rect(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        pass_in.bind(pos=update_pass_rect, size=update_pass_rect)
        
        pass_box.add_widget(pass_in)
        card.add_widget(pass_box)

        # 7. BUTTON (Blue)
        btn = Button(
            text="ENTER",
            background_color=(0,0,0,0),
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.20),
            color=(1, 1, 1, 1)
        )
        with btn.canvas.before:
            Color(*ACCENT_COLOR) 
            btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[25])
            
        def update_btn(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        btn.bind(pos=update_btn, size=update_btn)

        card.add_widget(btn)
        layout.add_widget(card)

        return layout

# --- ATTACHMENT LOGIC ---
try:
    ui = WhispLogin.build_ui()
    
    target_app = None
    if 'app_instance' in locals():
        target_app = locals()['app_instance']
    elif 'app_instance' in globals():
        target_app = globals()['app_instance']
        
    if target_app:
        target_app.layout.clear_widgets()
        target_app.layout.add_widget(ui)
    else:
        # Fallback for PC testing
        from kivy.app import App
        app = App.get_running_app()
        if app:
            app.layout.clear_widgets()
            app.layout.add_widget(ui)

except Exception as e:
    raise e
