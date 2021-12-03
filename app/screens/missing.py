from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from app.utils import build_screen


class MissingDevicesScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)