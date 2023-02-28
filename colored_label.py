from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtProperty


class ColoredLabel(QLabel):

    def __init__(self, text="", parent=None, color: QColor = None,
                 geometry: tuple[int, int, int, int] = (0, 0, 100, 80),
                 align: str = "mm"):
        super().__init__(text, parent)
        if color is not None:
            self.set_color(color)
        self.set_font()
        self.setGeometry(*geometry)
        alignment = AlignedLabel.get_alignment(align)
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

    def _set_background_color(self, background_color: QColor):
        self.set_color(background_color, self.palette().color(self.foregroundRole()))

    color_anim = pyqtProperty(QColor, fset=_set_background_color)

    def set_font(self, size: int = 20, weight: int = 500):
        ft = QFont()
        ft.setWeight(weight)
        ft.setPointSize(size)
        self.setFont(ft)


class AlignedLabel(QLabel):
    def __init__(self, parent, align="lm"):
        super().__init__(parent)
        self.setAlignment(self.get_alignment(align))

    @staticmethod
    def get_alignment(align_string):
        alignment = {
            "l": Qt.AlignmentFlag.AlignLeft,
            "m": Qt.AlignmentFlag.AlignHCenter,
            "r": Qt.AlignmentFlag.AlignRight
        }[align_string[0]]
        alignment |= {
            "t": Qt.AlignmentFlag.AlignTop,
            "m": Qt.AlignmentFlag.AlignVCenter,
            "b": Qt.AlignmentFlag.AlignBottom
        }[align_string[1]]
        return alignment
