import sys
from PySide6.QtWidgets import QApplication
from editor import Editor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Editor()
    window.show()
    app.exec()