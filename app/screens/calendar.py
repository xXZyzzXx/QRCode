from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from KivyCalendar import CalendarWidget

from app.utils import build_screen


class CalendarScreen(Screen):
    def on_enter(self, *args):
        body = AnchorLayout(anchor_x="center", anchor_y="center")
        # TODO: Custom logic, just in progress
        body.add_widget(CalendarWidget(size_hint_y=.8))
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)
