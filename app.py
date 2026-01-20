# --- SELF-CONTAINED UI ---
# We define the class first, but we don't import ANYTHING at the top level.
# This forces the script to find the tools it needs when it runs.

class WhispLogin(object):
    # We use a factory method to build the widget to avoid inheritance scope issues
    @staticmethod
    def build_ui():
        # --- ALL IMPORTS MUST BE INSIDE HERE ---
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.graphics import Color, Rectangle

        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=[40, 60, 40, 60], spacing=20)

        # 1. Background Logic
        def update_rect(instance, value):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

        with layout.canvas.before:
            Color(0.12, 0.12, 0.14, 1)  # Dark Grey
            layout.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=update_rect, pos=update_rect)

        # 2. Title
        layout.add_widget(Label(
            text="WHISP", 
            font_size='40sp', 
            bold=True, 
            color=(0.5, 0.3, 0.9, 1), # Purple Accent
            size_hint=(1, 0.3)
        ))

        # 3. Username
        user_input = TextInput(
            hint_text="Username", 
            multiline=False, 
            size_hint=(1, 0.12),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.5, 0.3, 0.9, 1)
        )
        layout.add_widget(user_input)

        # 4. Password
        pass_input = TextInput(
            hint_text="Password", 
            password=True, 
            multiline=False, 
            size_hint=(1, 0.12),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.5, 0.3, 0.9, 1)
        )
        layout.add_widget(pass_input)

        # 5. Button
        btn = Button(
            text="ENTER", 
            size_hint=(1, 0.15),
            background_color=(0.5, 0.3, 0.9, 1),
            background_normal=''
        )
        layout.add_widget(btn)

        return layout

# --- ATTACHMENT LOGIC ---
try:
    # 1. Build the UI using the safe function
    ui = WhispLogin.build_ui()
    
    # 2. Find the Shell
    target_app = None
    if 'app_instance' in locals():
        target_app = locals()['app_instance']
    elif 'app_instance' in globals():
        target_app = globals()['app_instance']
        
    # 3. Mount it
    if target_app:
        target_app.layout.clear_widgets()
        target_app.layout.add_widget(ui)
    else:
        # Fallback for strict environments
        from kivy.app import App
        app = App.get_running_app()
        if app:
            app.layout.clear_widgets()
            app.layout.add_widget(ui)

except Exception as e:
    raise e
