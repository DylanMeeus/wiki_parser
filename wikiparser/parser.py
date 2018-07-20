from functools import reduce
""" tool to manage wiki.txt data for KWS prod/try release mails 
    
    Info
    ----
    h1: recipients / h4: topics / *: entry
"""

class topic:
    def __init__(self, name):
        self.name = name.strip()
        self.entries = []
        
    def __eq__(self, other):
        return other != None and self.name.lower() == other.name.lower()

class recipient:
    def __init__(self, name):
        self.name = name.strip()
        self.topics = []
        
    def __eq__(self, other):
        return other != None and self.name.lower() == other.name.lower()
    
    def __hash__(self):
        return hash(self.name)

class pretty_printer:
    """ prints the output for the chosen group (wiki / users / tester /  developers """

    def __init__(self, recipients):
        self.recipients = recipients

    def print_for_groups(self, groups):
        """ prints the groups in the chosen order"""
        content = "<html><body>"
        for group in groups:
            for recipient in self.recipients:
                if recipient == group:
                    content += ("\n\n<h1>{0}</h1><hr>".format(recipient.name[3:]))
                    for topic in sorted(recipient.topics, key = lambda t: t.name.lower()):
                        content += ("\n\n<h4>{0}</h4>".format(topic.name[3:]))
                        for entry in topic.entries:
                            content += ("\n{0}<br/>".format(entry[2:].replace("\\","")))
        content += "</body></html>"
        return content

    def print_s9(self):
        """ at the moment they are equal"""
        return self.print_wiki()

    def print_testers(self):
        tester_recipients = list(filter(lambda r: r.name != "h1. s9", self.recipients))
        return self.print_for_groups(tester_recipients)

    def print_users(self):
        return self.print_for_groups([recipient("h1. g")])

    def print_wiki(self):
        """ prints wiki output"""
        sorted_recipients = sorted(self.recipients, key = lambda r: r.name)
        return self.print_for_groups(sorted_recipients)


class parser:
    """ Stateful parser of wiki mails """
    def __init__(self):
        self.recipients = []
        self.current_recipient = None
        self.current_topic = None

    def add_recipient(self):
        if self.current_recipient != None and self.current_recipient not in self.recipients:
            self.recipients.append(self.current_recipient)
        self.current_recipient = None

    def add_topic(self):
        if self.current_topic != None and self.current_topic not in self.current_recipient.topics:
            self.current_recipient.topics.append(self.current_topic)
        self.current_topic = None

    def parse(self, content):
        """ Parse wiki-formatted content """
        lines = content.split("\n")

        for line in lines:
            if len(line) < 2: # invalid line
                continue
            prefix = line[:2]
            if prefix == '* ': # entry
                self.current_topic.entries.append(line)
            elif prefix == 'h1':
                # replace the recipient
                self.add_topic()
                self.add_recipient()
                new_recipient = recipient(line)
                # use an existing object if it matches
                # otherwise keep using the new object
                for r in self.recipients:
                    if r == new_recipient:
                        new_recipient = r
                        break
                self.current_recipient = new_recipient
            elif prefix == 'h4':
                self.add_topic()
                new_topic = topic(line)
                for existing_topic in self.current_recipient.topics:
                    if existing_topic == new_topic:
                        new_topic = existing_topic
                        break
                self.current_topic = new_topic
        # EOF reached, but we might have to append outstanding topics etc
        self.add_topic()
        self.add_recipient()
        return self.recipients
    
