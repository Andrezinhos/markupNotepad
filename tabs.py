from PySide6.QtWidgets import QTabWidget, QTextEdit, QTabBar
from PySide6.QtGui import QFont

class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # tabs
        self.addNewTab(QFont("Arial", 12))   
        self.addTab(QTextEdit(), "+")
        self.currentChanged.connect(self.onTabChanged)
        self.tabBar().tabBarClicked.connect(self.checkNewTab)
        self.setTabsClosable(True)

        plusIndex = self.count() - 1
        self.tabBar().setTabButton(plusIndex, QTabBar.RightSide, None)
        self.tabCloseRequested.connect(self.closeTab) 

    def addNewTab(self, font, title="New Note"):
        textArea = QTextEdit()
        textArea.setFont(font)
        index = self.count() - 1
        self.insertTab(index, textArea, title)
        self.setCurrentIndex(index)

    def checkNewTab(self, index):
        if index < 0 or index >= self.count():
            return 
        if self.tabText(index) == "+":
            font = QFont("Arial", 12)
            self.addNewTab(font, "New Note")

    def onTabChanged(self, index):
        pass

    def closeTab(self, index):
        if self.tabText(index) != "+":
            self.removeTab(index)

        if self.count() == 1:
            self.addNewTab(QFont("Arial", 12), "New Note")

        plusIndex = self.count() - 1
        self.tabBar().setTabButton(plusIndex, QTabBar.RightSide, None)