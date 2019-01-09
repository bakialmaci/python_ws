import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        startButton = QPushButton('Start', self)
        startButton.clicked.connect(QApplication.instance().quit)
        startButton.resize(startButton.sizeHint())
        startButton.move(10, 470)
        stopButton = QPushButton('Stop', self)
        stopButton.clicked.connect(QApplication.instance().quit)
        stopButton.resize(stopButton.sizeHint())
        stopButton.move(100, 470)

        H_minColor = QLabel("H:", self)
        H_minColor.move(200, 475)
        H_minColorValue = QLabel("000", self)
        H_minColorValue.move(210, 475)

        S_minColor = QLabel("S:", self)
        S_minColor.move(240, 475)
        S_minColorValue = QLabel("000", self)
        S_minColorValue.move(250, 475)

        V_minColor = QLabel("V:", self)
        V_minColor.move(280, 475)
        V_minColorValue = QLabel("000", self)
        V_minColorValue.move(290, 475)

        H_maxColor = QLabel("H:", self)
        H_maxColor.move(350, 475)
        H_maxColorValue = QLabel("000", self)
        H_maxColorValue.move(360, 475)

        S_maxColor = QLabel("S:", self)
        S_maxColor.move(390, 475)
        S_maxColorValue = QLabel("000", self)
        S_maxColorValue.move(400, 475)

        V_maxColor = QLabel("V:", self)
        V_maxColor.move(430, 475)
        V_maxColorValue = QLabel("000", self)
        V_maxColorValue.move(440, 475)

        self.setGeometry(710, 290, 500, 500)
        self.setWindowTitle('Hunrobotx HSV Calculator')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
