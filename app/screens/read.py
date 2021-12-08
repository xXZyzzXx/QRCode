from app import database
from app.custom_widgets import CameraScreen


class ReadQRCodeScreen(CameraScreen):
    """
    Reading QR code data and add
    """
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        # self.skip_reading_qr_for_test()
        print(f"on_enter")
        super(ReadQRCodeScreen, self).on_enter(build=True, *args)

    def change_to_process_qr_code_screen(self, qr_code_data: str) -> None:
        database.add_qr_code_record(qr_code=qr_code_data)
