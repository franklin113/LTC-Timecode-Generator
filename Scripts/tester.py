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
import "Types/CueSelection.py"
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



def TimecodeToSeconds(timecode: string):
    
    timecode = timecode.split(':')

    


# def onSelectRow(info):
# 	print(info)

selectedCue = CueSelection()
Playlister = parent.Playlist
def onClick(info):
    #pprint(info)
    #pprint(info['rowData']['Name'])

    row = info['row']
    col = info['col']

    if row >= 0 and col >= 0:

        try:
            selectedCue.Build(info['row'], info['col'], info['rowData'], info['cellText'])
            if Playlister.par.Debug:
                
                selectedCue.Debug()
        except Exception as e:
            debug(e)
    else:
        pass






