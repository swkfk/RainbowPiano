# 又是被多线程薄纱的一天 TAT
import os.path

import cv2
import numpy as np
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QWidget

import color_palette
import read_mnote
from color_palette import RainbowColor


def rgb_to_bgr(rgb: tuple[int, int, int]):
    return rgb[2], rgb[1], rgb[0]


class VideoProcessThread(QThread):
    processUpdate = pyqtSignal(int)
    processShow = pyqtSignal(str)
    processOver = pyqtSignal()

    def __init__(self, q_parent):
        super().__init__()
        self.output_name = None
        self.info = None
        self.notes = None
        self.video = None
        self.notes = None
        self.parent: QWidget = q_parent
        self.blank_image = np.zeros((1080, 1920, 3), np.uint8)
        self.images = []
        font = cv2.FONT_HERSHEY_COMPLEX
        for idx, (name, clr) in enumerate(RainbowColor.color_lst):
            self.images.append(np.zeros((1080, 1920, 3), np.uint8))
            self.images[-1][:] = list(rgb_to_bgr(clr))
            cv2.putText(
                self.images[-1],
                color_palette.RainbowColor.tone_lst[idx][0] + " " + color_palette.RainbowColor.eng_name[idx],
                (10, 80), font, 3, (0, 0, 0), 1
            )

    # def prepare_to_start(self, input_name, output_name):
    #     self.progress_bar = QProgressDialog(self.parent)
    #     self.video = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*"mp4v"), 30, (1920, 1080), True)
    #     self.info, self.notes = read_mnote.mnote_reader(input_name)
    #     self.output_name = output_name
    #     self.progress_bar.setRange(0, len(self.notes))
    #     self.progress_bar.setLabelText(f"输入：{input_name}\n输出：{output_name}")
    #     self.in_process = True

    def insert_note(self, input_name, output_name):
        self.info, self.notes = read_mnote.mnote_reader(input_name)
        self.video = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*"mp4v"), 30, (1920, 1080), True)

    def run(self):
        for idx, note in enumerate(self.notes):
            for _ in range(int(
                    read_mnote.note_width_ms(self.info['bpm'], self.info['beat'], note[1]) / 1000 * 30
            )):
                self.video.write(self.images[note[0] - 1])
            for _ in range(5):
                self.video.write(self.blank_image)
            self.processUpdate.emit(idx + 1)
        self.video.release()


# test
if __name__ == "__main__":
    images = []
    for name_, clr_ in RainbowColor.color_lst:
        images.append(np.zeros((1080, 1920, 3), np.uint8))
        images[-1][:] = list(rgb_to_bgr(clr_))

    video = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (1920, 1080), True)

    for i in range(7):
        video.write(images[i])

    video.release()
