from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar import pyzbar
import cv2

from app.utils import screen_manager, build_screen
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
        first_name = data.get("first name")
        phone_number = data.get("phone number")
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


# Read qr screen
class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = Image()  # Image widget to display frames
        self.camera = None
        self.update_event = None
        self.need_update = True

    def setup_camera(self):
        """Setup OpenCV camera resolution"""
        self.camera = cv2.VideoCapture(0)  # start OpenCV camera
        self.camera.set(3, 640)  # set resolution of camera
        self.camera.set(4, 640)
        self.need_update = True
        self.update_event = Clock.schedule_interval(self.update_camera_frame, 1.0 / 30)  # update for 30fps

    def on_enter(self, build: bool = False, *args):
        self.setup_camera()
        body = self.build_camera_screen()
        root = body
        if build:
            root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def on_leave(self, *args):
        self.clear_widgets()
        if self.update_event:
            self.update_event.cancel()
        self.need_update = False
        cv2.destroyAllWindows()
        self.camera = None

    def build_camera_screen(self):
        """Create screen layout"""
        box_lay = BoxLayout(orientation='vertical')
        box_lay.add_widget(self.img)
        return box_lay

    def update_camera_frame(self, dt: float):
        """Update frame of OpenCV camera"""
        if self.need_update:
            success, frame = self.camera.read()  # retrieve frames from OpenCV camera
            if success:
                buf1 = cv2.flip(frame, 0)  # convert it into texture
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img.texture = image_texture  # display image from the texture

                barcodes = pyzbar.decode(frame)  # detect barcode from image
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    text = "{} ({})".format(barcode_data, barcode_type)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    if barcode_data:
                        self.need_update = False
                        print(f"change screen")
                        self.change_screen(barcode=barcode_data)
                        if self.update_event:
                            self.update_event.cancel()
                        cv2.destroyAllWindows()

    def change_screen(self, barcode: str) -> None:
        print(f"qr_code_data: {barcode}")
        self.change_to_process_qr_code_screen(qr_code_data=barcode)
