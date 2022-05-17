class MenuItem(object):
    def __init__(self, type:str, name:str, attributes = None, visible = True):
        self.type = type
        self.name = name
        self.attributes = attributes
        self.visible = visible

class Back(MenuItem):
	def __init__(self, name:str):
		MenuItem.__init__(self, "back", name)

class Menu(MenuItem):
	def __init__(self, name:str, attributes = None, visible = True, options:list[MenuItem] = []):
		MenuItem.__init__(self, "menu", name, attributes, visible)
		self.options = options
		self.selectedOption = 0
		self.parent = None

	def addOptions(self, options:list[MenuItem]):
		self.options = self.options + options
		self.selectedOption = 0

	def addOption(self, option:MenuItem):
		newOptionList = []
		newOptionList.insert(0, option)
		self.options = self.options + newOptionList
		self.selectedOption = 0

	def setParent(self, parent):
		self.parent = parent

	def nextSelection(self):
		self.selectedOption = (self.selectedOption + 1) % len(self.options)

	def getSelection(self):
		return self.options[self.selectedOption]