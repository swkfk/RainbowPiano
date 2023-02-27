from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class ColoredLabel(QLabel):

    def __init__(self, text="", parent=None, color: QColor = None,
                 geometry: tuple[int, int, int, int] = (0, 0, 100, 80),
                 align: str = "mm"):
        super().__init__(text, parent)
        if color is not None:
            self.set_color(color)
        self.set_font()
        self.setGeometry(*geometry)
        alignment = {
            "l": Qt.AlignmentFlag.AlignLeft,
            "m": Qt.AlignmentFlag.AlignHCenter,
            "r": Qt.AlignmentFlag.AlignRight
        }[align[0]]
        alignment |= {
            "t": Qt.AlignmentFlag.AlignTop,
            "m": Qt.AlignmentFlag.AlignVCenter,
            "b": Qt.AlignmentFlag.AlignBottom
        }[align[1]]
        self.setAlignment(alignment)

    def set_color(self, background_color: QColor, text_color: QColor = QColor(0, 0, 0)) -> tuple[QColor, QColor]:
        self.setAutoFillBackground(True)
        palette = self.palette()
        old_background_color = palette.color(self.backgroundRole())
        palette.setColor(self.backgroundRole(), background_color)
        old_text_color = palette.color(self.foregroundRole())
        palette.setColor(self.foregroundRole(), text_color)
        self.setPalette(palette)
        return old_background_color, old_text_color

    def set_font(self, size: int = 20, weight: int = 500):
        ft = QFont()
        ft.setWeight(weight)
        ft.setPointSize(size)
        self.setFont(ft)
