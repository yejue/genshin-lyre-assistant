import ctypes
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from client.main import MainController
from genshin_assistant import settings


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except RuntimeError:
        return False


def main():
    app = QApplication(["default"])
    app.setWindowIcon(QIcon(settings.ICON_PATH))
    controller = MainController()
    controller.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    if is_admin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
