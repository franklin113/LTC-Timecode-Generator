# me - This DAT
# 
# dat - The DAT that received the key event
# key - The name of the key attached to the event.
#		This tries to be consistent regardless of which language
#		the keyboard is set to. The values will be the english/ASCII
#		values that most closely match the key pressed.
#		This is what should be used for shortcuts instead of 'character'.
# character - The unicode character generated.
# alt - True if the alt modifier is pressed
# ctrl - True if the ctrl modifier is pressed
# shift - True if the shift modifier is pressed
# state - True if the event is a key press event
# time - The time when the event came in milliseconds

playlister = op.Playlist


def onKey(dat, key, character, alt, lAlt, rAlt, ctrl, lCtrl, rCtrl, shift, lShift, rShift, state, time):
	return

# shortcutName is the name of the shortcut

# topMenuCallbacks = op.GUI.mod.topMenuCallbacks1
# assert topMenuCallbacks	
# shortcutAssignment = {
# 	'shift.s' : ['onSaveCueList', 'Save Cue List'],
# 	#'alt.s' : ['onSaveCueList','Save Cue List As'],
# 	'ctrl.l' : ['onSaveCueList','Load Cue List']
# }

def onShortcut(dat, shortcutName, time):
	#print(shortcutName)
	
	# if hasattr(topMenuCallbacks, shortcutAssignment[shortcutName][0]):
	# 	getattr(topMenuCallbacks, shortcutAssignment[shortcutName][0])(dict([('item',shortcutAssignment[shortcutName][1])]))

	if shortcutName == 'shift.s':
		playlister.Save()
	elif shortcutName == 'ctrl.l':
		playlister.Load()

	return
	