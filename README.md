# LTC-Timecode-Generator

To begin using this tool, create a new playlist (file->New) and add new cues. (New Cue Button)

## Release History - 

### 1.07
Timecode readout is now substantially more efficient because the numbers are all using cache selects.  On startup, values 0-60 are stored in a cache top. The timecode readout as well as the countdown are simply retrieving these from cache. 

### 1.03 
Fixed an issue with icon usage on Mac os. Fixed a mac version issue with text slightly shifting due to auto sizing.



## Cue List Window - 

Here you can build out your cues. Add a new cue with the "New Cue" button. Set your start and end time, decide if you want it to loop, and hit Go.  Double click the name column to rename your cues.
There is some decent auto correct and some additional features for entering in time.

A quick map of what you can enter - 

Naming a cue TOD will begin timecode at the current TOD. This MIGHT drift out of sync over long periods of time.

1h = 01:00:00:00

01h = 01:00:00:00

1h30 = 01:30:00:00

01h30m = 01:30:00:00

0100 = 00:00:01:00

100000 = 00:10:00:00

Down the line...

There's also a checker to ensure you don't accidentally make the start time after the end time. (Thanks Brian!)

## Countdown Window - 

This shows your cue name and the countdown to 0.

## Timecode Window - 

Shows you current timecode with an analog clock readout that noone asked for, but got anyway.

## Transport Window - 

The Left / Right buttons - 

Ctrl+click = 1 sec

Ctrl+shift+click = 5 sec

Click = 10 sec

## Dropdown Menu -

### File - 

Save All saves the project which I don't recommend. It will most likely lock up briefly.  Ctrl.S also does this.

Save Cue List saves your cue list to your "CueLists" folder. This folder is automatically generated when you bring the tox into your project. 

Save As- make sure you put these inside of the cue list folder.

### Settings - 

Edit Look - 

Allows you to configure the color and look of most of the panels. I'd be cautious changing the colors during a show, personally.

Audio Config - 

The Active Toggle is read only because under the hood I'm using that whenever you pause or stop. TD continues to send timecode out even when you pause so this was the best solution.

### Window - 

This just allows you to bring back the panels that you closed out of.




