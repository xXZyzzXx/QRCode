from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy_garden.zbarcam import ZBarCam

from app.utils import Screens, build_screen
from app.custom_widgets import MenuButton


class MenuScreen(Screen):
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        body = AnchorLayout(anchor_x="center", anchor_y="center")
        menu_buttons = BoxLayout(orientation='vertical', size_hint_y=0.5, size_hint_x=0.5)
        for screen_name in Screens.SCREENS:
            menu_buttons.add_widget(MenuButton(screen_name=screen_name))
        body.add_widget(menu_buttons)
        root.add_widget(body)
        self.add_widget(root)


# Screens
class RegisterScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # Custom logic
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)


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
