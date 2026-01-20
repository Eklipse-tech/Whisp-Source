from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# 1. SETUP THE DARK THEME COLORS
# "Whisp" Theme: Deep Purple & Black
BG_COLOR = (0.1, 0.1, 0.12, 1)       # Dark Grey/Blue
ACCENT_COLOR = (0.4, 0.2, 0.8, 1)    # Purple
TEXT_COLOR = (1, 1, 1, 1)            # White

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20
        
        # Draw the background
        with self.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # -- TITLE --
        self.add_widget(Label(
            text="Whisp", 
            font_size='40sp', 
            bold=True, 
            color=ACCENT_COLOR,
            size_hint=(1, 0.3)
        ))

        # -- USERNAME INPUT --
        self.user_input = TextInput(
            hint_text="Username", 
            multiline=False,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT_COLOR,
            size_hint=(1, 0.1)
        )
        self.add_widget(self.user_input)

        # -- PASSWORD INPUT --
        self.pass_input = TextInput(
            hint_text="Password", 
            password=True, 
            multiline=False,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT_COLOR,
            size_hint=(1, 0.1)
        )
        self.add_widget(self.pass_input)

        # -- LOGIN BUTTON --
        self.login_btn = Button(
            text="ENTER",
            background_color=ACCENT_COLOR,
            background_normal='',
            font_size='20sp',
            bold=True,
            size_hint=(1, 0.15)
        )
        self.login_btn.bind(on_press=self.do_login)
        self.add_widget(self.login_btn)

        # -- STATUS LABEL (For errors) --
        self.status = Label(
            text="", 
            color=(1, 0.3, 0.3, 1),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.status)

        # Spacer at bottom
        self.add_widget(Label(size_hint=(1, 0.2)))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def do_login(self, instance):
        # This is where we will eventually connect to your PC
        username = self.user_input.text
        password = self.pass_input.text
        self.status.text = f"Connecting as {username}..."

# --- THE MAGIC HOOK ---
# We attach our new screen to the 'app_instance' from the Shell
app_instance.layout.clear_widgets()
app_instance.layout.add_widget(LoginScreen())
