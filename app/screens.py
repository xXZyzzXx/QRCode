from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, WipeTransition
from kivy_garden.zbarcam import ZBarCam

screen_manager = ScreenManager(transition=NoTransition())


class Screens:
    """Screen names"""
    REGISTER = "Register"
    CALENDAR = "Calendar"
    ASSIGN_QR = "Assign QR code"
    READ_QR = "Read QR code"
    MISSING_DEVICES = "Missing devices"
    MENU = "Menu"

    SCREENS = [REGISTER, CALENDAR, ASSIGN_QR, READ_QR, MISSING_DEVICES]


class MenuButton(Button):
    def __init__(self, screen_name: str, **kwargs):
        super().__init__(**kwargs)
        self.text = screen_name

    def on_release(self):
        screen_manager.current = self.text


class BackButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        screen_manager.current = Screens.MENU


class CustomScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    @staticmethod
    def get_back_btn():
        root = AnchorLayout(anchor_x="center", anchor_y="center")
        footer = BoxLayout(orientation='vertical', size_hint_y=0.2)
        footer.add_widget(BackButton(text="Back to main menu"))
        root.add_widget(footer)
        return root


class MenuScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        body = AnchorLayout(anchor_x="center", anchor_y="center")
        menu_buttons = BoxLayout(orientation='vertical', size_hint_y=0.5, size_hint_x=0.5)
        for screen_name in Screens.SCREENS:
            menu_buttons.add_widget(MenuButton(screen_name=screen_name))
        body.add_widget(menu_buttons)
        root.add_widget(body)
        self.add_widget(root)


class RegisterScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        body = BoxLayout(orientation='vertical', size_hint_y=0.8)
        footer = self.get_back_btn()
        root.add_widget(body)
        root.add_widget(footer)
        self.add_widget(root)


class CalendarScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=40)
        header.add_widget(Label(text=Screens.CALENDAR))
        body = BoxLayout(orientation='vertical')
        # body.add_widget(Calender())
        root.add_widget(header)
        root.add_widget(body)
        root.add_widget(Widget())
        self.add_widget(root)


class AssignQRCodeScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        root.add_widget(Widget())
        # Adding QRCode scanner to layout
        """
        try:
            root.add_widget(ZBarCam())
        except Exception as e:
            print(f"Add ZBarCam widget error")
        """
        self.add_widget(root)


class ReadQRCodeScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        root.add_widget(Widget())
        self.add_widget(root)


class MissingDevicesScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        root.add_widget(Widget())
        self.add_widget(root)
