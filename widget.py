import os.path

from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QSlider, QPushButton, QFileDialog
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt, QUrl, QPropertyAnimation, pyqtSignal

import color_palette
import consts
from colored_label import ColoredLabel, AlignedLabel
from auto_play import AutoPlayThread


class MainWidget(QWidget):
    pausePlay = pyqtSignal()
    resumePlay = pyqtSignal()
    loadPlay = pyqtSignal(str)
    changePlay = pyqtSignal(int)

    def __init__(self):
        super(MainWidget, self).__init__()

        # window information
        self.setWindowTitle(f"Rainbow Piano - PC edition - V{consts.__version__} - {consts.__author__}")
        self.setFixedSize(*consts.MainWindow.size)

        # window widgets
        self.label_center = ColoredLabel(
            text="", parent=self,
            color=QtGui.QColor(102, 204, 255),
            geometry=consts.MainWindow.Labels.main_geometry,
            align="rt"
        )
        self.label_center.set_color(QtGui.QColor(102, 204, 255), QtGui.QColor(0, 0, 0, 100))
        self.main_label_anim = QPropertyAnimation(self.label_center, b"color_anim")
        self.main_label_anim.setDuration(300)

        self.hint_labels = []
        for idx in range(7):
            tup = color_palette.RainbowColor.get_color_by_board(idx)
            # s_tup = ", ".join([str(ss).zfill(3) for ss in tup[1][0:3]])
            tone = color_palette.RainbowColor.get_tone_by_board(idx)
            self.hint_labels.append(
                ColoredLabel(
                    text=tone[0] + "\n\n" + "ZXCVBNM"[idx], parent=self,
                    color=QtGui.QColor(*tup[1]),
                    geometry=consts.MainWindow.Labels.hint_geometry(idx),
                    align="mm",
                )
            )

        # auto_play widgets
        self.play_slide = QSlider(Qt.Orientation.Horizontal, self)
        self.play_slide.setGeometry(*consts.MainWindow.AutoPlay.slider_geometry)
        self.play_slide.setStyleSheet(consts.Style.slider)
        self.play_slide.setRange(0, 65535)
        self.play_slide.setValue(0)
        self.play_slide.setEnabled(False)
        self.play_button = QPushButton("播放", self)
        self.play_button.setEnabled(False)
        self.play_button.setGeometry(*consts.MainWindow.AutoPlay.play_geometry)
        self.info_label = AlignedLabel(self, "rm")
        self.info_label.setGeometry(*consts.MainWindow.AutoPlay.info_geometry)
        self.load_button = QPushButton("载入文件", self)
        self.load_button.setGeometry(*consts.MainWindow.AutoPlay.load_geometry)
        self.file_label = AlignedLabel(self, "lm")
        self.file_label.setGeometry(*consts.MainWindow.AutoPlay.file_geometry)
        self.file_label.setWordWrap(True)

        # auto_play thread
        self.autoplay_thread = AutoPlayThread(self, self.pausePlay, self.resumePlay, self.changePlay,
                                              self.loadPlay)

        # signal & slot
        self.autoplay_thread.keyPressed.connect(lambda x: self.key_pressed("ZXCVBNM"[x]))
        self.autoplay_thread.loadDown.connect(self.load_down)
        self.autoplay_thread.playChange.connect(self.play_slide.setValue)
        self.autoplay_thread.overSignal.connect(self.play_over)
        self.play_slide.valueChanged.connect(lambda x: self.changePlay.emit(x))
        self.play_button.clicked.connect(self.play_button_pressed)
        self.load_button.clicked.connect(self.choose_file)

        # show window
        self.show()
        self.autoplay_thread.start()

    def play_over(self):
        self.play_button.setText("播放")
        # FIXME: 在最后一个音暂停会导致“播放”可被再次按下

    def play_button_pressed(self):
        if self.play_button.text() == "播放":
            self.resumePlay.emit()
            self.play_button.setText("暂停")
        else:
            self.pausePlay.emit()
            self.play_button.setText("播放")

    def choose_file(self):
        url = QFileDialog.getOpenFileUrl(
            self, "选择打开的录制文件",
            QUrl.fromLocalFile("music"), "(*.mnote)"
        )[0].path()[1:]

        if os.path.exists(url):
            self.loadPlay.emit(url)
            self.file_label.setText(url)
        else:
            print(f"invalid url: <{url}>")

    def load_down(self, text, val):
        self.play_slide.setEnabled(True)
        self.play_slide.setMaximum(val - 1)
        self.play_button.setEnabled(True)
        self.play_button.setText("播放")
        self.info_label.setText(text)
        self.pausePlay.emit()
        self.changePlay.emit(0)

    def key_pressed(self, key: str):
        print(key)
        brd = "ZXCVBNM".index(key)
        tup = color_palette.RainbowColor.get_color_by_board(brd)
        s_tup = ", ".join([str(ss).zfill(3) for ss in tup[1][0:3]])
        tone = color_palette.RainbowColor.get_tone_by_board(brd)

        self.label_center.setText(f"{tone[0]} 🎵 {tup[0]}: RGB({s_tup})")

        self.main_label_anim.setStartValue(self.label_center.palette().color(self.label_center.backgroundRole()))
        self.main_label_anim.setEndValue(QtGui.QColor(*tup[1]))

        sound = QSoundEffect(self)
        sound.setSource(QUrl.fromLocalFile(".\\sound\\" + tone[1]))
        sound.setLoopCount(1)
        sound.setVolume(1)

        self.main_label_anim.start()
        sound.play()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.isAutoRepeat():
            return
        key = a0.key()
        match key:
            case Qt.Key.Key_Z | Qt.Key.Key_1:
                self.key_pressed("Z")
            case Qt.Key.Key_X | Qt.Key.Key_2:
                self.key_pressed("X")
            case Qt.Key.Key_C | Qt.Key.Key_3:
                self.key_pressed("C")
            case Qt.Key.Key_V | Qt.Key.Key_4:
                self.key_pressed("V")
            case Qt.Key.Key_B | Qt.Key.Key_5:
                self.key_pressed("B")
            case Qt.Key.Key_N | Qt.Key.Key_6:
                self.key_pressed("N")
            case Qt.Key.Key_M | Qt.Key.Key_7:
                self.key_pressed("M")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.autoplay_thread.terminate()
        a0.accept()
