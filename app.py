import sys
from src.frontend.window import MainWindow
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(width=1400, height=800)
    main_window.show()
    app.exec() 