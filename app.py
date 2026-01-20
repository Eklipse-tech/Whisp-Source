from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

# --- UI DEFINITION ---
class WhispLogin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [40, 60, 40, 60]  # Left, Top, Right, Bottom
        self.spacing = 20
        
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

        # Inputs
        self.user = TextInput(
            hint_text="Username", 
            multiline=False, 
            size_hint=(1, 0.12),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.5, 0.3, 0.9, 1)
        )
        self.add_widget(self.user)

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

        # Button
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
        self.rect.size = self.size
        self.rect.pos = self.pos

# --- THE ATTACHMENT LOGIC ---
# This is the part that was failing before. 
# We look for 'app_instance' in the local variables passed by the Shell.

try:
    # 1. Create the UI
    ui = WhispLogin()
    
    # 2. Find the App Window (The "Shell")
    # In the new shell, 'app_instance' is passed directly as a local variable.
    if 'app_instance' in locals():
        target_app = locals()['app_instance']
        
        # 3. Mount the UI
        target_app.layout.clear_widgets() # Clear "Loading..."
        target_app.layout.add_widget(ui)  # Add Login Screen
        
    elif 'app_instance' in globals():
        # Fallback check
        globals()['app_instance'].layout.clear_widgets()
        globals()['app_instance'].layout.add_widget(ui)
        
except Exception as e:
    # If this fails, the Shell will catch it and show the Red Error
    raise e
