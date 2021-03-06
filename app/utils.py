import datetime
import os
from typing import Union

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, NoTransition

screen_manager = ScreenManager(transition=NoTransition())

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 1136


def get_screen_dimensions(debug: bool = False) -> tuple:
    """
    Returns current dimensions
    """
    scale_modifier = 1.5
    if not debug:
        return DEFAULT_WIDTH, DEFAULT_HEIGHT
    return DEFAULT_WIDTH / scale_modifier, DEFAULT_HEIGHT / scale_modifier


class Screens:
    """
    Provide screen names
    """
    REGISTER = "Register"
    CALENDAR = "Calendar"
    ASSIGN_QR = "Assign QR code"
    READ_QR = "Read QR code"
    MISSING_DEVICES = "Missing devices"
    MENU = "Menu"

    SCREENS = [REGISTER, CALENDAR, ASSIGN_QR, READ_QR, MISSING_DEVICES]


class BackButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        screen_manager.current = Screens.MENU


def get_header(screen_name: str) -> BoxLayout:
    header = BoxLayout(orientation='vertical', size_hint_y=0.1)
    header.add_widget(Label(text=f"{screen_name} menu"))
    return header


def get_body() -> BoxLayout:
    body = BoxLayout(orientation='vertical', size_hint_y=0.75)
    return body


def get_footer() -> AnchorLayout:
    footer = AnchorLayout(anchor_x="center", anchor_y="center", size_hint_y=0.15)
    box_lay = BoxLayout(orientation='vertical', size_hint_x=0.5, size_hint_y=0.5)
    box_lay.add_widget(BackButton(text="Back to main menu"))
    footer.add_widget(box_lay)
    return footer


def build_screen(screen_name: str, body: Union[BoxLayout, AnchorLayout]) -> BoxLayout:
    root = BoxLayout(orientation='vertical')
    root.add_widget(get_header(screen_name=screen_name))
    root.add_widget(body)
    root.add_widget(get_footer())
    return root


def create_database_folder() -> None:
    if not os.path.exists("db"):
        os.makedirs("db")


# Datetime utils
def convert_active_time_to_datetime(date_list: list) -> datetime.datetime:
    current_datetime = datetime.datetime.strptime(
        '-'.join([str(i) for i in date_list]),
        "%d-%m-%Y"
    )
    return current_datetime


def format_timedelta(delta: datetime.timedelta) -> str:
    total_seconds = delta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    pretty_time = f"{int(minutes)} m, {f'0{int(seconds)}' if int(seconds) < 10 else int(seconds)}s"
    if hours:
        pretty_time = f"{int(hours)} h, {pretty_time}"
    return pretty_time


def datetime_from_string(str_datetime: str) -> datetime.datetime:
    dt = datetime.datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S.%f')
    return dt
