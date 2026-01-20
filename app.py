# --- WHISP MODERN UI (Self-Contained) ---
class WhispLogin(object):
    @staticmethod
    def build_ui():
        # --- CRITICAL: ALL IMPORTS INSIDE HERE ---
        # This prevents the "NameError" crashes permanently.
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.graphics import Color, RoundedRectangle
        from kivy.core.window import Window

        # 1. Main Background (Deep "Void" Black)
        layout = FloatLayout()
        
        def update_bg(instance, value):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size

        with layout.canvas.before:
            Color(0.05, 0.05, 0.07, 1)  # Almost black background
            layout.bg = RoundedRectangle(pos=layout.pos, size=layout.size)
        
        layout.bind(pos=update_bg, size=update_bg)

        # 2. The "Card" Container (Centered)
        card = BoxLayout(
            orientation='vertical', 
            padding=[30, 50, 30, 50], 
            spacing=25,
            size_hint=(0.85, 0.6), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # 3. Logo (Modern & Minimal)
        card.add_widget(Label(
            text="whisp", 
            font_size='55sp', 
            bold=True, 
            color=(0.6, 0.4, 1.0, 1), # Soft Neon Purple
            size_hint=(1, 0.3)
        ))

        # --- CUSTOM ROUNDED INPUT HELPER ---
        def create_modern_input(hint, is_password=False):
            # Container
            inp_box = BoxLayout(size_hint=(1, 0.15))
            
            # The Input Field
            inp = TextInput(
                hint_text=hint,
                password=is_password,
                multiline=False,
                background_color=(0,0,0,0), # Transparent (we draw our own)
                foreground_color=(1, 1, 1, 1), # White text
                cursor_color=(0.6, 0.4, 1.0, 1),
                padding=[20, 20, 20, 15],
                font_size='18sp'
            )
            
            # Draw Rounded Grey Background
            def update_inp_rect(inst, val):
                inst.rect.pos = inst.pos
                inst.rect.size = inst.size

            with inp.canvas.before:
                Color(0.15, 0.15, 0.18, 1) # Dark Grey Input
                inp.rect = RoundedRectangle(pos=inp.pos, size=inp.size, radius=[15])
            
            inp.bind(pos=update_inp_rect, size=update_inp_rect)
            return inp

        # 4. Add Inputs
        user_in = create_modern_input("Username")
        pass_in = create_modern_input("Password", is_password=True)
        
        card.add_widget(user_in)
        card.add_widget(pass_in)

        # 5. The "Glow" Button
        btn = Button(
            text="ENTER",
            background_color=(0,0,0,0), # Invisible standard bg
            font_size='20sp',
            bold=True,
            size_hint=(1, 0.18),
            color=(1, 1, 1, 1)
        )
        
        def update_btn(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size

        with btn.canvas.before:
            Color(0.4, 0.2, 0.9, 1) # Deep Purple Button
            btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[25])
            
        btn.bind(pos=update_btn, size=update_btn)

        card.add_widget(btn)
        layout.add_widget(card)

        return layout

# --- ATTACHMENT LOGIC (UNCHANGED) ---
try:
    # Build UI inside the safe function
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
