# --- WHISP "BLUE HORIZON" (The Module Loader) ---
# This file doesn't have UI code. It downloads the UI files and runs them.

class WhispApp(object):
    @staticmethod
    def build_ui():
        import requests
        import os
        import importlib.util
        import sys
        from kivy.uix.screenmanager import ScreenManager
        from kivy.uix.label import Label
        from kivy.clock import Clock

        # --- REPO CONFIG ---
        BASE_URL = "https://raw.githubusercontent.com/Eklipse-tech/Whisp-Source/refs/heads/main/"
        MODULES = ["login.py", "home.py"]
        
        # 1. Download Modules
        # We assume we are in the app's internal storage
        for mod in MODULES:
            try:
                print(f"Downloading {mod}...")
                # Add random query to force fresh download
                import time
                url = f"{BASE_URL}{mod}?t={int(time.time())}"
                
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    with open(mod, 'w') as f:
                        f.write(r.text)
                else:
                    print(f"Failed to download {mod}: {r.status_code}")
            except Exception as e:
                print(f"Error downloading {mod}: {e}")

        # 2. Dynamic Import
        # This is the magic that loads the file we just downloaded
        def load_screen_class(filename, class_name):
            try:
                spec = importlib.util.spec_from_file_location(filename.replace(".py",""), filename)
                module = importlib.util.module_from_spec(spec)
                sys.modules[filename.replace(".py","")] = module
                spec.loader.exec_module(module)
                return getattr(module, class_name)
            except Exception as e:
                return None

        # 3. Assemble App
        try:
            LoginScreen = load_screen_class("login.py", "LoginScreen")
            HomeScreen = load_screen_class("home.py", "HomeScreen")

            if LoginScreen and HomeScreen:
                sm = ScreenManager()
                sm.add_widget(LoginScreen(name='login'))
                sm.add_widget(HomeScreen(name='home'))
                return sm
            else:
                return Label(text="Error: Could not load screens.\nCheck internet & restart.")
                
        except Exception as e:
            return Label(text=f"CRASH: {str(e)}")

# --- ATTACHMENT ---
try:
    ui = WhispApp.build_ui()
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
