class Status:
    def __init__(self):
        self.entries = []

    def addEntry(self, time, log):
        self.entries.append(Entry(time, log))

    def clear(self):
        self.entries = []

    def __str__(self):
        return "\n".join([str(entry) for entry in self.entries])
    
class Entry:
    def __init__(self, time, log):
        self.time = time
        self.log = log
    
    def __str__(self):
        return self.time + " - " + self.log