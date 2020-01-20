


class CueSelection:
    def __init__(self):

        self.StartTime = ''
        self.EndTime = ''
        self.Name = ''
        self.Row = 0
        self.WasTriggered = False
        self.triggerWord = 'GO'
        self.TimecodeOP= op.Tc
        self.Loop = 0
        
    def GetName(self):
        return self.Name
    
    def GetStartTime(self):
        return self.StartTime
    
    def GetEndTime(self):
        return self.EndTime
    
    def GetRowIndex(self):
        return self.Row-1
    
    def GetLoopState(self):
        return self.Loop

    def Build(self, row, col, rowData, cellText):
        self.__init__()
        self.StartTime = rowData['Start Time']
        self.EndTime = rowData['End Time']
        self.Name = rowData['Name']
        self.Row = row
        self.Loop = rowData['Loop']

        if cellText == self.triggerWord:
            self.WasTriggered = True
        
        # else:
        #     self.WasTriggered = False

    def GetTime(self):
        h, m, s, f = self.StartTime.split(':')
        return (h,m,s,f)

    def TriggerTimecodeChange(self):
        timeData = self.GetTime()
        self.TimecodeOP.par.Hour = timeData[0]
        self.TimecodeOP.par.Minute = timeData[1]
        self.TimecodeOP.par.Second = timeData[2]
        self.TimecodeOP.par.Frame = timeData[3]
        self.TimecodeOP.par.Resetpulse.pulse()

    
    def Debug(self):
        print(self)
        print("\n\nSelection:")
        print("Name: " , self.Name)
        print("Start Time: ", self.StartTime)
        print("End Time: ", self.EndTime)
        print("Row: ", self.Row)
        print("Was Trigger: ", self.WasTriggered, '\n\n')
        print("Loop State: ", self.Loop)





#print(TimecodeToSeconds('00:01:05:00'))