import time
import rtmidi
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    print "Virtual port opened"

# Colorblaze TRX 3ch RGB -> RGBAW

red = [0x91, 60, 127] # channel 2, middle C, velocity 127
green = [0x91, 61, 127]
blue = [0x81, 62, 127]
q = 'q'

red_off = [0x91, 60, 0]
green_off = [0x91, 61, 0]
blue_off = [0x81, 62, 0]

def allOff():
    midiout.send_message(red_off)
    midiout.send_message(blue_off)
    midiout.send_message(green_off)

while True:
    color = input('What color? ')
    allOff()
    if color == 'red':
        midiout.send_message(red)
    elif color == 'green':
        midiout.send_message(green)
    elif color == 'blue':
        midiout.send_message(blue)
    elif color == 'qqq':
        print 'quitting'
        allOff()
        del midiout
        break