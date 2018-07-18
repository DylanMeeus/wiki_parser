
""" tool to manage wiki.txt data for KWS prod/try release mails 
    
    Info
    ----
    h1: recipients / h4: topics / *: entry
"""

class topic:
    def __init__(self, name):
        self.name = name
        self.entries = []
        
    def __eq__(self, other):
        return other != None and self.name == other.name

class recipient:
    def __init__(self, name):
        self.name = name
        self.topics = []
        
    def __eq__(self, other):
        return other != None and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

class pretty_printer:
    """ prints the output for the chosen group (wiki / users / tester /  developers """

    def __init__(self, recipients):
        self.recipients = recipients

    def print_for_groups(self, groups):
        """ prints the groups in the chosen order"""
        for group in groups:
            for recipient in self.recipients:
                if recipient.name == group.name:
                    print("\n{0}".format(recipient.name))
                    for topic in recipient.topics:
                        print("\n{0}".format(topic.name))
                        for entry in topic.entries:
                            print(entry)
            

    def print_wiki(self):
        """ prints wiki output"""
        sorted_recipients = sorted(self.recipients, key = lambda r: r.name)
        return self.print_for_groups(sorted_recipients)


class parser:
    def parse(self, content):
        """ Parse wiki-formatted content """
        lines = content.split("\n")
        current_recipient = None
        current_topic = None
        recipients = []
        for line in lines:
            if len(line) < 2: # invalid line
                continue
            prefix = line[:2]
            if prefix == '* ': # entry
               current_topic.entries.append(line)
            elif prefix == 'h1':
                # replace the recipient
                if current_recipient != None and current_recipient not in recipients:
                    recipients.append(current_recipient)
                new_recipient = recipient(line)
                # use an existing object if it matches
                # otherwise keep using the new object
                for r in recipients:
                    if r == new_recipient:
                        print(r.name)
                        new_recipient = r 
                current_recipient = new_recipient
            elif prefix == 'h4':
                if current_topic != None and current_topic not in current_recipient.topics:
                    current_recipient.topics.append(current_topic)
                new_topic = topic(line)
                for existing_topic in current_recipient.topics:
                    if existing_topic == new_topic:
                        new_topic = existing_topic
                current_topic = new_topic 
        return recipients
    
if __name__ == '__main__':
    file = open("mail.txt")
    recipients =  parser().parse(file.read())
    printer = pretty_printer(recipients)
    printer.print_wiki()
