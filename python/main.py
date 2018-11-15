import sys,os
from wikiparser import parser
from ui import windows

from PyQt5.QtCore import  *
from PyQt5.QtGui import  *
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = windows.ToolWindow()
    print("done")
    sys.exit(app.exec_())
    #file = open("mail.txt")
    #recipients =  parser.parser().parse(file.read())
    #printer = parser.pretty_printer(recipients)
    #printer.print_wiki()
