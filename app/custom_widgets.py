from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.clock import Clock

from app.utils import screen_manager
from app.database import create_new_pupil


class MenuButton(Button):
    def __init__(self, screen_name: str, **kwargs):
        super().__init__(**kwargs)
        self.text = screen_name

    def on_release(self):
        screen_manager.current = self.text


class CustomTextInput(TextInput):
    def __init__(self, key: str, **kwargs):
        super().__init__(**kwargs)
        self.key = key


class RegisterNewPupilButton(Button):
    """
    Save pupil data to database and show result notification
    """
    def __init__(self, text_inputs: list, nl: Label, **kwargs):
        super().__init__(**kwargs)
        self.text = "Create new pupil"
        self.text_inputs = text_inputs
        self.notification_label = nl

    def on_release(self):
        self.validate_text_input_data()

    def validate_text_input_data(self) -> None:
        pupil_data = {}
        missed_fields = []
        # Checking is all text input fields valid
        for text_input in self.text_inputs:
            line_text = text_input.text
            if not line_text:
                missed_fields.append(text_input.key)
            else:
                pupil_data[text_input.key] = text_input.text
        # Show notification result and save to database
        if missed_fields:
            self.show_fail_message(missed_fields=missed_fields)
        else:
            self.save_pupil_data_to_database(data=pupil_data)
            self.show_success_message()
        # Remove notification after specified time
        Clock.schedule_once(self.notification_remove_callback, 3)

    def save_pupil_data_to_database(self, data: dict) -> None:
        name = data.get("name")
        first_name = data.get("first_name")
        phone_number = data.get("phone_number")
        create_result = create_new_pupil(name=name, first_name=first_name, phone_number=phone_number)
        if not create_result:
            self.show_fail_message(extra_message="Save pupils to database error !")

    def show_success_message(self) -> None:
        self.notification_label.color = (0, 1, 0)
        self.notification_label.text = "You have successfully created a new pupil !"

    def show_fail_message(self, missed_fields: list = None, extra_message: str = None) -> None:
        self.notification_label.color = (1, 0, 0)
        fail_message = f"You need to fill this fields: {', '.join([*missed_fields])}"
        if extra_message:
            fail_message = extra_message
        self.notification_label.text = fail_message

    def notification_remove_callback(self, dt: float) -> None:
        """Remove notification after showing"""
        self.notification_label.text = ""



