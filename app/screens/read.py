from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from app.utils import build_screen


class ReadQRCodeScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # TODO: Custom logic, just in progress
        """
        try:
            root.add_widget(ZBarCam())
        except Exception as e:
            print(f"Add ZBarCam widget error")
        """
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)
