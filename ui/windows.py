from PyQt5.QtCore import  *
from PyQt5.QtGui import  *
from PyQt5.QtWidgets import *

from wikiparser import parser

class InputWidget(QTextEdit):
    def __init__(self):
        super().__init__()


class RawWiki(QTextEdit):
    """ Display the raw data (sorted and joined) """
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

class ToolWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wiki tool")
        self.resize(800,600)

        self.input_widget = InputWidget()
        self.raw_wiki_widget = RawWiki()
        self.input_widget.textChanged.connect(self.convert)

        tab_widget = QTabWidget()
        tab_widget.addTab(self.input_widget, "Input")
        tab_widget.addTab(self.raw_wiki_widget, "Raw Wiki")
        self.setCentralWidget(tab_widget)
        self.show()

    @pyqtSlot()
    def convert(self):
        input = self.input_widget.toPlainText()
        parsed_content = parser.parser().parse(input)
        printer = parser.pretty_printer(parsed_content)
        print(printer.print_wiki())
        self.raw_wiki_widget.setPlainText(printer.print_wiki())


