from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, WipeTransition
from kivymd.uix.toolbar import MDToolbar
from kivy_garden.zbarcam import ZBarCam

screen_manager = ScreenManager(transition=NoTransition())


class Screens:
    """Screen names"""
    REGISTER = "Register"
    CALENDAR = "Calendar"
    ASSIGN_QR = "Assign QR code"
    READ_QR = "Read QR code"
    MISSING_DEVICES = "Missing devices"


class CustomScreen(Screen):
    def __init__(self, nav_drawer, **kw):
        super().__init__(**kw)
        self.nav_drawer = nav_drawer

    def on_pre_enter(self):
        self.nav_drawer.set_state('close')


class RegisterScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        toolbar = MDToolbar(title=Screens.REGISTER)
        toolbar.right_action_items = [["dots-vertical", lambda x: self.nav_drawer.set_state('toggle')]]
        root.add_widget(toolbar)
        root.add_widget(Widget())
        self.add_widget(root)


class CalendarScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        toolbar = MDToolbar(title=Screens.CALENDAR)
        toolbar.right_action_items = [["dots-vertical", lambda x: self.nav_drawer.set_state('toggle')]]
        root.add_widget(toolbar)
        root.add_widget(Widget())
        self.add_widget(root)


class AssignQRCodeScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        toolbar = MDToolbar(title=Screens.ASSIGN_QR)
        toolbar.right_action_items = [["dots-vertical", lambda x: self.nav_drawer.set_state('toggle')]]
        root.add_widget(toolbar)
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
        toolbar = MDToolbar(title=Screens.READ_QR)
        toolbar.right_action_items = [["dots-vertical", lambda x: self.nav_drawer.set_state('toggle')]]
        root.add_widget(toolbar)
        root.add_widget(Widget())
        self.add_widget(root)


class MissingDevicesScreen(CustomScreen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        toolbar = MDToolbar(title=Screens.MISSING_DEVICES)
        toolbar.right_action_items = [["dots-vertical", lambda x: self.nav_drawer.set_state('toggle')]]
        root.add_widget(toolbar)
        root.add_widget(Widget())
        self.add_widget(root)
