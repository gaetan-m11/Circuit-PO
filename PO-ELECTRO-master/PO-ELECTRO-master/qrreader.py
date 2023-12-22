import os
import time

import cv2
from timerV2 import RepeatedTimer

import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image

class QRReader:
    qr = None
    cam = None
    running = False

    def __init__(self):
        self.timer = None
        pass

    def get_qr(self):
        return self.qr

    def start_detection(self):
        self.cam = cv2.VideoCapture(0)
        self.running = True
        self.timer = RepeatedTimer(0.2, self.read)

    def stop_detection(self):
        self.cam.release()
        self.timer.stop()
        self.running = False

    def update_qr(self, qr):
        self.qr = qr

    def is_running(self):
        return self.running

    def read(self):
        result, image = self.cam.read()

        if result:
            # cv2.imshow("test", image)
            name = "tmp/" + str(time.perf_counter_ns()) + ".png"
            cv2.imwrite(name, image)
            #imwrite("current.png", image)

            # retval, decoded_info, points, straight_qrcode = self.qcd.detectAndDecodeMulti(image)
            #
            # print(retval, decoded_info)
            #
            # if retval:
            #     self.update_qr(decoded_info[0])
            decocdeQR = decode(Image.open(name))
            if len(decocdeQR) > 0:
                data = decocdeQR[0].data.decode('utf-8')
                # print(data)
                self.qr = data.split('/')[-1]
                # print("------", self.qr)

            # print(os.getcwd() + "/" + name)
            # time.sleep(.2)
            os.remove(os.getcwd() + "/" + name)

        else:
            print("couldn't capture image")

