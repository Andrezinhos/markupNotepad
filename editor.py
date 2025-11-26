from PySide6.QtWidgets import QMainWindow, QFileDialog, QPushButton
from PySide6.QtGui import QAction, QFont, QIcon
from tabs import Tabs

class Editor(QMainWindow):
    def __init__(self):
        APP_VERSION = "0.7.4"
        super().__init__()
        self.setWindowTitle(f"Markup {APP_VERSION}")
        self.setWindowIcon(QIcon("favicon.ico"))
        self.resize(800, 600)

        # Tabs
        self.tabs = Tabs()
        self.setCentralWidget(self.tabs)
        self.currentFile = None
        self.filePaths = {}
        self.isDirty = False
        self.dirtyTabs = set()

        # Menu bar
        menu = self.menuBar()
        files = menu.addMenu("Files")
        format = menu.addMenu("Format")

        open = QAction("Open File", self)
        save = QAction("Save", self)
        saveAs = QAction("Save As", self)
        exit = QAction("Exit", self)

        files.addAction(open)
        files.addAction(save)
        files.addAction(saveAs)
        files.addSeparator()
        files.addAction(exit)

        majorFont = QAction("Increase Font", self)
        minorFont = QAction("Decrease Font", self)

        format.addAction(majorFont)
        format.addAction(minorFont)

        open.setShortcut("Ctrl+O")        
        open.triggered.connect(self.OpenFile)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.SaveFile)
        saveAs.setShortcut("Ctrl+Shift+S")
        saveAs.triggered.connect(self.SaveFileAs)
        majorFont.triggered.connect(lambda: self.tabs.currentWidget().setFont(QFont("Arial", 14)))
        minorFont.triggered.connect(lambda: self.tabs.currentWidget().setFont(QFont("Arial", 12)))
        exit.setShortcut("Ctrl+Q")
        exit.triggered.connect(self.close)
        
    def OpenFile(self):
        way, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if way:
            with open (way, "r", encoding="utf-8") as f:
                content = f.read()
                editor = self.tabs.currentWidget()
                editor.setPlainText(content)
                editor.textChanged.connect(self.markDirty)
                fileName = way.split("/")[-1]

                self.tabs.setTabText(self.tabs.currentIndex(), fileName)
                self.filePaths[self.tabs.currentIndex()] = way

    def SaveFile(self):
        index = self.tabs.currentIndex()
        if index in self.filePaths:
            path = self.filePaths[index]
            editor = self.tabs.currentWidget()
            with open (path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
                self.clearDirty(index)
        else:
            self.SaveFileAs()

    def SaveFileAs(self):
        way, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)")
        if way:
            editor = self.tabs.currentWidget()
            with open (way, "w", encoding="utf-8") as f:
                content = editor.toPlainText()
                f.write(content)
                fileName = way.split("/")[-1]
                self.tabs.setTabText(self.tabs.currentIndex(), fileName)
                self.filePaths[self.tabs.currentIndex()] = way

    def markDirty(self):
        #self.isDirty = True
        index = self.tabs.currentIndex()
        self.dirtyTabs.add(index)
        title = self.tabs.tabText(index)
        if not title.endswith("*"):
            self.tabs.setTabText(index, title + "*")
            
    def clearDirty(self, index):
        if index in self.dirtyTabs:
            self.dirtyTabs.remove(index)
        title = self.tabs.tabText(index).rstrip("*")
        self.tabs.setTabText(index, title)
    