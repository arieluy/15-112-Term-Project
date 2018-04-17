import rtmidi
from lights import *
from Tkinter import *
from leap_sensing import *
import sys, thread, time
sys.path.insert(0, "../LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    print "Virtual port opened"


def init(data):
    data.midiout = midiout
    data.lights = dict()
    LeapHand.init(LeapHand, data)
    data.step = 1
    data.dim = False
    data.lights[1] = Moving()
    data.lights[2] = Moving()
    data.whichLight = 1

def mousePressed(event, data): # switch between lights
    fd_plus = [0x91, 1, 127]
    fd_minus = [0x91, 2, 127]
    if data.whichLight == 1:
        data.whichLight = 2
        data.midiout.send_message(fd_plus)
    elif data.whichLight == 2:
        data.whichLight = 1
        data.midiout.send_message(fd_minus)

def allOff(data): # turn all lights off
    for i in data.lights:
        light = data.lights[i]
        light.color = [0, 0, 0]
        light.intensity = 0
        light.position = [0, 0]

def keyPressed(event, data):
    light = data.lights[data.whichLight]
    if event.char == 'i': # intensity 
        if light.intensity >= 127:
            light.intensity = 127
        else:
            light.intensity += 16
    pos = ['p','t'] # pan, tilt
    for i in range(2):
        if event.char == pos[i]:
            if light.position[i] >= 111:
                light.position[i] = 127
            else:
                light.position[i] += 16
    if event.keysym == 'space': # clear
        allOff(data)
    elif event.char == 'd':
        data.dim = not data.dim
    elif event.char == 'q':
        print 'quitting'
        allOff(data)
        del midiout
    sendToLights(data)

def sendToLights(data):
    for i in data.lights:
        light = data.lights[data.whichLight]
        f1 = [0x90, 60, light.intensity] # channel 1, middle C, velocity 127
        f2 = [0x90, 61, light.position[0]]
        f3 = [0x90, 62, light.position[1]]
        data.midiout.send_message(f1)
        data.midiout.send_message(f2)
        data.midiout.send_message(f3)

def timerFired(data):
    if LeapHand.isPointing(LeapHand, data):
    # if data.dim: This is the replacement in case Leap Motion doesn't work
        for i in data.lights:
            light = data.lights[i]
            if light.intensity >= 127:
                data.increasing = False
            elif light.intensity <= 0:
                data.increasing = True
            if data.increasing:
                light.intensity += data.step
            elif light.intensity <= 1:
                light.intensity = 0
            else:
                light.intensity -= data.step
    sendToLights(data)



def redrawAll(canvas, data):
    for i in data.lights:
        light = data.lights[i]
        offset = 0
        if i == 2:
            offset = 50
        canvas.create_text(data.width/2, data.height/2 + offset, \
            text='intensity: ' + str(light.intensity) + 
                '  pan: ' + str(light.position[0]) + '  tilt: ' + str(light.position[1]))



####################################

# from 112 course notes
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)