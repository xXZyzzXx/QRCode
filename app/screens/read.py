from datetime import date, datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

from app.utils import build_screen
from app.database import add_qr_code_record


class ReadQRCodeScreen(Screen):
    def on_enter(self, *args):
        body = BoxLayout()
        # TODO: Custom logic, just in progress
        body.add_widget(self.build_test_qr_code_screen())
        """
        try:
            root.add_widget(ZBarCam())
        except Exception as e:
            print(f"Add ZBarCam widget error")
        """
        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def build_test_qr_code_screen(self) -> AnchorLayout:
        root = AnchorLayout(anchor_x="center", anchor_y="center")
        box_lay = BoxLayout(orientation="vertical")
        read_qr_btn = Button(text="Add QR code datetime record", size_hint=(.6, .25))
        read_qr_btn.bind(
            on_release=lambda _: self.test_get_qr_code_data()
        )
        box_lay.add_widget(read_qr_btn)
        self.qr_code_input = TextInput()
        box_lay.add_widget(self.qr_code_input)
        root.add_widget(box_lay)
        return root

    def test_get_qr_code_data(self):
        qr_code = self.qr_code_input.text
        add_qr_code_record(qr_code=qr_code)
