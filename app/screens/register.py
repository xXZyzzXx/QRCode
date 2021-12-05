from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from app.utils import build_screen
from app.custom_widgets import (
    RegisterNewPupilButton, CustomTextInput
)


class RegisterScreen(Screen):
    """
    Screen to register new pupils
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.text_input_lines = None

    def on_enter(self, *args):
        self.text_input_lines = []  # Refresh initial data
        body = BoxLayout()
        body.add_widget(self.build_register_menu())  # Creating register menu
        root = build_screen(screen_name=self.name, body=body)  # Building all parts together
        self.add_widget(root)

    def on_leave(self, *args):
        self.clear_widgets()

    def build_register_menu(self) -> AnchorLayout:
        root = AnchorLayout(anchor_x="center", anchor_y="top")

        notifications_lay = BoxLayout(orientation="vertical", height=50)
        notification_label = Label()
        notifications_lay.add_widget(notification_label)

        box_lay = BoxLayout(orientation="vertical", size_hint=(0.7, 0.8), padding=(0, 0, 0, 50))
        box_lay.add_widget(notifications_lay)
        box_lay.add_widget(Label(text=r"You can create a new pupil here \/", halign="left"))
        # List with required fields to create a new pupil
        required_fields = ["name", "first name", "phone number"]
        # Generating labels and text inputs for each line
        for line_name in required_fields:
            line_box = BoxLayout(orientation="vertical")
            label = Label(text=line_name)
            text_input = CustomTextInput(key=line_name)
            self.text_input_lines.append(text_input)  # Add to global list
            line_box.add_widget(label)
            line_box.add_widget(text_input)
            box_lay.add_widget(line_box)

        box_lay.add_widget(Widget(size_hint_y=None, height=50))  # Empty widget as separator
        box_lay.add_widget(RegisterNewPupilButton(text_inputs=self.text_input_lines, nl=notification_label))
        root.add_widget(box_lay)
        return root
