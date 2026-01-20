# We only import the layout basics at the top level
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# --- UI DEFINITION ---
class WhispLogin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [40, 60, 40, 60]
        self.spacing = 20
        
        # --- FIX: IMPORT GRAPHICS INSIDE THE METHOD ---
        # This tells Python: "Look for Color right here, right now."
        from kivy.graphics import Color, Rectangle

        # Dark Background
        with self.canvas.before:
            Color(0.12, 0.12, 0.14, 1)  # Dark Grey
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Title
        self.add_widget(Label(
            text="WHISP", 
            font_size='40sp', 
            bold=True, 
            color=(0.5, 0.3, 0.9, 1), # Purple Accent
            size_hint=(1, 0.3)
        ))

        # Username Input
        self.user = TextInput(
            hint_text="Username", 
            multiline=False, 
            size_hint=(1, 0.12),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.5, 0.3, 0.9, 1)
        )
        self.add_widget(self.user)

        # Password Input
        self.pwd = TextInput(
            hint_text="Password", 
            password=True, 
            multiline=False, 
            size_hint=(1, 0.12),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.5, 0.3, 0.9, 1)
        )
        self.add_widget(self.pwd)

        # Login Button
        self.btn = Button(
            text="ENTER", 
            size_hint=(1, 0.15),
            background_color=(0.5, 0.3, 0.9, 1),
            background_normal=''
        )
        self.add_widget(self.btn)
        
        # Status Label
        self.status = Label(text="", color=(1,0.3,0.3,1), size_hint=(1, 0.1))
        self.add_widget(self.status)

    def update_rect(self, *args):
        # Re-import here to be 100% safe
        from kivy.graphics import Rectangle
        self.rect.size = self.size
        self.rect.pos = self.pos

# --- THE ATTACHMENT LOGIC ---
try:
    # 1. Create the UI
    ui = WhispLogin()
    
    # 2. Find the App Window
    # We check both local and global scopes to be 100% sure we find the shell
    target_app = None
    if 'app_instance' in locals():
        target_app = locals()['app_instance']
    elif 'app_instance' in globals():
        target_app = globals()['app_instance']
        
    if target_app:
        target_app.layout.clear_widgets() # Clear "Loading..."
        target_app.layout.add_widget(ui)  # Add Login Screen
    else:
        print("CRITICAL: Could not find app_instance to attach UI.")

except Exception as e:
    # This ensures the red error message appears if something else breaks
    raise e
