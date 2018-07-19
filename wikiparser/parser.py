
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
        content = ""
        for group in groups:
            for recipient in self.recipients:
                if recipient.name == group.name:
                    content += ("\n\n{0}".format(recipient.name))
                    for topic in sorted(recipient.topics, key = lambda t: t.name.lower()):
                        content += ("\n\n{0}".format(topic.name))
                        for entry in topic.entries:
                            content += ("\n{0}".format(entry))
        return content
            

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
            if self.current_topic != None and self.current_topic not in self.current_recipient.topics:
                self.current_recipient.topics.append(self.current_topic)
                self.current_topic = None
            self.recipients.append(self.current_recipient)

    def add_topic(self):
        if self.current_topic != None and self.current_topic not in self.current_recipient.topics:
            self.current_recipient.topics.append(self.current_topic)

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
                self.add_recipient()
                new_recipient = recipient(line)
                # use an existing object if it matches
                # otherwise keep using the new object
                for r in self.recipients:
                    if r == new_recipient:
                        new_recipient = r
                self.current_recipient = new_recipient
            elif prefix == 'h4':
                self.add_topic()
                new_topic = topic(line)
                for existing_topic in self.current_recipient.topics:
                    if existing_topic == new_topic:
                        new_topic = existing_topic
                self.current_topic = new_topic
        # EOF reached, but we might have to append outstanding topics etc
        self.add_topic()
        self.add_recipient()
        return self.recipients
    
