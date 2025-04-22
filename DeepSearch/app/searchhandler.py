from Modules.Search.searchtxt import serach_text


class MenuOption:
    def __init__(self,name,shortcut=None):
        self.name = name
        self.shortcut = shortcut
    
    def execute(self):
        print("executing {self.name}")

def textbase(text=None)-> list:
    return serach_text(text)