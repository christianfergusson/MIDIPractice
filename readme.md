# Piano Sight Reading Practice

## Description

This is a python program made to provide practice with sight reading piano music.

It produces a pygame window that displays sheet music staves and generates an endless score by sliding in random notes from the right edge of the screen.

The program reads input values from a connected MIDI device and compares them to the foremost note, making the note disappear when the correct key is pressed, and pausing the note movement if the user falls far enough behind.

## To Do

- Automatic speed scaling based on rate of correct inputs
- Randomly varying note durations (with appropriate spacing and rests)
- Ability to generate one note on each staff simultaneously
- Ability to generate chords
- Ability to import sheet music

## Installation

Requires:
- Python 3
- PyGame
- MIDI Device (or use can be simulated with the keyboard)

## Operation

### Device Selection
<img src="images/titlescreen.png" alt="sample" width="80" height="80">

[IMAGE]

Initially, the UI will prompt for a MIDI device to be selected (or the user can re-scan the devices).

### Playing
[GIF]

Upon selection, the UI will display the staves and start moving notes toward the clefs from offscreen at regular spacing intervals. 

[GIF]

The goal is to press the piano (MIDI) key that corresponds with the leftmost note.  Pressing a wrong key will result in a red "X" symbol appearing for feedback, but has no other effect.

[GIF]

Pressing the correct key will display a green "O" symbol and will remove the leftmost note from the screen.  The remainder of the notes will continue moving leftward at constant speed.

### Movement
[GIF]

If the leftmost note reaches the bar line in front of the clef, the entire set of notes will stop.

[GIF]

They will resume moving any time that the leftmost note on the screen is not yet at the bar line, so playing a correct key and removing the foremost note will resume movement.

[GIF]

With multiple staves active, all sets of notes follow the same movement and do not pause or resume independently.

### USER SETTINGS:

Option | Details
-------|-------
Note Range			 | This limits the not generation to a certain range of notes, which can help the user focus their practice and can also act as a difficulty modifier<br>[2 IMAGE]
BPM					 | This sets the approximate speed at which the notes move, so that hitting the correct notes at this rate means the user will not fall behind or get ahead<br>[2 GIF]
Note Spacing		 | This changes the amount of horizontal space between each note on the staff in order to match visibility preference<br>[3 IMAGE]
Staves Active		 | This sets which staves are active (treble, bass, or both)<br>[3 IMAGE]
Accidentals			 | This toggles whether newly generated notes can sometimes have accidentals or never have them.  It will not affect notes already on the screen.<br>[2 IMAGE]
Note Type			 | This changes the note symbol (whole note, half note, or quarter note) in order to match visibility preference.  This does not affect rate of play at all.<br>[3 IMAGE]
Variable Note Length | This will make the newly generated notes have varying note lengths and can include rests in order to more realistically simulate actual sheet music.  While enabled, this makes the "Note Type" option irrelevant.<br>[2 IMAGE]
Simultaneous Notes	 | Disabled means that only a single note will be generated at each location, either on the treble staff or the bass staff.  Enabled means that a note will be generated on both staves for each note position, and so the left and right hands will need to play simultaneously.<br>[2 IMAGE]
Note Letter Display	 | This toggles whether or not the note name (e.g. "C#") will display above the notes.  This is useful early in a user's practice while they are still familiarizing themselves with the notes.<br>[2 GIF]
MIDI Value Display	 | This toggles whether or not the MIDI value (e.g. "64") will display above each note, as well as displaying the input values from the MIDI device above the topmost clef.  It can be used for diagnostics to compare to the input value from the MIDI device.<br>[2 GIF]