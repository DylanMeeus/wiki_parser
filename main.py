from parser import parser

if __name__ == '__main__':
    file = open("mail.txt")
    recipients =  parser.parser().parse(file.read())
    printer = parser.pretty_printer(recipients)
    printer.print_wiki()
