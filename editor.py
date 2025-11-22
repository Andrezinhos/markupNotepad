from PySide6.QtWidgets import QMainWindow, QTextEdit, QFileDialog
from PySide6.QtGui import QAction, QFont

class Editor(QMainWindow):

    
    def __init__(self):
        APP_VERSION = "0.2.1"
        super().__init__()
        self.setWindowTitle(f"Markup {APP_VERSION}")
        self.resize(800, 600)
        font = QFont("Arial", 12)

        self.textArea = QTextEdit()
        self.textArea.setFont(font)
        self.setCentralWidget(self.textArea)

        menu = self.menuBar()
        archive = menu.addMenu("Arquivo")
        format = menu.addMenu("Formatar")

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
        majorFont.triggered.connect(lambda: self.textArea.setFont(QFont("Arial", 14)))
        minorFont.triggered.connect(lambda: self.textArea.setFont(QFont("Arial", 12)))
        exit.triggered.connect(self.close)
        
    def OpenFile(self):
        way, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if way:
            with open (way, "r", encoding="utf-8") as f:
                content = f.read()
                self.textArea.setPlainText(content)

    def SaveFile(self):
        way, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if way:
            with open (way, "w", encoding="utf-8") as f:
                content = self.textArea.toPlainText()
                f.write(content)