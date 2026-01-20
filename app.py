from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import random

# 1. Define the UI
class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Add a colored background so we KNOW it's drawing
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Dark Grey
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Big Title
        self.add_widget(Label(text="WHISP RELOADED", font_size='40sp', color=(0,1,0,1)))
        
        # Test Button
        self.btn = Button(text="CLICK ME", size_hint=(1, 0.2))
        self.add_widget(self.btn)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# 2. THE CRITICAL PART (Attaching to the screen)
try:
    # We try to find the shell app
    if 'app_instance' in globals():
        app_instance.layout.clear_widgets() # Clean slate
        app_instance.layout.add_widget(LoginScreen()) # Add the new UI
    else:
        print("Error: Could not find app_instance")
except Exception as e:
    # If something fails, print it to the screen so we see the error
    if 'app_instance' in globals():
        app_instance.layout.add_widget(Label(text=f"ERROR: {e}", color=(1,0,0,1)))
