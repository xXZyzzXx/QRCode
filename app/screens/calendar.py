from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from KivyCalendar import CalendarWidget

from app.utils import build_screen


class CalendarScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        body.add_widget(CalendarWidget())
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)
