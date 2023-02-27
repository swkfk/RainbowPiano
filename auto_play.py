from PyQt6.QtCore import QThread, pyqtSignal

from read_mnote import mnote_reader


class AutoPlayThread(QThread):
    keyPressed = pyqtSignal(int)
    loadDown = pyqtSignal(str)

    def __init__(self, parent, pause_signal, resume_signal, change_signal, load_signal):
        super().__init__(parent)
        self.parent = parent
        self.pause_signal = pause_signal
        self.resume_signal = resume_signal
        self.change_signal = change_signal
        self.load_signal = load_signal

        self.pause_signal.connect(self.pause)
        self.resume_signal.connect(self.resume)
        self.change_signal.connect(self.change)
        self.load_signal.connect(self.load)

        self.on_play = False
        self.play_idx = 0
        self.info = {}
        self.note = []

    def load(self, path):
        self.play_idx = 0
        self.info, self.note = mnote_reader(path)
        self.loadDown.emit(f"《{self.info['title']}》 {self.info['author']} {self.info['bpm']} BPM")

    def run(self) -> None:
        while True:
            if not self.on_play or self.play_idx >= len(self.note):
                self.msleep(100)
                continue
            self.keyPressed.emit(self.note[self.play_idx][0] - 1)  # This -1 is important!
            self.msleep(int(60000 / (self.info["bpm"] * self.info["beat"]) * self.note[self.play_idx][1]))
            self.play_idx += 1

    def pause(self):
        self.on_play = False

    def resume(self):
        self.on_play = True

    def change(self, val: int):
        pass
