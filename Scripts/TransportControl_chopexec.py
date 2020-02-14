# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
tc = op.Tc
Pl = op.Playlist
Kb = op.Kb

audioOp = op.Tc.op('audiodevout1')
outputState = parent.GUI.par.Outputenabled

def onOffToOn(channel, sampleIndex, val, prev):
	
	if channel.name == 'stop':
		tc.par.Play = False
		tc.par.Resetpulse.pulse()
		Pl.ResetSegment()
		SetAudioState(False)

	elif channel.name == 'play':
		tc.par.Play = True
		Pl.Unpause()
		SetAudioState(True)


	elif channel.name == 'pause':
		tc.par.Play = False
		Pl.Pause(nextSegmentIsBeingFired = False)
		SetAudioState(False)

	elif channel.name == 'start':
		tc.par.Resetpulse.pulse()

	elif channel.name == 'left':
		increment = GetIncrement()
		Pl.ScrubDo(-1, increment)
		SetAudioState(False)
		
		
	elif channel.name == 'right':
		increment = GetIncrement()
		Pl.ScrubDo(1, increment)
		SetAudioState(False)


	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):

	return
	
def GetIncrement():



	#returns an increment value based on the keyboard combo

	# ctrl = 1
	# ctrl+shift = 5
	# just click = 10

	if Kb.par.Ctrl and Kb.par.Shift != True:
		increment = 1
	elif Kb.par.Ctrl and Kb.par.Shift:
		increment = 5
	elif Kb.par.Ctrl != True and Kb.par.Shift != True:
		increment = 10
	return increment

def SetAudioState(state):
	if not outputState.eval():
		state = False
	audioOp.par.active = state
		

