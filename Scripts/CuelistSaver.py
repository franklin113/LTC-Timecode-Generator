import os

class Saver:

	def __init__(self):
		self.defaultFolder = project.folder + '/CueLists'
		self.PlaylistOP = op.Playlist
		self.CueListPath = self.PlaylistOP.par.Cuelistpath
		self.LinkedTable = self.PlaylistOP.op('linkedTable')
	
	def CreateCueListFolder(self):	
		try:
			os.mkdir(self.defaultFolder)
		except FileExistsError:
		    pass
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