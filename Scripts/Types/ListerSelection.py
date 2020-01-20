


class CueSelection:
    def __init__(self,start,end,name,row,col):
        self.CueInfo = {
            'startTime':start,
            'endTime':end,
            'name': name,
            'row': row-1,
            'col':col
        }

    def __getitem__(self,key):
        return self.CueInfo[key]