from PyQt5.QtCore import  *
from PyQt5.QtGui import  *
from PyQt5.QtWidgets import *

class ToolWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input window")
        self.resize(800,600)
        self.textArea = QTextEdit()
        self.textArea.textChanged.connect(self.convert)
        self.setCentralWidget(self.textArea)
        self.show()


    @pyqtSlot()
    def convert(self):
        print(self.textArea.toPlainText())

