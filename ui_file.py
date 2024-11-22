import sys
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtCore import *


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test')
        self.setup()

    def setup(self):
        self.btn = QPushButton(self)
        self.setGeometry(0, 0, 500, 500)
        self.btn.setText("push")
        self.btn.move(20, 20)
        self.btn.resize(100, 100)
        self.player = QMediaPlayer()
        self.out = QAudioOutput()
        self.player.setAudioOutput(self.out)
        self.player.positionChanged.connect(self.positionChanged)
        path = "files/sample-3s.mp3"
        self.player.setSource(QUrl.fromLocalFile(path))
        self.out.setVolume(50)
        self.btn.clicked.connect(self.run)

    def run(self):
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    ex.show()
    sys.exit(app.exec())
