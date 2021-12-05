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
from kivy.clock import Clock

from app.utils import build_screen, format_timedelta, datetime_from_string
from app.database import get_day_info_by_date, get_all_pupils, get_qr_code_record


class MissingDevicesScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.date_today = None
        self.day_info = None
        self.pupils_who_pass_phone_list = None
        self.pupils_who_late_list = None
        self.pupils_who_did_not_pass_phone_list = None
        self.did_not_pass_phones_lay = None
        self.schedule_event = None

    def on_enter(self, *args):
        body = BoxLayout()
        body.add_widget(self.build_missing_devices_menu())
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def on_leave(self, *args):  # TODO: add to all screens
        self.clear_widgets()
        self.schedule_event.cancel()

    def build_missing_devices_menu(self) -> AnchorLayout:
        self.date_today = datetime.datetime.now()
        self.day_info = get_day_info_by_date(date=self.date_today.date())
        print(f"day_info: {self.day_info}")
        anchor_lay = AnchorLayout(anchor_x="center", anchor_y="center")

        if self.day_info:
            box_lay = BoxLayout(orientation="vertical", size_hint=(0.9, 0.8))
            scroll_lay = ScrollView(size_hint_y=1, do_scroll_x=False)
            grid_lay = GridLayout(size_hint_y=None, cols=1)
            grid_lay.bind(minimum_height=grid_lay.setter('height'))

            self.pupils_who_pass_phone_list = []
            self.pupils_who_late_list = []
            self.pupils_who_did_not_pass_phone_list = []

            all_pupils = get_all_pupils()
            self.sort_pupils(all_pupils)
            print(
                f"pupils_who_pass_phone_list: {self.pupils_who_pass_phone_list}\n\n"
                f"pupils_who_late_list: {self.pupils_who_late_list}\n\n"
                f"pupils_who_did_not_pass_phone_list: {self.pupils_who_did_not_pass_phone_list}"
            )
            self.display_pupils_list_on_grid(grid_lay=grid_lay)
            scroll_lay.add_widget(grid_lay)
            box_lay.add_widget(scroll_lay)
            anchor_lay.add_widget(box_lay)
            self.schedule_event = Clock.schedule_interval(self.update_missed_time_difference, 1)
        else:
            anchor_lay.add_widget(Label(text="No phones today!"))
        return anchor_lay

    def display_pupils_list_on_grid(self, grid_lay: GridLayout) -> None:
        pass_phones_lay = self.build_pupil_grid_items(
            pupil_group_data=self.pupils_who_pass_phone_list,
        )
        late_lay = self.build_pupil_grid_items(
            pupil_group_data=self.pupils_who_late_list,
        )
        self.did_not_pass_phones_lay = self.build_pupil_grid_items(
            pupil_group_data=self.pupils_who_did_not_pass_phone_list
        )
        grid_lay.add_widget(pass_phones_lay)
        grid_lay.add_widget(Label(text="Missing devices", size_hint_y=None, height=30))  # Separator
        grid_lay.add_widget(late_lay)
        grid_lay.add_widget(self.did_not_pass_phones_lay)

    def sort_pupils(self, pupils: dict) -> None:
        """
        Add pupil data {"name": str, "late": bool, "date_diff": datetime} to needed list
        """
        for pupil_name in pupils:
            pupil_data = pupils.get(pupil_name)
            pupil_name = pupil_data.get("name")
            pupil_qr_code = pupil_data.get("qr_code")
            active_day_info = self.day_info.get("datetime")
            active_day_datetime = datetime_from_string(str_datetime=active_day_info)
            qr_code_record = get_qr_code_record(date=self.date_today.date(), qr_code=pupil_qr_code)
            if qr_code_record:
                qr_code_record_datetime = qr_code_record.get("datetime")
                datetime_moment = datetime_from_string(str_datetime=qr_code_record_datetime)
            else:
                datetime_moment = datetime.datetime.now()
            is_late = True if datetime_moment > active_day_datetime else False
            if is_late:
                date_difference = datetime_moment - active_day_datetime
            else:
                date_difference = active_day_datetime - datetime_moment

            data_to_save = {"name": pupil_name, "late": is_late, "date_diff": date_difference}
            print(f"datetime_moment: {datetime_moment}, {active_day_datetime}, date_difference: {date_difference}")
            if qr_code_record:
                if is_late:
                    self.pupils_who_late_list.append(data_to_save)
                    continue
                self.pupils_who_pass_phone_list.append(data_to_save)
            else:
                self.pupils_who_did_not_pass_phone_list.append(data_to_save)

    def build_pupil_grid_items(self, pupil_group_data: dict) -> BoxLayout:
        """
        Add pupil label with difference time and pupil name to group lay
        """
        group_lay = GridBoxLayout()
        default_item_height = 30
        total_lay_height = 0
        for pupil_data in pupil_group_data:
            if pupil_data and isinstance(pupil_data, dict):
                name = pupil_data.get("name")
                late = pupil_data.get("late")
                date_diff = pupil_data.get("date_diff")
                data_list_item = BoxLayout(orientation='horizontal', height=default_item_height, size_hint_y=None)
                data_list_item.add_widget(PupilLabel(text=name, size_hint_x=.75))
                text_color = (1, 1, 1, .5)
                if late:
                    text_color = (1, 0, 0, 1)
                time_diff_label = TimeDiffLabel(size_hint_x=.25, color=text_color)
                print(f"date_diff: {date_diff}")
                time_diff_label.change_label_text(delta_time=date_diff)
                data_list_item.add_widget(time_diff_label)
                total_lay_height += default_item_height
                group_lay.add_widget(data_list_item)
        group_lay.height = total_lay_height
        return group_lay

    def update_missed_time_difference(self, *args) -> None:
        for grid_item in self.did_not_pass_phones_lay.children:
            time_label = grid_item.children[0]
            new_delta = time_label.current_delta + datetime.timedelta(seconds=1)
            time_label.change_label_text(delta_time=new_delta)


class PupilLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = "left"
        self.valign = "middle"

    def on_size(self, *args):
        self.text_size = self.size


class TimeDiffLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_delta = None
        self.halign = "right"
        self.valign = "middle"

    def on_size(self, *args):
        self.text_size = self.size

    def change_label_text(self, delta_time: datetime.timedelta):
        self.current_delta = delta_time
        self.text = format_timedelta(delta=delta_time)


class GridBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 0
