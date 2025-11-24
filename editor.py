from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtGui import QAction, QFont, QIcon
from tabs import Tabs

class Editor(QMainWindow):
    def __init__(self):
        APP_VERSION = "0.5.5"
        super().__init__()
        self.setWindowTitle(f"Markup {APP_VERSION}")
        self.setWindowIcon(QIcon("favicon.ico"))
        self.resize(800, 600)
        font = QFont("Arial", 12)

        # Tabs
        self.tabs = Tabs()
        self.setCentralWidget(self.tabs)

        # Menu bar
        menu = self.menuBar()
        archive = menu.addMenu("Archive")
        format = menu.addMenu("Format")

        open = QAction("Open File", self)
        save = QAction("Save File", self)
        exit = QAction("Exit", self)

        archive.addAction(open)
        archive.addAction(save)
        archive.addSeparator()
        archive.addAction(exit)

        majorFont = QAction("Increase Font", self)
        minorFont = QAction("Decrease Font", self)

        format.addAction(majorFont)
        format.addAction(minorFont)

        open.triggered.connect(self.OpenFile)
        save.triggered.connect(self.SaveFile)
        majorFont.triggered.connect(lambda: self.tabs.currentWidget().setFont(QFont("Arial", 14)))
        minorFont.triggered.connect(lambda: self.tabs.currentWidget().setFont(QFont("Arial", 12)))
        exit.triggered.connect(self.close)
        
    def OpenFile(self):
        way, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if way:
            with open (way, "r", encoding="utf-8") as f:
                content = f.read()
                editor = self.tabs.currentWidget()
                editor.setPlainText(content)
                fileName = way.split("/")[-1]
                self.tabs.setTabText(self.tabs.currentIndex(), fileName)

    def SaveFile(self):
        way, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if way:
            editor = self.tabs.currentWidget()
            with open (way, "w", encoding="utf-8") as f:
                content = editor.toPlainText()
                f.write(content)
                fileName = way.split("/")[-1]
                self.tabs.setTabText(self.tabs.currentIndex(), fileName)
    