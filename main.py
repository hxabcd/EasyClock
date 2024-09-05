import sys
import time

import PyQt6.QtCore as QtC
import PyQt6.QtWidgets as QtW
import qfluentwidgets as qfw
from qframelesswindow.utils import getSystemAccentColor

from stopwatch import Ui_Stopwatch


class Stopwatch:
    def __init__(self):
        self.start_time = 0
        self.past_time = 0
        self.is_running = False

    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def pause(self):
        self.past_time = self.get(now=True)
        self.start_time = 0
        self.is_running = False

    def reset(self):
        self.start_time = 0
        self.past_time = 0
        self.is_running = False

    def get(self, now=False):
        if now:
            return time.time() - self.start_time + self.past_time
        return self.past_time

    def getf(self, now=False):
        if now:
            now_time = time.time() - self.start_time + self.past_time
            return "%02d:%02d:%06.3f" % (
                now_time // 60 // 60,
                now_time // 60 % 60,
                now_time % 60 % 60,
            )
        return "%02d:%02d:%06.3f" % (
            self.past_time // 60 // 60,
            self.past_time // 60 % 60,
            self.past_time % 60 % 60,
        )


class StopwatchControl(QtW.QWidget, Ui_Stopwatch):
    def __init__(self, timer: Stopwatch):
        super().__init__()
        self.setObjectName("Stopwatch")

        self.setupUi(self)
        self.buttonSw.clicked.connect(self.buttonSwOnClick)
        self.buttonReset.clicked.connect(self.buttonResetOnClick)
        self.buttonShowTime.clicked.connect(self.buttonShowTimeOnClick)
        self.timer = timer

        self.buttonSwStatus = "start"

    def buttonSwOnClick(self):
        if self.buttonSw.text() == (
                "%s" % self.buttonSwStatus.capitalize()
        ):  # 开始/继续计时
            self.buttonSw.setText("Pause")
            self.statusShow.setText("Click to pause")
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
            self.statusShow.setText("Click to %s" % self.buttonSwStatus)

    def buttonResetOnClick(self):  # 重置计时
        self.timer.reset()
        print("Stopwatch reset")
        self.buttonSwStatus = "start"  # 重置按钮状态
        self.buttonSw.setText("Start")
        self.statusShow.setText("Click to start")

        qfw.Flyout.create(
            title="Successful",
            content="Timer reset",
            icon=qfw.InfoBarIcon.SUCCESS,
            target=self.buttonReset,
            parent=self,
            isClosable=True,
        )

    def buttonShowTimeOnClick(self):
        qfw.Flyout.create(
            title="Time past now:",
            content="%s" % self.timer.getf(True) if self.timer.is_running else self.timer.getf(),
            icon=qfw.InfoBarIcon.SUCCESS,
            target=self.buttonReset,
            parent=self,
            isClosable=True,
        )


class About(QtW.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("About")

        self.title = qfw.TitleLabel("About", self)
        self.text = qfw.BodyLabel(
            "A clock application based on PyQt6 and PyQt6-Fluent-Widgets.", self
        )
        self.author = qfw.BodyLabel("Author: HxAbCd", self)
        self.text.setWordWrap(True)

        self.show_layout = QtW.QVBoxLayout()
        self.show_layout.addWidget(self.title)
        self.show_layout.setAlignment(self.title, QtC.Qt.AlignmentFlag.AlignTop)
        self.show_layout.addWidget(self.text)
        self.show_layout.addWidget(self.author)
        self.setLayout(self.show_layout)


class MainWindow(qfw.FluentWindow):
    def __init__(self):
        super().__init__()
        self.resize(320, 280)
        self.setWindowTitle("EasyClock")

        qfw.setTheme(qfw.Theme.AUTO)
        if sys.platform in ["win32", "darwin"]:
            qfw.setThemeColor(getSystemAccentColor(), save=False)

        timer = Stopwatch()
        stopwatch_ctl = StopwatchControl(timer)
        about = About()
        self.addSubInterface(stopwatch_ctl, qfw.FluentIcon.STOP_WATCH, "Stopwatch")
        self.addSubInterface(about, qfw.FluentIcon.INFO, "About")


def main():
    app = QtW.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
