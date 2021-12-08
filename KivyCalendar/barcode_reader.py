from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar import pyzbar
import cv2


class CameraScreen(Screen):
    # first screen that is displayed when program is run
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = self.setup_camera()
        self.img = None

    def setup_camera(self):
        camera = cv2.VideoCapture(0)  # start OpenCV camera
        camera.set(3, 1280)  # set resolution of camera
        camera.set(4, 720)
        self.img = Image()  # Image widget to display frames

        self.add_widget(self.img)
        Clock.schedule_interval(self.update, 1.0 / 30)  # update for 30fps
        return camera

    def on_enter(self, *args):
        self.build_camera_screen()

    def on_leave(self, *args):
        self.clear_widgets()

    def build_camera_screen(self):
        box_lay = BoxLayout(orientation='vertical')
        box_lay.add_widget(self.img)
        self.add_widget(box_lay)

    # update frame of OpenCV camera
    def update(self, dt):
        ret, frame = self.cam.read()  # retrieve frames from OpenCV camera

        if ret:
            buf1 = cv2.flip(frame, 0)  # convert it into texture
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = image_texture  # display image from the texture

            barcodes = pyzbar.decode(frame)  # detect barcode from image
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                self.change_screen(barcode=barcodeData)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                exit(0)

    def stop_stream(self, *args):
        self.cam.release()  # stop camera
