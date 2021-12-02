from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy_garden.zbarcam import ZBarCam
from KivyCalendar import CalendarWidget

from app.utils import Screens, build_screen
from app.custom_widgets import MenuButton, RegisterNewPupilButton, OutlinedLabel, CustomTextInput


class MenuScreen(Screen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        body = AnchorLayout(anchor_x="center", anchor_y="center")
        menu_buttons = BoxLayout(orientation='vertical', size_hint_y=0.5, size_hint_x=0.7)
        for screen_name in Screens.SCREENS:
            menu_buttons.add_widget(MenuButton(screen_name=screen_name))
        body.add_widget(menu_buttons)
        root.add_widget(body)
        self.add_widget(root)


# Screens
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
        # Creating register menu
        body.add_widget(self.build_register_menu())
        # Building all parts together
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def build_register_menu(self):
        root = AnchorLayout(anchor_x="center", anchor_y="top")

        notifications_lay = BoxLayout(orientation="vertical", height=50)
        notification_label = OutlinedLabel()
        notifications_lay.add_widget(notification_label)  # Button(text="notifications")

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


class CalendarScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)


class AssignQRCodeScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)


class ReadQRCodeScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        """
        try:
            root.add_widget(ZBarCam())
        except Exception as e:
            print(f"Add ZBarCam widget error")
        """
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)


class MissingDevicesScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)
