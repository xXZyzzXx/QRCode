from app import database
from app.custom_widgets import CameraScreen
from app.utils import Screens


class ReadQRCodeScreen(CameraScreen):
    """
    Reading QR code data and add
    """
    def on_enter(self, *args):
        super(ReadQRCodeScreen, self).on_enter(build=True, *args)

    def change_to_process_qr_code_screen(self, qr_code_data: str) -> None:
        database.add_qr_code_record(qr_code=qr_code_data)
        self.manager.current = Screens.MENU
