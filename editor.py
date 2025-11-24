from PySide6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QTabWidget, QTabBar
from PySide6.QtGui import QAction, QFont, QIcon

class Editor(QMainWindow):
    def __init__(self):
        APP_VERSION = "0.5.3"
        super().__init__()
        self.setWindowTitle(f"Markup {APP_VERSION}")
        self.setWindowIcon(QIcon("favicon.ico"))
        self.resize(800, 600)
        font = QFont("Arial", 12)

        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.addNewTab(font)   
        self.tabs.addTab(QTextEdit(), "+")
        self.tabs.currentChanged.connect(self.onTabChanged)
        self.tabs.tabBar().tabBarClicked.connect(self.checkNewTab)
        self.tabs.setTabsClosable(True)
        plusIndex = self.tabs.count() - 1
        self.tabs.tabBar().setTabButton(plusIndex, QTabBar.RightSide, None)
        self.tabs.tabCloseRequested.connect(self.closeTab)

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
    
    def addNewTab(self, font, title="New Note"):
        textArea = QTextEdit()
        textArea.setFont(font)
        index = self.tabs.count() - 1
        self.tabs.insertTab(index, textArea, title)
        self.tabs.setCurrentIndex(index)

    def checkNewTab(self, index):
        if self.tabs.tabText(index) != "+":
            self.tabs.currentChanged.disconnect(self.checkNewTab)
            self.tabs.removeTab(index)
            self.tabs.currentChanged.connect(self.checkNewTab)
        if self.tabs.tabText(index) == "+":
            font = QFont("Arial", 12)
            self.addNewTab(font, "New Note")
    def onTabChanged(self, index):
        pass
    def closeTab(self, index):
        if index < 0 or index >= self.tabs.count():
            return
        
        if self.tabs.tabText(index) != "+":
            self.tabs.removeTab(index)

        if self.tabs.count() == 1:
            self.addNewTab(QFont("Arial", 12), "New Note")

        plusIndex = self.tabs.count() - 1
        self.tabs.tabBar().setTabButton(plusIndex, QTabBar.RightSide, None)