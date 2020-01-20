


def TimecodeToSeconds(timecode, framerate=60):
    try:
        h, m, s , f = timecode.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(f) / framerate

    except Exception as e:
        if parent.Playlist.par.Debug:
            debug(e)
        return 0
    





#print(TimecodeToSeconds('00:01:05:00'))