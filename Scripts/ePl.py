"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

SELECTOVERLAYER = 70
import time
from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions


class ePl:
	"""
	ePl description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		## ---------  OPS

		self.LinkedTable = self.ownerComp.op('linkedTable')
		assert self.LinkedTable
		
		self.Lister= self.ownerComp.op('lister')
		assert self.Lister
	

		self.TcOp = op.Tc
		assert self.TcOp

		self.Timer = self.ownerComp.op('timer2')
		assert self.Timer

		self.TimerInfoDat = self.ownerComp.op('info1')
		assert self.TimerInfoDat

		self.TimerInfoChop = self.ownerComp.op('info2')
		assert self.TimerInfoChop

		self.SegmentsDat = self.ownerComp.op('null_segments')
		assert self.SegmentsDat

		## ---------- CONSTANTS
		self.LoopCol = 3
		self.RunRadio = 4

		# an object containing my Transport buttons
		# subscript op is overriden so get buttons by subscripting
		self.Transport = mod.Transport.Transport()
		assert self.Transport

		self.TransportOp = op.Transport
		assert self.TransportOp

		self.SumList = self.ownerComp.op('null_SumList')
		assert self.SumList

		self.Segment = 0

		self.PlayState = 0  # stopped, play, paused

	


	def ToggleLoop(self, row):

		
		LoopState = int(self.LinkedTable[row,3].val)


		#op('lister').par.Linkedtable = ''
		self.LinkedTable[row,3] = int(not LoopState)
		
		#self.Lister.par.Refresh.pulse()
		#op('lister').par.Linkedtable = self.LinkdTable.path

	def RadioPlay(self, row , keepActive = False):
		linkedTableLength = self.LinkedTable.numRows
		#debug(project.pythonStack())
		
		# we use an invalid number to reset with. it's valid if it's greater than 0
		if row >= 0:
			curState = int(self.LinkedTable[row,self.RunRadio].val)

		else:
			curState = None # nothing, we don't even use this.
		
		if self.ownerComp.par.Debug:
			debug("Radio Play triggered for row: ", row)
			debug("Current Button State: ", curState)
		
		# make everything in our table 0, 0 makes all the go buttons green
		for i in range(linkedTableLength):
			self.LinkedTable[i,self.RunRadio] = 0
			
		if self.ownerComp.par.Debug.eval():
			debug(project.pythonStack())

		if row == -1:
			# this means reset everything back to default
			return
		else:
			# change the one we clicked back to the red stop button
			if curState == 0:
				self.LinkedTable[row,self.RunRadio] = 1
				self.Start()

			elif curState == 1:
				self.Stop()


	## --------- Transport

	def Stop(self):
		#debug(project.pythonStack())
		self.TcOp.par.Play = False
		self.Timer.par.play = False
		self.TransportOp.par.Radioindex = 0
		self.PlayState = 0
		self.OutputStatus = False
		
	def Start(self):
		self.TcOp.par.Play = True
		self.Timer.par.play = True
		self.TransportOp.par.Radioindex = 1
		self.PlayState = 1
		self.OutputStatus = True

	def Pause(self, nextSegmentIsBeingFired = True):
		curSegment = int(self.Timer['segment'])
		try:
			if nextSegmentIsBeingFired == False:
				self.LinkedTable[curSegment,4] = 2
				self.TransportOp.par.Radioindex = 2
				self.TcOp.par.Outputstatus = False

			else:
				self.LinkedTable[curSegment,4] = 1
		except:
			return
		
		#print(project.pythonStack())
		self.PlayState = 2

	def Unpause(self):
		curSegment = int(self.Timer['segment'])
		self.LinkedTable[curSegment,self.RunRadio] = 1
		#print(self.LinkedTable[curSegment,4].val)
		self.PlayState = 1


	## --------- Table Manipulation

	def ResetRadio(self):
		# sets all buttons back to default, but doesn't stop anything
		self.RadioPlay(-1)

	def ResetSegment(self):
		# Resets the current segment back to default
		# resets the timecode, and the timer
		
		'''
		tc.par.Play = False
		tc.par.Resetpulse.pulse()
		'''
		self.TcOp.par.Play = False	
		self.ResetRadio()
		self.SetSegment(self.Timer['segment'])
		# get current segment's start time in seconds
		segmentSeconds = self.GetCurrentSegmentStartSeconds()

		segmentStartTime = self.SecondsToTcTuple(segmentSeconds,self.FrameRate)
		self.TriggerTimecodeChangeWithFloats(segmentStartTime)

	## --------- Timecode Manipulation

		###  --- Triggering Timecode Changes
	def TriggerTimecodeChange(self, timeString, TOD = False):

		if TOD: # time of day...
			hmsf = (self.TcOp.op('null_TOD')['hour'], 
				self.TcOp.op('null_TOD')['min'],
				self.TcOp.op('null_TOD')['sec'],
				self.TcOp.op('null_TOD')['hour']
			)

			self.TriggerTimecodeChangeWithFloats(hmsf)
		else:
			hmsf = self.TcStringToTuple(timeString)
		
			self.Hour, self.Minute, self.Second, self.Frame = hmsf
			#print(project.pythonStack())
			self.TcOp.par.Resetpulse.pulse()

	def TriggerTimecodeChangeWithFloats(self, hmsf):
		
		self.Hour, self.Minute, self.Second, self.Frame = hmsf

		self.TcOp.par.Resetpulse.pulse()


	##################################
	#			REDO
	
	# string conversions
	def TcStringToTuple(self, timecode: str) -> tuple:
		h, m, s , f = timecode.split(':')
		return (h,m,s,f)

	def TcTupleToString(self, timecode: tuple ) -> str:
		return "%d:%02d:%02d:%02d" % (hour, m, sec,frames) 

	# seconds conversions
	def TcTupleToSeconds(self, tc: tuple, framerate: float) -> float:
		return int(tc[0]) * 3600 + int(tc[1]) * 60 + int(tc[2]) + int(tc[3]) / framerate

	def SecondsToTcTuple(self, inputSeconds: float, framerate: float) -> tuple:
		frames = int((inputSeconds - int(inputSeconds)) * framerate)
		m, sec = divmod(inputSeconds, 60) 
		hour, m = divmod(m, 60) 
		return (hour,m,sec,frames)
	
	# current tc getters
	def GetCurrentTimecodeInSeconds(self) -> float: 
		return self.TcTupleToSeconds(self.GetCurrentTimecodeAsTuple(), self.FrameRate)
	
	def GetCurrentTimecodeAsString(self) -> str:
		return self.TcTupleToString(self.GetCurrentTimecodeTuple())

	def GetCurrentTimecodeAsTuple(self) -> tuple:
		return (self.Hour,self.Minute,self.Second,self.Frame)
		
	# segment Timecode getters
	def GetRunningSegmentTcInSeconds(self) -> float:
		runningSeconds = self.TimerInfoChop['frames_segment'].eval() / self.FrameRate
		currentSegmentStart = self.GetCurrentSegmentStartSeconds()
		return runningSeconds/2 + currentSegmentStart
		
	def GetCurrentSegmentStartSeconds(self) -> float:
		tcString = self.LinkedTable[self.GetCurrentSegment(),1].val
		tcTuple = self.TcStringToTuple(tcString)
		return self.TcTupleToSeconds(tcTuple,self.FrameRate)
	
	def GetCurrentSegmentEndSeconds(self) -> float:
		tcString = self.LinkedTable[self.GetCurrentSegment(),2].val
		tcTuple = self.TcStringToTuple(tcString)
		return self.TcTupleToSeconds(tcTuple,self.FrameRate)

	####################################
	## --------- Timer Sets

	def SetSegment(self, segment):
		self.Segment = int(segment)
		self.Timer.goTo(segment = self.Segment)
		#self.ownerComp.op('lister').SetRowLook(self.Segment+1, 'rowSeg', True, 1010)
		#stackprint(self.Segment)

	def ScrubDo(self, direction, increment):
		#direction = -1 for back, 1 for forward
		#todo- fix this... the math is wrong.  Keeps skipping segments
		#todo - see if there is a better way

		try:
			segmentMin = float(self.SumList[int(self.Segment),0].val)
			segmentMax = float(self.SumList[int(self.Segment+1),0].val)
		except Exception as e:
			if self.ownerComp.par.Debug:
				debug(e)
			return


		# currentTime = self.GetCurrentSegmentTime()

		currentTime = self.Timer['cumulative_seconds'].eval()
		newTime = currentTime + increment * direction
		frameLength = (1000 / self.FrameRate)*.001

		segmentTime = min(max(segmentMin, newTime),segmentMax-frameLength) #go to the last frame

		# Running timecode is the start time + time since start of playing
		timecodeSeconds= self.GetRunningSegmentTcInSeconds()

		# segment start in seconds
		currentSegmentStart = self.GetCurrentSegmentStartSeconds()
		
		timecodeSeconds += increment * direction

		# clamp the values between the start and end of the segment
		finalTimecodeSeconds = min(max(timecodeSeconds,currentSegmentStart),self.GetCurrentSegmentEndSeconds())
		
		#Seconds to HMSF returns a tuple like - (h,m,s,f)
		# TriggerTimecodeChangeWithFloats uses the tuple rather than a time string.

		# to do - probably we should only have one and convert to tuple instead of having two
		self.TriggerTimecodeChangeWithFloats(self.SecondsToTcTuple(finalTimecodeSeconds,self.FrameRate))

		# todo - fix a bug where jumping doesn't always land on the same frame...
		self.Timer.goTo(seconds = segmentTime)
		
		self.Pause()
		
		if self.ownerComp.par.Debug:
			debug('segment min: ', segmentMin)
			debug('segment max: ', segmentMax)
			debug('Segment Time: ', segmentTime)

	
	## --------- Timer Gets

	def GetTime(self, timeString):
		try:
			h, m, s, f = timeString.split(':')
			return (h,m,s,f)

		except:
			return (0,0,0,0)
		
	def GetCurrentSegment(self):
		return int(self.Timer['segment'])

	def GetCurrentSegmentTime(self):
		curSegment = self.GetCurrentSegment() + 1
		curLength = float(self.ownerComp.op('null_segments')[curSegment,'length'].val)
		if self.ownerComp.par.Debug:
			print('curSegment ', curSegment)

			debug(curLength, "Debug")
		return self.Timer.fraction / curLength


	## --------- Playlist Building

	def NewPlaylist(self):
		name = self.GetNewCueName()
		self.LinkedTable.appendRow([name,'00:00:00:00', '00:01:00:00', 0,0])

	
	def GetNewCueName(self):
		field = op('field_NewCueString')
		return field.par.Value0


	## ----------  properties

	@property
	def FrameRate(self):
		return self.TcOp.par.Framerate.eval()

	@property
	def Hour(self):
		return self.TcOp.par.Hour.eval()
	
	@Hour.setter
	def Hour(self,val):
		self.TcOp.par.Hour = val

	@property
	def Minute(self):
		return self.TcOp.par.Minute.eval()
	
	@Minute.setter
	def Minute(self,val):
		self.TcOp.par.Minute = val
	
	
	@property
	def Second(self):
		return self.TcOp.par.Second.eval()
	
	@Second.setter
	def Second(self,val):
		self.TcOp.par.Second = val

	@property
	def Frame(self):
		return self.TcOp.par.Frame.eval()
	
	@Frame.setter
	def Frame(self,val):
		self.TcOp.par.Frame = val


	@property
	def OutputStatus(self):
		return self.TcOp.par.OutputStatus

	@OutputStatus.setter
	def OutputStatus(self,val):
		if parent.GUI.par.Outputenabled:
			self.TcOp.par.Outputstatus = val