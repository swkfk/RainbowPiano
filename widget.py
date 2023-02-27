from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt, QUrl

import color_palette
import consts
from colored_label import ColoredLabel


class MainWidget(QWidget):
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

        # show window
        self.show()

    def key_pressed(self, key: str):
        brd = "ZXCVBNM".index(key)
        tup = color_palette.RainbowColor.get_color_by_board(brd)
        s_tup = ", ".join([str(ss).zfill(3) for ss in tup[1][0:3]])
        tone = color_palette.RainbowColor.get_tone_by_board(brd)
        self.label_center.setText(f"{tone[0]} 🎵 {tup[0]}: RGB({s_tup})")
        self.label_center.set_color(QtGui.QColor(*tup[1]), QtGui.QColor(0, 0, 0, 100))
        sound = QSoundEffect(self)
        sound.setSource(QUrl.fromLocalFile(".\\sound\\" + tone[1]))
        sound.setLoopCount(1)
        sound.setVolume(1)
        sound.play()
        # sound.deleteLater()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        key = a0.key()
        match key:
            case Qt.Key.Key_Z:
                self.key_pressed("Z")
            case Qt.Key.Key_X:
                self.key_pressed("X")
            case Qt.Key.Key_C:
                self.key_pressed("C")
            case Qt.Key.Key_V:
                self.key_pressed("V")
            case Qt.Key.Key_B:
                self.key_pressed("B")
            case Qt.Key.Key_N:
                self.key_pressed("N")
            case Qt.Key.Key_M:
                self.key_pressed("M")

