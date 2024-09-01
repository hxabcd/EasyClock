import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore  as qtc
import qfluentwidgets as qfw
from qframelesswindow.utils import getSystemAccentColor
import time


class Stopwatch(qtw.QWidget):
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.stop_time = time.time()

    def get(self):
        return self.stop_time - self.start_time

    def getf(self):
        tmp = self.get()
        return "%02d:%02d:%06.3f" % (tmp // 60 // 60, tmp // 60 % 60, tmp % 60 % 60)


class Control(qtw.QWidget):
    def __init__(self, timer: Stopwatch):
        super().__init__()
        self.timer = timer
        self.setObjectName("Stopwatch")

        self.title = qfw.TitleLabel("Stopwatch", self)
        self.timing = qtw.QWidget()
        self.label = qfw.BodyLabel("Click to start", self.timing)
        self.button = qfw.PushButton("Start", self)
        self.button.clicked.connect(self.change_text)

        self.timing_layout = qtw.QHBoxLayout()
        self.timing_layout.addWidget(self.label)
        self.timing_layout.addWidget(self.button)
        self.timing.setLayout(self.timing_layout)

        self.show_layout = qtw.QVBoxLayout()
        self.show_layout.addWidget(self.title)
        self.show_layout.setAlignment(self.title, qtc.Qt.AlignmentFlag.AlignTop)
        self.show_layout.addWidget(self.timing)
        self.setLayout(self.show_layout)

    def change_text(self):
        print("Change text", end=" - ")
        if self.button.text() == "Start":
            print("Started")
            self.button.setText("Stop")
            self.label.setText("Click to stop")
            self.timer.start()
        else:
            print("Stopped")
            self.button.setText("Start")
            self.label.setText("Click to Start")
            self.timer.stop()
            self.showResult()

    def showResult(self):
        # self.msgbox.information(self, 'EasyTimer', 'Finished: %s' % self.timer.getf(), qtw.QMessageBox.StandardButton.Ok)
        qfw.Flyout.create(
            icon=qfw.InfoBarIcon.SUCCESS,
            title="Finished",
            content=self.timer.getf(),
            target=self.button,
            parent=self,
            isClosable=True,
        )


class About(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("About")

        self.title = qfw.TitleLabel("About", self)
        self.text = qfw.BodyLabel("A clock application based on PyQt6 and PyQt6-Fluent-Widgets.", self)
        self.author = qfw.BodyLabel("Author: HxAbCd", self)
        self.text.setWordWrap(True)

        self.show_layout = qtw.QVBoxLayout()
        self.show_layout.addWidget(self.title)
        self.show_layout.setAlignment(self.title, qtc.Qt.AlignmentFlag.AlignTop)
        self.show_layout.addWidget(self.text)
        self.show_layout.addWidget(self.author)
        self.setLayout(self.show_layout)



class MainWindow(qfw.FluentWindow):
    def __init__(self):
        super().__init__()
        # self.resize(360, 240)
        self.setFixedWidth(360)
        self.setFixedHeight(240)
        self.setWindowTitle("EasyClock")
        
        qfw.setTheme(qfw.Theme.AUTO)
        if sys.platform in ["win32", "darwin"]:
            qfw.setThemeColor(getSystemAccentColor(), save=False)

        timer = Stopwatch()
        control = Control(timer)
        about = About()
        self.addSubInterface(
            interface=control,
            icon=qfw.FluentIcon.STOP_WATCH,
            text="Stopwatch",
        )
        self.addSubInterface(
            interface=about,
            icon=qfw.FluentIcon.INFO,
            text="About",
        )


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
