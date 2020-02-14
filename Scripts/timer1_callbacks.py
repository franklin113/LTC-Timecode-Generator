# me - this DAT.
# timerOp - the connected Timer CHOP
# cycle - the cycle index
# segment - the segment index
# fraction - the time in fractional form
#
# interrupt - True if the user initiated a premature
# interrupt, False if a result of a normal timeout.
#
# onInitialize(): if return value > 0, it will be
# called again after the returned number of frames.

Pl = parent.Playlist
linkedTable = Pl.op('linkedTable')

'''

The timer callbacks handle:

onSegmentEnter- 
	-changes the lister radio buttons via ePl.RadioPlay
	-triggers the timecode change via ePl.TriggerTimecodeChange

onSegmentExit-
	-pause the timers on the next cue

onCycle-
	-start the timecode over via ePl.TriggerTimecodeChange


'''


def onInitialize(timerOp):
	return 0

def onReady(timerOp):
	return
	
def onStart(timerOp):
	return
	
def onTimerPulse(timerOp, segment):
	return

def whileTimerActive(timerOp, segment, cycle, fraction):
	return

def onSegmentEnter(timerOp, segment, interrupt):
	
	if timerOp['running_seconds'] > .2:
		# to ensure that we aren't running this on the first play, we make sure the timer has 
		# been running for at least a second
		Pl.RadioPlay(segment)
		try:
			Pl.TriggerTimecodeChange(linkedTable[segment,1].val)
		except IndexError as e:
			debug(e)
	return
	
def onSegmentExit(timerOp, segment, interrupt):
	#debug("Segment: ", segment+2)
	#Pl.Pause()

	return

def onCycleStart(timerOp, segment, cycle):
	return

def onCycleEndAlert(timerOp, segment, cycle, alertSegment, alertDone, interrupt):
	return
	
def onCycle(timerOp, segment, cycle):
	#setting the cycle state is handled inside of the segments dat
	try:
		Pl.TriggerTimecodeChange(linkedTable[segment,1].val)
	except IndexError as e:
		debug(e)
	return

def onDone(timerOp, segment, interrupt):
	timerOp.par.play = False
	return
	