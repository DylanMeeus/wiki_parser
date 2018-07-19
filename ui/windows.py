from PyQt5.QtCore import  *
from PyQt5.QtGui import  *
from PyQt5.QtWidgets import *

from wikiparser import parser

class InputWidget(QTextEdit):
    def __init__(self):
        super().__init__()


class HtmlWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

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
        self.user_mail = HtmlWidget()
        self.dev_mail = HtmlWidget()
        self.tester_mail = HtmlWidget()

        self.input_widget.textChanged.connect(self.convert)

        tab_widget = QTabWidget()
        tab_widget.addTab(self.input_widget, "Input")
        tab_widget.addTab(self.raw_wiki_widget, "Raw Wiki")
        tab_widget.addTab(self.user_mail, "User mail")
        tab_widget.addTab(self.tester_mail, "Imp mail")
        tab_widget.addTab(self.dev_mail, "S9 mail")

        self.setCentralWidget(tab_widget)
        self.show()

    @pyqtSlot()
    def convert(self):
        input =  self.input_widget.toPlainText()
        parsed_content = parser.parser().parse(input)
        printer = parser.pretty_printer(parsed_content)
        self.raw_wiki_widget.setPlainText(printer.print_wiki())
        self.user_mail.setPlainText(printer.print_users())
        self.dev_mail.setPlainText(printer.print_s9())
        self.tester_mail.setPlainText(printer.print_testers())


