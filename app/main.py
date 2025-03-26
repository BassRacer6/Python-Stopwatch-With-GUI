import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame,
                             QLabel, QPushButton, QVBoxLayout,QHBoxLayout)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QIcon, QFont, QFontDatabase

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        screen = QApplication.instance().primaryScreen()
        screenGeometry = screen.geometry()
        screenWidth = screenGeometry.width()
        screenHeight = screenGeometry.height()
        windowWidth = 500
        windowHeight = 200
        x = (screenWidth - windowWidth) // 2
        y = (screenHeight - windowHeight) // 2
        self.setGeometry(x, y, windowWidth, windowHeight)

        self.time = QTime(0,0,0,0)
        self.timeLabel = QLabel("00:00:00:00", self)
        self.startButton = QPushButton("Start")
        self.pauseButton = QPushButton("Pause")
        self.resetButton = QPushButton("Reset")
        self.timer = QTimer(self)
        self.running = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stopwatch")
        self.setWindowIcon(QIcon("WatchIcon.png"))

        vbox = QVBoxLayout()
        vbox.addWidget(self.timeLabel)
        vbox.addWidget(self.startButton)
        vbox.addWidget(self.pauseButton)
        vbox.addWidget(self.resetButton)
        self.setLayout(vbox)

        self.timeLabel.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.pauseButton)
        hbox.addWidget(self.resetButton)
        vbox.addLayout(hbox)

        #fontId = QFontDatabase.addApplicationFont("RobotoMono.ttf")
        #fontFamily = QFontDatabase.applicationFontFamilies(fontId)[0]
        #digitalFont = QFont(fontFamily, 150, QFont.Bold)
        #self.timeLabel.setFont(digitalFont)

        self.setStyleSheet("""
            QPushButton, QLabel {
                font-weight: bold;
                border: 4px outset gray;
                background-color: lightgray;
                padding: 20px;
                color: rgb(0,0,0,200);
                }       
            QPushButton{
                font-family: monospace;
                font-size: 30px;
            }
            QPushButton:pressed {
                border: 4px inset gray;
                background-color: gray;
            }
            QLabel{
                font-family: monospace;
                font-size: 60px;
            }
        """)

        self.startButton.clicked.connect(self.start)
        self.pauseButton.clicked.connect(self.pause)
        self.resetButton.clicked.connect(self.reset)
        self.timer.timeout.connect(self.updateDisplay)

    def start(self):
        if not self.running:
            self.timer.start(10)
            self.running = True

    def pause(self):
        if self.running:
            self.timer.stop()
            self.running = False

    def reset(self):
        if not self.running:
            self.timer.stop()
            self.time = QTime(0, 0, 0, 0)
            self.timeLabel.setText(self.formatTime(self.time))
            self.running = False

    def formatTime(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:02}"
    
    def updateDisplay(self):
        self.time = self.time.addMSecs(10)
        self.timeLabel.setText(self.formatTime(self.time))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())