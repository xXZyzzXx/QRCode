import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from app.utils import build_screen
from app.database import get_day_info_by_date, get_all_pupils, get_qr_code_record


class MissingDevicesScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.grid_lay = None
        self.date_today = None
        self.day_info = None
        self.pupils_who_did_not_pass_phones_dict = None

    def on_enter(self, *args):
        body = BoxLayout()
        body.add_widget(self.build_missing_devices_menu())
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def build_missing_devices_menu(self) -> AnchorLayout:
        self.date_today = datetime.datetime.now()
        self.day_info = get_day_info_by_date(date=self.date_today.date())
        print(f"day_info: {self.day_info}")
        anchor_lay = AnchorLayout(anchor_x="center", anchor_y="center")

        if self.day_info:
            box_lay = BoxLayout(orientation="vertical", size_hint=(0.9, 0.8))
            scroll_lay = ScrollView(size_hint_y=.85, do_scroll_x=False, bar_inactive_color=(.7, .7, .7, .5))
            self.grid_lay = GridLayout(size_hint_y=None, cols=1)
            self.grid_lay.bind(minimum_height=self.grid_lay.setter('height'))
            all_pupils = get_all_pupils()

            self.pupils_who_did_not_pass_phones_dict = {}

            self.build_pupils_handle_data(all_pupils)  # Create pupils who handed devices
            self.grid_lay.add_widget(Label(text="separator", size_hint_y=None, height=30))
            if self.pupils_who_did_not_pass_phones_dict:  # Create pupils who does not hand devices
                self.build_pupils_handle_data(self.pupils_who_did_not_pass_phones_dict, text_color=(1, 0, 0, 1))

            print(f"pupils_who_did_not_pass_phones_dict: {self.pupils_who_did_not_pass_phones_dict}")

            scroll_lay.add_widget(self.grid_lay)
            box_lay.add_widget(scroll_lay)
            anchor_lay.add_widget(box_lay)
        else:
            anchor_lay.add_widget(Label(text="No phones today!"))

        return anchor_lay

    def build_pupils_handle_data(self, pupils: dict, text_color=(1, 1, 1, .5)):
        print(f"Second")
        for pupil_name in pupils:
            pupil_data = pupils.get(pupil_name)
            pupil_name = pupil_data.get("name")
            pupil_first_name = pupil_data.get("first_name")
            pupil_phone_number = pupil_data.get("phone_number")
            pupil_qr_code = pupil_data.get("qr_code")
            qr_code_record = get_qr_code_record(date=self.date_today.date(), qr_code=pupil_qr_code)
            # TODO: не создаётся остальная часть, проверить время
            if qr_code_record:
                qr_code_record_datetime = qr_code_record.get("datetime")
                active_day_info = self.day_info.get("datetime")
                qr_datetime = datetime.datetime.strptime(qr_code_record_datetime, '%Y-%m-%d %H:%M:%S.%f')
                active_day_datetime = datetime.datetime.strptime(active_day_info, '%Y-%m-%d %H:%M:%S.%f')
                time_difference = qr_datetime - active_day_datetime
                pretty_time_difference = self.chop_microseconds(time_difference)
                print(f"qr_code_record_datetime: {qr_datetime}, active_day_datetime: {active_day_datetime}")
                pupil_display_data = f"{pupil_name}, {pupil_first_name}, {pupil_phone_number}"
                grid_box = BoxLayout(orientation='horizontal', height=30, size_hint_y=None)
                grid_box.add_widget(PupilLabel(text=pupil_display_data, size_hint_x=.8))
                grid_box.add_widget(Label(text=pretty_time_difference, size_hint_x=.2, color=text_color))
                self.grid_lay.add_widget(grid_box)
            else:
                self.pupils_who_did_not_pass_phones_dict[pupil_name] = pupil_data

    def chop_microseconds(self, delta):
        return str(delta - datetime.timedelta(microseconds=delta.microseconds))


class PupilLabel(Label):
    def on_size(self, *args):
        self.halign = "left"
        self.valign = "middle"
        self.text_size = self.size
