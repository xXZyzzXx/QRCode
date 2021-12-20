from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen

from app.screens.register import RegisterScreen
from app.screens.calendar import CalendarScreen
from app.screens.assign import AssignQRCodeScreen
from app.screens.read import ReadQRCodeScreen
from app.screens.missing import MissingDevicesScreen

from app.custom_widgets import MenuButton
from app.utils import Screens, screen_manager, get_screen_dimensions


Window.size = get_screen_dimensions(debug=True)


class MenuScreen(Screen):
    """
    Main menu screen with other sub-menus
    """
    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        body = AnchorLayout(anchor_x="center", anchor_y="center")
        menu_buttons = BoxLayout(orientation='vertical', size_hint_y=0.5, size_hint_x=0.7)
        for screen_name in Screens.SCREENS:
            menu_buttons.add_widget(MenuButton(screen_name=screen_name))
        body.add_widget(menu_buttons)
        root.add_widget(body)
        self.add_widget(root)


class MainApp(App):
    """
    Main app for building GUI
    """
    def build(self):
        self.title = "QRCode management app"
        screen_manager.add_widget(MenuScreen(name=Screens.MENU))
        screen_manager.add_widget(RegisterScreen(name=Screens.REGISTER))
        screen_manager.add_widget(CalendarScreen(name=Screens.CALENDAR))
        screen_manager.add_widget(AssignQRCodeScreen(name=Screens.ASSIGN_QR))
        screen_manager.add_widget(ReadQRCodeScreen(name=Screens.READ_QR))
        screen_manager.add_widget(MissingDevicesScreen(name=Screens.MISSING_DEVICES))
        screen_manager.current = Screens.MENU  # Set default screen
        return screen_manager


if __name__ == "__main__":
    MainApp().run()
