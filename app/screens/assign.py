from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
# from kivy_garden.zbarcam import ZBarCam

from app.utils import build_screen
from app.database import get_all_pupils, add_qr_code_data_to_pupil_by_name


class AssignScreenNames:
    """
    Provide assign screen names
    """
    START = "start_screen"
    READ = "read_qr"
    ASSIGN = "assign_qr"

    SCREENS = [START, READ, ASSIGN]


# Basic screen
class AssignQRCodeScreen(Screen):
    """
    Root screen to manage assign logic with sub-menus
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.assign_qr_manager = AssignScreenManager()
        self.build_assign_screen()

    def build_assign_screen(self) -> None:
        self.assign_qr_manager.qr_code_data = None
        body = BoxLayout()
        self.assign_qr_manager.add_widget(StartScreen(name=AssignScreenNames.START))
        self.assign_qr_manager.add_widget(ReadQRScreen(name=AssignScreenNames.READ))
        self.assign_qr_manager.add_widget(AssignToPupilScreen(name=AssignScreenNames.ASSIGN))
        self.assign_qr_manager.current = AssignScreenNames.START
        body.add_widget(self.assign_qr_manager)
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def on_enter(self, *args):
        self.assign_qr_manager.qr_code_data = None
        self.assign_qr_manager.set_default_screen()


# Additional widgets
class AssignScreenManager(ScreenManager):
    """
    Custom screen manager for navigation between assign menu
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.qr_code_data = None

    def change_screen_to_assign(self, qr_code_data: dict) -> None:
        self.qr_code_data = qr_code_data
        self.change_to_screen(screen_name=AssignScreenNames.ASSIGN)

    def set_default_screen(self) -> None:
        if self.current != AssignScreenNames.START:
            self.change_to_screen(screen_name=AssignScreenNames.START)

    def change_to_screen(self, screen_name: str) -> None:
        self.current = screen_name


# Assign screens
class StartScreen(Screen):
    """
    Default menu to start assign QR or get back
    """
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.add_widget(self.build_start_screen())

    def build_start_screen(self) -> AnchorLayout:
        root = AnchorLayout(anchor_x="center", anchor_y="center")
        read_qr_btn = Button(text="Start read qr code", size_hint=(.6, .25))
        read_qr_btn.bind(
            on_release=lambda _: self.manager.change_to_screen(screen_name=AssignScreenNames.READ)
        )
        root.add_widget(read_qr_btn)
        return root


class ReadQRScreen(Screen):
    """
    Reading QR data and pass to next screen
    """
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self.skip_reading_qr_for_test()

    def skip_reading_qr_for_test(self) -> None:
        # Temporary for testing (qr code read emulating)
        qr_code_data = {"qr_code": "47389d389d2y3733yh4393"}
        self.manager.change_screen_to_assign(qr_code_data=qr_code_data)


class AssignToPupilScreen(Screen):
    """
    Choosing pupils to assign a QR code
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.qr_code_data = None

    def on_enter(self, *args):
        self.qr_code_data = self.manager.qr_code_data
        self.add_widget(self.build_assign_screen())

    def build_assign_screen(self) -> AnchorLayout:
        root = AnchorLayout(anchor_x="center", anchor_y="top")
        box_lay = BoxLayout(orientation="vertical", size_hint=(0.9, 0.8))

        label = Label(text="Select a pupil to assign a qr code", size_hint_y=.15)
        scroll_lay = ScrollView(size_hint_y=.85, do_scroll_x=False, bar_inactive_color=(.7, .7, .7, .5))
        grid_lay = GridLayout(size_hint_y=None, cols=1)
        grid_lay.bind(minimum_height=grid_lay.setter('height'))
        all_pupils = get_all_pupils()
        for pupil_name in all_pupils:
            pupil_data = all_pupils.get(pupil_name)
            grid_lay.add_widget(AssignQRCodeButton(pupil_data=pupil_data, screen=self, height=30, size_hint_y=None))

        scroll_lay.add_widget(grid_lay)
        box_lay.add_widget(label)
        box_lay.add_widget(scroll_lay)
        root.add_widget(box_lay)
        return root

    def set_assign_choice(self, pupil_name: str, accept: bool = False) -> None:
        if accept:
            qr_code = self.qr_code_data.get("qr_code")
            add_qr_code_data_to_pupil_by_name(qr_code_data=qr_code, pupil_name=pupil_name)
            self.manager.set_default_screen()


# Custom widgets
class AssignQRCodeButton(Button):
    """
    Custom button to open confirmation popup to assign qr data to pupil
    """
    def __init__(self, pupil_data: dict, screen: Screen, **kwargs):
        super().__init__(**kwargs)
        self.pupil_data = pupil_data
        self.pupil_name = pupil_data.get("name")
        self.pupil_first_name = pupil_data.get("first_name")
        self.pupil_phone_number = pupil_data.get("phone_number")
        self.parent_screen = screen
        self.text = f"{self.pupil_name}, {self.pupil_first_name}, {self.pupil_phone_number}"
        self.popup = None

    def on_release(self):
        self.show_assign_qr_popup()

    def show_assign_qr_popup(self):
        self.popup = Popup(title=f"Do you want to assign QR code to {self.pupil_name}?", size_hint=(.8, .4))
        box_lay = BoxLayout(orientation="vertical")
        pupils_data_lay = BoxLayout(orientation="vertical", size_hint_y=.7)
        choice_lay = BoxLayout(orientation="horizontal", size_hint_y=.3)
        for key in self.pupil_data:
            if key == "qr_code":  # Skip unnecessary data to show
                continue
            value = self.pupil_data[key]
            pupils_data_lay.add_widget(Label(text=f"{key} - {value}"))

        accept_button = Button(text="Accept")
        decline_button = Button(text="Decline")
        accept_button.bind(on_release=lambda _: self.set_assign_choice(accept=True))
        decline_button.bind(on_release=lambda _: self.set_assign_choice(accept=False))
        choice_lay.add_widget(accept_button)
        choice_lay.add_widget(decline_button)

        box_lay.add_widget(pupils_data_lay)
        box_lay.add_widget(choice_lay)
        self.popup.add_widget(box_lay)
        self.popup.open()

    def set_assign_choice(self, accept: bool = False):
        self.parent_screen.set_assign_choice(accept=accept, pupil_name=self.pupil_name)
        self.popup.dismiss()
