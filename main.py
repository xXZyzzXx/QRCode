from kivy.app import App

from app.screens import (
    RegisterScreen, CalendarScreen, AssignQRCodeScreen, ReadQRCodeScreen,
    MissingDevicesScreen, MenuScreen, Screens, screen_manager
)


class MainApp(App):
    """
    Main app for building GUI
    """

    def build(self):
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
