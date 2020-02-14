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
import datetime
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

#selectedCue = mod.CueSelection.CueSelection()
listerSelection = mod.CueSelection.CueSelection
Playlister = parent.Playlist
Lister = parent.Playlist.op('lister')
timer = op('timer2')
linkedTable = Playlister.op('linkedTable')


#assert timer
import re



'''
 'rowData': OrderedDict([('Name', 'Cue 3 - Test'),
                         ('Start Time', '05:00:00:00'),
                         ('End Time', '05:00:12:00'),
                         ('Loop', '0'),
                         ('Go', '0'),
                         ('rowObject',
                          ['Cue 3 - Test',
                           '05:00:00:00',
                           '05:00:12:00',
                           '0',
                           '0'])])}

'''

def onClick(info):
	#pprint(info)
	#pprint(info['rowData']['Name'])

	row = int(info['row'])
	col = int(info['col'])
	if row >= 0 and col >= 0:

		try:

			cueSelection = mod.CueSelection.CueSelection(
				info['rowData']['Start Time'],
				info['rowData']['End Time'],
				info['rowData']['Name'],
				row,
				col
				)
			
			if Playlister.par.Debug:
				debug(cueSelection)
			runRadio = 4 #parent().RunRadio # the column that triggers cues
			if int(col) == runRadio:

				Playlister.SetSegment(cueSelection['row'])
				run("op('{myOP}').RadioPlay({val})".format(myOP = Playlister, val = cueSelection['row']), delayFrames = 1, fromOP = me)

				#run("op('{}').goTo(segment = {})".format(timer, selectedCue.GetRowIndex()),delayFrames = 1, fromO = me)
				if cueSelection['name'] == 'TOD':
					timeOfDay = True
				else:
					timeOfDay = False
				Playlister.TriggerTimecodeChange(cueSelection['startTime'], TOD=timeOfDay)
			
			elif int(col) == parent().LoopCol:
				run("op('{myOP}').ToggleLoop({val})".format(myOP = parent(), val = cueSelection['row']), delayFrames = 1, fromOP = me)



		except Exception as e:
			debug(e)
	else:
		pass

def onEditEnd(info):
	if info['col'] == 1 or info['col'] == 2:
		
	

		timeString = info['cellText']

		# check if this is formatted right, if so, return

		run('AutoCorrect("{}",{},{},"{}")'.format(timeString,info['row'],info['col'],info['prevText']),delayFrames = 1, fromOP = me)
		run('CorrectTimeLogic({}, {}, "{}")'.format(info['row'], info['col'], info['prevText']), delayFrames = 1, fromOP = me)

def CorrectTimeLogic(rowNum:int, colNum:int, prevText:str):
	'''
	Function used to assert startTime and endTime logic.
	Incorrect logic will revert the startTime or endTime value to the previous value.
	'''
	endTimeIDX = list(Lister.Data[0].keys()).index('End Time')
	startTimeIDX = list(Lister.Data[0].keys()).index('Start Time')
	name, start, end, *rest = linkedTable.row(rowNum-1)
	startTime = datetime.datetime.strptime(start.val, '%H:%M:%S:%f')
	endTime = datetime.datetime.strptime(end.val, '%H:%M:%S:%f')

	if colNum == endTimeIDX:
		if endTime <= startTime:
			linkedTable[rowNum-1, colNum] = prevText
	elif colNum == startTimeIDX:
		if startTime >= endTime:
			linkedTable[rowNum-1, colNum] = prevText

def AutoCorrect(timeString,row,col,prevText):
			# (r'(\d\d)(\d)(:\d\d:\d\d:\d\d)', r'\1\3'),
		# 
		# (r'(\d\d:\d\d:\d\d)(\d)(:\d\d)', r'\1\3'),
	issues = [
		
		(r'[^0-9^a-z]',':'),									# $ or anything


		# -- 1h, 01h, 1m,01m,1s,01s,1f,01f
		(r'^(\d)(h)$',						r'0\g<1>:00:00:00'),
		(r'^(\d\d)(h)$',						r'\g<1>:00:00:00'),
		(r'^(\d)(m)$',						r'00:0\g<1>:00:00'),
		(r'^(\d\d)(m)$',						r'00:\g<1>:00:00'),

		(r'^(\d)(s)$',						r'00:00:0\g<1>:00'),
		(r'^(\d\d)(s)$',						r'00:\g<1>:00'),

		(r'^(\d)(f)$',						r'00:00:00:0\g<1>'),
		(r'^(\d\d)(f)$',						r'00:00:00:\g<1>'),
		
		# -- 1h30 ?m, 01h30 ?m

		(r'^(\d)(h)(\d\d)(m)?',						r'0\g<1>:\g<3>:00:00'),
		(r'^(\d\d)(h)(\d\d)(m)?',						r'\g<1>:\g<3>:00:00'),



		
		(r'(\d\d:\d\d:\d\d:\d\d)(\d)', 	r'\1'), 
		(r'(\d\d)(\d)(:\d\d:\d\d:\d\d)', 		r'\1\3'), 
		(r'(\d\d:\d\d)(\d)(:\d\d:\d\d)', 		r'\1\3'),
		(r'(\d\d:\d\d:\d\d)(\d)(:\d\d)', 		r'\1\3'),
		
		#(r'^(\d:)$'						r'00:00:0\g<1>0'),
		(r'^(\d:\d\d)$',				r'00:00:0\1'),
		(r'^(\d:)$',					r'00:00:0\g<1>00'),
		(r'^(\d\d:)$',					r'00:00:\g<1>00'),
		(r'^(\d\d:\d\d:)$',				r'00:\g<1>00'),
		
		(r'^(\d)$',						r'00:00:00:0\1'),
		(r'^(\d\d)$',					r'00:00:00:\1'),
		(r'^(\d)(\d\d)$',				r'00:00:0\1:\2'),
		(r'^(\d\d)(\d\d)$',				r'00:00:\1:\2'),
		(r'^(\d)(\d\d)(\d\d)$',			r'00:0\1:\2:\3'),
		(r'^(\d\d)(\d\d)(\d\d)$',		r'00:\1:\2:\3'),
		(r'^(\d)(\d\d)(\d\d)(\d\d)$',	r'0\1:\2:\3:\4'),
		(r'^(\d\d)(\d\d)(\d\d)(\d\d)$',	r'\1:\2:\3:\4'),
		(r'(\d\d)(\d\d)',				r'\1:\2'), 		# 3113
		(r'^(\d\d:\d\d)$',				r'00:00:\1'),	# 41:34
		(r'^(\d\d:\d\d:\d\d)$',			r'00:\1'),		# 14:65:14
		(r'^(\d\d:\d\d:\d\d:)$',			r'\g<1>00'),# 14:65:14:

		(r'(\d\d)(\d)(:\d\d:\d\d:\d\d)',	r'\1\3'),
		(r'(\d)(\d\d:\d\d)',	r'00:0\1:\2')

		]
	count = 0
	isProper = False
	while count < 10 and isProper == False:
		for i in issues:
			timeString = re.sub(i[0], i[1],timeString)

		mo = re.fullmatch(r'\d\d:\d\d:\d\d:\d\d',timeString)

		if mo:
			isProper = True
			break

		count += 1
		
	if isProper == False:
		timeString = prevText

	linkedTable[row-1,col] = timeString