# --- WHISP MODERN UI (Bulletproof Scope) ---
class WhispLogin(object):
    @staticmethod
    def build_ui():
        # 1. IMPORT EVERYTHING HERE (So it's available everywhere inside this function)
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.graphics import Color, RoundedRectangle
        from kivy.metrics import dp

        # 2. Main Background (Deep "Void" Black)
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.05, 0.05, 0.07, 1)  # Almost black
            layout.bg = RoundedRectangle(pos=layout.pos, size=layout.size, radius=[0])
        
        def update_bg(instance, value):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
        layout.bind(pos=update_bg, size=update_bg)

        # 3. The "Card" Container (Centered)
        card = BoxLayout(
            orientation='vertical', 
            padding=[dp(30), dp(50), dp(30), dp(50)], 
            spacing=dp(20),
            size_hint=(0.85, 0.6), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # 4. Logo
        card.add_widget(Label(
            text="whisp", 
            font_size='50sp', 
            bold=True, 
            color=(0.6, 0.4, 1.0, 1), # Soft Neon Purple
            size_hint=(1, 0.25)
        ))

        # 5. USERNAME INPUT (Manually built to avoid scope errors)
        user_box = BoxLayout(size_hint=(1, 0.15))
        user_in = TextInput(
            hint_text="Username",
            multiline=False,
            background_color=(0,0,0,0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.6, 0.4, 1.0, 1),
            padding=[dp(15), dp(15), dp(15), dp(15)],
            font_size='16sp'
        )
        with user_in.canvas.before:
            Color(0.15, 0.15, 0.18, 1) # Dark Grey
            user_in.rect = RoundedRectangle(pos=user_in.pos, size=user_in.size, radius=[15])
            
        def update_user_rect(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        user_in.bind(pos=update_user_rect, size=update_user_rect)
        
        user_box.add_widget(user_in)
        card.add_widget(user_box)

        # 6. PASSWORD INPUT (Manually built)
        pass_box = BoxLayout(size_hint=(1, 0.15))
        pass_in = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            background_color=(0,0,0,0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.6, 0.4, 1.0, 1),
            padding=[dp(15), dp(15), dp(15), dp(15)],
            font_size='16sp'
        )
        with pass_in.canvas.before:
            Color(0.15, 0.15, 0.18, 1) # Dark Grey
            pass_in.rect = RoundedRectangle(pos=pass_in.pos, size=pass_in.size, radius=[15])
            
        def update_pass_rect(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
        pass_in.bind(pos=update_pass_rect, size=update_pass_rect)
        
        pass_box.add_widget(pass_in)
        card.add_widget(pass_box)

        # 7. BUTTON (Manually built)
        btn = Button(
            text="ENTER",
            background_color=(0,0,0,0),
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.15),
            color=(1, 1, 1, 1)
        )
        with btn.canvas.before:
            Color(0.4, 0.2, 0.9, 1) # Deep Purple
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
