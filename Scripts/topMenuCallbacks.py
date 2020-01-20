"""
TopMenu callbacks

Callbacks always take a single argument, which is a dictionary
of values relevant to the callback. Print this dictionary to see what is
being passed. The keys explain what each item is.

TopMenu info keys:
	'widget': the TopMenu widget
	'item': the item label in the menu list
	'index': either menu index or -1 for none
	'indexPath': list of parent menu indexes leading to this item
	'define': TopMenu define DAT definition info for this menu item
	'menu': the popMenu component inside topMenu
"""

#################################
# exampleMenuDefine callbacks


import os



def onQuit(info):
	"""
	A simple menu item callback, named in the Top Menu DAT table
	"""
	debug('QUIT!')

settingsMenu = op.GUI.op('SettingsMenu')
opTable = op.GUI.op('table_settingsOPs')
opFind = op.GUI.op('opfind1')
cueListOp = op.Playlist
linkedTable = op.Playlist.op('linkedTable')

#Saver = op.Tools.mod.CuelistSaver.Saver()
playlister = op.Playlist


itemDict = {
	'Timecode': 'Timecode',
	'Cue List': 'CueList',
	'Countdown':'Countdown',
	'Transport':'Transport',
	'Control Panel':'Control_Panel',
	'Performance' :'showCooks'
}


def ToggleActive(path,isActive):
	newOP = op(path)
	assert newOP, "Could not toggle the display, no op found"
	newOP.par.enable = isActive
	newOP.par.display = isActive

def onSetting(info):
	"""
	A menu item callback that works on multiple menu items. The checkboxes in
	the menu evaluate the global guides and grid variables above to determine
	their state. The expressions used to evaluate the checkbox state are
	defined in the Top Menu DAT.
	"""


	if info['item'] == 'Edit Look':
		settingsMenu.par.Page = "parameter_look" #opTable['Look Settings',1].val
		ToggleActive(settingsMenu, True)
	elif info['item'] == 'Audio Config':
		settingsMenu.par.Page = "parameter_audio" 
		ToggleActive(settingsMenu, True)


def onWindow(info):
	item = info['item']
	itemOpName = itemDict[item] # translates the name from UI to comp name

	opPath = opFind[itemOpName,'path'].val

	curState = op(opPath).par.display

	ToggleActive(opPath, not curState)


def onNew(info):
	playlister.New()

def onSave(info):
	project.save()
	#linkedTable.save()

def onSaveCueList(info):
	item = info['item']


	if item == 'Save Cue List':
		playlister.Save()

	elif item == 'Save Cue List As':
		playlister.Save(saveAs=True)
	# if filepath == '':
	# 	filepath = GetNewFilePath()
	# 	SetFilePath(filepath)


	# if item == 'Save Cue List':
	# 	linkedTable.save(linkedTable.par.file.eval())

	# elif item == 'Save Cue List As':
	# 	newFilePath = GetNewFilePath()
	# 	#print(newFilePath)
	# 	SetFilePath(newFilePath)
	# 	linkedTable.save(newFilePath)


def onLoadCueList(info):
	playlister.Load()
	# item = info['item']
	# newFilePath = GetNewFilePath(isLoad =True)
	# SetFilePath(newFilePath)
	# linkedTable.par.loadonstartpulse.pulse()



def GetNewFilePath(isLoad = False) -> str:
	defaultFolder = project.folder + '/' + 'CueLists'
	
	try:
		os.mkdir(project.folder + '/' + 'CueLists')
	except FileExistsError:
		pass
	
	newFile = ui.chooseFile(load = isLoad,start = defaultFolder,  fileTypes = ['py'], title = "Cue List")

	if newFile == None: # user has cancelled the operation
		newFile = cueListOp.par.Cuelistpath.eval() # revert it back to normal
	
	return newFile


def SetFilePath(path):

	cueListOp.par.Cuelistpath = path
	# this is most certainly an error, if so throw an assertion error
	assert cueListOp.par.Cuelistpath.eval() != '', "There is no path assigned to the cue list"




def getRecentFiles(info):
	"""
	A rowCallback used in the Top Menu DAT table to automatically generate rows.
	These callbacks must return a dictionary or list of dictionaries that mimic
	the columns in the Top Menu DAT. Dictionaries only need the columns with
	data in them, but must have corresponding columns in the Top Menu DAT in
	order to be recognized.
	"""
	return [
		{'item2': 'File 1'},
		{'item2': 'File 2', 'highlight': True},
		{'item2': 'File three', 'dividerAfter': True}
	]

# end examples
####################################

# standard menu callbacks

def onSelect(info):
	"""
	User selects a menu option
	"""
	#debug(info)

def onRollover(info):
	"""
	Mouse rolled over an item
	"""

def onOpen(info):
	"""
	Menu opened
	"""

def onClose(info):
	"""
	Menu closed
	"""

def onMouseDown(info):
	"""
	Item pressed
	"""

def onMouseUp(info):
	"""
	Item released
	"""

def onClick(info):
	"""
	Item pressed and released
	"""

def onLostFocus(info):
	"""
	Menu lost focus
	"""