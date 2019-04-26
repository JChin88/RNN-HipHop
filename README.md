# RNN-HipHop
## Overview
The RNN is used to generate a backing track for a hip-hop song. A MIDI file is fed through parseMIDI.py in order to separate the tracks and transpose each track. The input is then fed through the RNN in order to learn the different tracks. A random vector is then fed in in order to generate an output.

## How it's used
Input MIDI files are to be placed in the MIDIFiles folder. Each track in the file is then parsed and placed into the tracks folder. Finally, each track in the folder is transposed into all 12 keys and placed into the input folder

## Technical Description
['rnn_hip_hop.py'](rnn_hip_hop.py): This is the RNN used to generate the melodies

['parseMIDI.py'](parseMIDI.py): This is the program used to parse through the MIDI files and convert them into a format that the RNN can read, and then reconstruct the output into a MIDI file