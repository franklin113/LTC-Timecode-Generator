#Shared Use License: This file is owned by Derivative Inc. (â€œDerivativeï¿½) 
#and can only be used, and/or modified for use, in conjunction with 
#Derivativeâ€™s TouchDesigner software, and only if you are a licensee who 
#has accepted Derivativeâ€™s TouchDesigner license or assignment agreement 
#(which also governs the use of this file).  You may share a modified version 
#of this file with another authorized licensee of Derivativeâ€™s TouchDesigner 
#software.  Otherwise, no redistribution or sharing of this file, with or 
#without modification, is permitted.

"""
All callbacks for this lister go in this DAT. For a list of available callbacks,
see:

https://docs.derivative.ca/Palette:lister#Custom_Callbacks
"""

from pprint import pprint
'''

{'callbackName': 'onClick',
 'cellText': 'Cue 2',
 'col': 0,
 'ownerComp': type:listCOMP path:/project1/container1/PlaylistBuilder/lister,
 'row': 2,
 'rowData': OrderedDict([('Name', 'Cue 2'),
						 ('Start Time', '00:10:05:00'),
						 ('End Time', '00:10:10:00'),
						 ('Go', 'Go'),
						 ('rowObject',
						  ['Cue 2', '00:10:05:00', '00:10:10:00', 'Go'])])}


'''


	


# def onSelectRow(info):
# 	print(info)

selectedCue = mod.CueSelection.CueSelection()
Playlister = parent.Playlist
Lister = parent.Playlist.op('lister')
timer = op('timer2')
linkedTable = Playlister.op('linkedTable')


#assert timer
import re

timePattern = '\d\d:\d\d:\d\d:\d\d'

digitFillPattern = [
	r'\d\d:\d\d:\d\d'
]

singleDigitPat = ':(\d):'

def onClick(info):
	pprint(info)
	#pprint(info['rowData']['Name'])

	row = info['row']
	col = info['col']

	if row >= 0 and col >= 0:

		try:
			selectedCue.Build(info['row'], info['col'], info['rowData'], info['cellText'])
			if Playlister.par.Debug:
				selectedCue.Debug()
			if int(col) == parent().RunRadio:
			   # timer.par.initialize.pulse()
				#timer.par.cycle = selectedCue.GetLoopState()
			   # debug("Loop state: ", selectedCue.GetLoopState())
				#timer.goTo(segment = -100 )#selectedCue.GetRowIndex())
				Playlister.SetSegment(selectedCue.GetRowIndex())
				#debug("Sending to the timer: ", selectedCue.GetRowIndex())
				run("op('{myOP}').RadioPlay({val})".format(myOP = Playlister, val = selectedCue.GetRowIndex()), delayFrames = 1, fromOP = me)

				#run("op('{}').goTo(segment = {})".format(timer, selectedCue.GetRowIndex()),delayFrames = 1, fromO = me)
				if selectedCue.GetName() == 'TOD':
					timeOfDay = True
				else:
					timeOfDay = False
				Playlister.TriggerTimecodeChange(selectedCue.GetStartTime(), TOD=timeOfDay)
			
			elif int(col) == parent().LoopCol:
				run("op('{myOP}').ToggleLoop({val})".format(myOP = parent(), val = selectedCue.GetRowIndex()), delayFrames = 1, fromOP = me)



		except Exception as e:
			debug(e)
	else:
		pass

def onEditEnd(info):

	if info['col'] == 1 or info['col'] == 2:
		
	

		timeString = info['cellText']

		# check if this is formatted right, if so, return

		match = re.match(timePattern,timeString)
		if match:
			#everything is ok, get out of here
			return
		run('AutoCorrect("{}",{},{})'.format(timeString,info['row'],info['col']),delayFrames = 1, fromOP = me)

def AutoCorrect(timeString,row,col):
	print('running')
	timePattern = r'\d\d:\d\d:\d\d:\d\d'

	is4digits = r'(\d\d)(\d\d)$'		# is seconds and frames
	is6digits = r'(\d\d)(\d\d)(\d\d)$'		# is seconds and frames

	pat1 = r'\d\d'				# only has frames
	pat2 = r'\d\d:\d\d'			# doesn't have hours or minutes
	pat3 = r'\d\d:\d\d:\d\d'	# doesn't have hours
	pat4 = r'\d'				# is only 1 digit long
	pat5 = r':(\d)$'			# ends with :
	pat6 = r'(\d)(\d\d)'		# 3 digits in a row
	pat7 = r'^(\d):'			# starts with only one digit

	singleDigitPat = r':(\d):'	# put only a single digit within : :

	timeString = re.sub(pat7, r'0\1:',timeString)
	timeString = re.sub(r'::', r':00:',timeString)

	timeString = re.sub(is6digits, r'\1:\2:\3',timeString)	

	timeString = re.sub(is4digits, r'\1:\2',timeString)	
	print(timeString)
	totalCount = 0
	timeString = ''.join([x for x in timeString if x.isdigit() or x == ':'])
	if len(timeString) > 0:
		
		while Playlister.IsValidTimecode(timeString) == False and totalCount < 20:
			#remove all letters
			totalCount += 1

			if timeString[0] == ':':
				timeString = timeString[1:]

			if re.fullmatch(r'\d\d:\d\d:\d\d',timeString):	# only MM:SS:FF
				timeString = '00:' + timeString
			elif re.fullmatch(r'\d\d:\d\d',timeString):		# only SS:FF
				timeString = '00:00:' + timeString
			elif re.fullmatch(r'\d\d', timeString):			# only FF
				timeString = '00:00:00:' + timeString
			elif re.fullmatch(r'\d', timeString):			# only single FF
				timeString = '00:00:00:0' + timeString


			
			# Lets check and see if there are any single digits around
			timeString = re.sub(r':(\d):', r':0\1:',timeString)	# a single digit wrapped in colons
			timeString = re.sub(r':(\d)$', r':0\1',timeString)	# a colon and single digit only at the end
			
			# fix including of three digits
			#timeString = re.sub(r'(\d\d\d)', r'err',timeString)		# Three digits 


	

	linkedTable[row-1,col] = timeString