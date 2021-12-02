from kivy.uix.button import Button

from app.utils import screen_manager


class MenuButton(Button):
    def __init__(self, screen_name: str, **kwargs):
        super().__init__(**kwargs)
        self.text = screen_name

    def on_release(self):
        screen_manager.current = self.text



