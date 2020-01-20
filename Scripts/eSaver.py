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
import os
class eSaver:
	"""
	eSaver description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.defaultFolder = project.folder + '/CueLists'
		self.PlaylistOP = op.Playlist
		self.CueListPath = self.PlaylistOP.par.Cuelistpath
		self.LinkedTable = self.PlaylistOP.op('linkedTable')
	
	def InitializeFiles(self):
		print('Starting Up The Program')
		self.CreateCueListFolder()
		run('parent().Save()',delayFrames = 15, fromOP = me)
		run('parent().LoadLinkedTable()',delayFrames = 30, fromOP = me)

	def CreateCueListFolder(self):	
		try:
			os.mkdir(self.defaultFolder)
		except FileExistsError:
			print('Default folder has already been created')

		self.PlaylistOP.par.Cuelistpath = self.defaultFolder
		return self.defaultFolder

	def ChooseFile(self, isLoad = False):
		newFile = ui.chooseFile(load = isLoad, start = self.defaultFolder,  fileTypes = ['py'], title = "Cue List")
		if newFile == None:
			newFile = self.CueListPath.eval()
		return newFile

	def Save(self,saveAs = False):
		
		path = self.CueListPath.eval()
		
		if saveAs:
			path = self.ChooseFile(isLoad=False)

		try:
			self.LinkedTable.save(path)
		except:
			self.CreateCueListFolder()
		
		return path

	def Load(self):

		self.PlaylistOP.par.Cuelistpath = self.ChooseFile(isLoad=True)
		self.LinkedTable.par.loadonstartpulse.pulse()

	def New(self):
		self.LinkedTable.clear()
		path = self.Save(saveAs = True)
		self.PlaylistOP.par.Cuelistpath = path

	def LoadLinkedTable(self):
		self.LinkedTable.par.loadonstartpulse.pulse()