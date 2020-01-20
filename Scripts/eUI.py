"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions
from pprint import pprint
class eUI:
	"""
	eUI description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		# TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
		# 				   readOnly=False)

		# # attributes:
		# self.a = 0 # attribute
		# self.B = 1 # promoted attribute

		# stored items (persistent across saves and re-initialization):
		storedItems = [
			# Only 'name' is required...
			{'name': 'UIPanels', 'default': None, 'readOnly': False,
			 						'property': True, 'dependable': True},
		]
		# Uncomment the line below to store StoredProperty. To clear stored
		# 	items, use the Storage section of the Component Editor
		
		self.Opfind = self.ownerComp.op('opfind1')

		self.stored = StorageManager(self, ownerComp, storedItems)

	def GetWindowList(self):
		self.stored['UIPanels'] = [x.val for x in self.Opfind.col('path')[1:]]
		self.SetPanelOrder(self.stored['UIPanels'])

	def ChangeOrder(self, selection):
		itemList = self.stored['UIPanels']
		item = itemList.pop(selection)
		itemList.append(item)
		self.SetPanelOrder(itemList)

	def SetPanelOrder(self,itemList):
		for ind, val in enumerate(itemList):
			op(val).par.layer = ind

