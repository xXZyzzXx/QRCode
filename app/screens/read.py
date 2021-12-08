from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy_garden.zbarcam import ZBarCam

from app.utils import build_screen
from app.database import add_qr_code_record


class ReadQRCodeScreen(Screen):
    """
    Reading QR code data and add
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.qr_code_input = None

    def on_enter(self, *args):
        body = BoxLayout(orientation='vertical')
        body.add_widget(self.build_test_qr_code_screen())

        try:
            body.add_widget(ZBarCam())
        except Exception as e:
            import traceback
            print(f"Add ZBarCam widget error: {e}, ")  # {traceback.format_exc()}

        root = build_screen(screen_name=self.name, body=body)
        self.add_widget(root)

    def on_leave(self, *args):
        self.clear_widgets()

    def build_test_qr_code_screen(self) -> AnchorLayout:
        """Building read qr code menu skeleton"""
        root = AnchorLayout(anchor_x="center", anchor_y="center")
        box_lay = BoxLayout(orientation="vertical", size_hint=(.6, .2))
        read_qr_btn = Button(text="Add QR code datetime record", size_hint=(1, .5))
        read_qr_btn.bind(
            on_release=lambda _: self.test_get_qr_code_data()
        )
        box_lay.add_widget(read_qr_btn)
        self.qr_code_input = TextInput()
        box_lay.add_widget(self.qr_code_input)
        root.add_widget(box_lay)
        return root

    def test_get_qr_code_data(self):
        """Temporary method for emulate qr-code answer"""
        qr_code = self.qr_code_input.text
        add_qr_code_record(qr_code=qr_code)
