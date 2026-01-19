from kivy.uix.label import Label
# This checks if the app is actually running
app_instance.layout.clear_widgets()
app_instance.layout.add_widget(Label(text="SUCCESS! LOADED FROM GITHUB!", font_size="30sp", color=(0,1,0,1)))
