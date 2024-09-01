import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import qfluentwidgets as qfw
from qframelesswindow.utils import getSystemAccentColor
import time

from stopwatch_ui import Ui_Stopwatch


class Stopwatch(qtw.QWidget):
    def __init__(self):
        self.reset()

    def start(self):
        self.start_time = time.time()

    def pause(self):
        self.past_time = self.getnow()
        self.start_time = 0

    def reset(self):
        self.start_time = 0
        self.past_time = 0

    def get(self):
        return self.past_time

    def getnow(self):
        return time.time() - self.start_time + self.past_time

    def getf(self):
        return "%02d:%02d:%06.3f" % (
            self.past_time // 60 // 60,
            self.past_time // 60 % 60,
            self.past_time % 60 % 60,
        )


class StopwatchControl(qtw.QWidget, Ui_Stopwatch):
    def __init__(self, timer: Stopwatch):
        super().__init__()
        self.setObjectName("Stopwatch")
        
        self.setupUi(self)
        self.buttonSw.clicked.connect(self.buttonSwOnClick)
        self.buttonReset.clicked.connect(self.buttonResetOnClick)
        self.timer = timer

        self.buttonSwStatus = "start"

    def buttonSwOnClick(self):
        if self.buttonSw.text() == (
            "%s" % self.buttonSwStatus.capitalize()
        ):  # 开始/继续计时
            self.buttonSw.setText("Pause")
            self.timeShow.setText("Click to pause")
            self.timer.start()
            print("Stopwatch %s" % self.buttonSwStatus)
            if self.buttonSwStatus == "start":  # 切换按钮状态
                self.buttonSwStatus = "continue"
        else:  # 暂停计时
            self.timer.pause()
            print("Stopwatch pause")
            qfw.Flyout.create(
                icon=qfw.InfoBarIcon.SUCCESS,
                title="Paused",
                content=self.timer.getf(),
                target=self.buttonSw,
                parent=self,
                isClosable=True,
            )
            self.buttonSw.setText("%s" % self.buttonSwStatus.capitalize())
            self.timeShow.setText("Click to %s" % self.buttonSwStatus)

    def buttonResetOnClick(self):  # 重置计时
        self.timer.reset()
        print("Stopwatch reset")
        self.buttonSwStatus = "start"  # 重置按钮状态
        self.buttonSw.setText("Start")
        self.timeShow.setText("Click to start")

        qfw.Flyout.create(
            title="Successful",
            content="Timer reset",
            icon=qfw.InfoBarIcon.SUCCESS,
            target=self.buttonReset,
            parent=self,
            isClosable=True,
        )


class About(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("About")

        self.title = qfw.TitleLabel("About", self)
        self.text = qfw.BodyLabel(
            "A clock application based on PyQt6 and PyQt6-Fluent-Widgets.", self
        )
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
        self.setFixedWidth(400)
        self.setFixedHeight(300)
        self.setWindowTitle("EasyClock")

        qfw.setTheme(qfw.Theme.AUTO)
        if sys.platform in ["win32", "darwin"]:
            qfw.setThemeColor(getSystemAccentColor(), save=False)

        timer = Stopwatch()
        timer2 = Stopwatch()
        stopwatchCtl = StopwatchControl(timer)
        about = About()
        self.addSubInterface(stopwatchCtl, qfw.FluentIcon.STOP_WATCH, "Stopwatch")
        self.addSubInterface(about, qfw.FluentIcon.INFO, "About")


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
