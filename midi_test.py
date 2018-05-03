print('Hello world!')

# this is a test from https://github.com/superquadratic/rtmidi-python

import time
import rtmidi 
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
    print 'hi'
else:
    midiout.open_virtual_port("My virtual output")

note_on = [0x91, 1, 112] # channel 1, middle C, velocity 112
note_off = [0x81, 1, 0]
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)

del midiout
