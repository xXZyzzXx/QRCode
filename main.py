from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout

from app.custom_widgets import ContentNavigationDrawer

from app.screens import (
    RegisterScreen, CalendarScreen, AssignQRCodeScreen, ReadQRCodeScreen,
    MissingDevicesScreen, Screens, screen_manager
)


class MainApp(MDApp):
    """
    Main app for building GUI
    """
    def build(self) -> MDNavigationLayout:
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        nav_lay = MDNavigationLayout()
        nav_drawer = MDNavigationDrawer()
        nav_drawer.add_widget(ContentNavigationDrawer())

        screen_manager.add_widget(RegisterScreen(name=Screens.REGISTER, nav_drawer=nav_drawer))
        screen_manager.add_widget(CalendarScreen(name=Screens.CALENDAR, nav_drawer=nav_drawer))
        screen_manager.add_widget(AssignQRCodeScreen(name=Screens.ASSIGN_QR, nav_drawer=nav_drawer))
        screen_manager.add_widget(ReadQRCodeScreen(name=Screens.READ_QR, nav_drawer=nav_drawer))
        screen_manager.add_widget(MissingDevicesScreen(name=Screens.MISSING_DEVICES, nav_drawer=nav_drawer))

        screen_manager.current = Screens.CALENDAR  # Set default screen
        nav_lay.add_widget(screen_manager)
        nav_lay.add_widget(nav_drawer)
        return nav_lay


if __name__ == "__main__":
    MainApp().run()
