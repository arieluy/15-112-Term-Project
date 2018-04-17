import time
import rtmidi
import leap_sensing
from lights import *
from Tkinter import *

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    print "Virtual port opened"


def init(data):
    data.midiout = midiout
    data.lights = set()
    leap_sensing.init(data)
    data.step = 1
    data.dim = False
    data.lights.add(Moving(1))
    data.lights.add(Moving(2))
    data.whichLight = 1

def mousePressed(event, data):
    fd_plus = [0x91, 1, 127]
    fd_minus = [0x91, 2, 127]
    if data.whichLight == 1:
        data.whichLight = 2
        data.midiout.send_message(fd_plus)
    elif data.whichLight == 2:
        data.whichLight = 1
        data.midiout.send_message(fd_minus)

def allOff(data):
    for light in data.lights:
        light.color = [0, 0, 0]
        light.intensity = 0
        light.position = [0, 0]

def keyPressed(event, data):
    if event.char == 'i':
        for light in data.lights:
            if light.channel == data.whichLight:
                if light.intensity >= 127:
                    light.intensity = 127
                else:
                    light.intensity += 16
    pos = ['p','t']
    for i in range(2):
        if event.char == pos[i]:
            for light in data.lights:
                if light.channel == data.whichLight:
                    if light.position[i] >= 111:
                        light.position[i] = 127
                    else:
                        light.position[i] += 16
    if event.keysym == 'space':
        allOff(data)
    elif event.char == 'd':
        data.dim = not data.dim
    elif event.char == 'q':
        print 'quitting'
        allOff(data)
        del midiout
    sendToLights(data)

def sendToLights(data):
    for light in data.lights:
        if light.channel == data.whichLight:
            f1 = [0x90, 60, light.intensity] # channel 1, middle C, velocity 127
            f2 = [0x90, 61, light.position[0]]
            f3 = [0x90, 62, light.position[1]]
            data.midiout.send_message(f1)
            data.midiout.send_message(f2)
            data.midiout.send_message(f3)

def f():
    pass

def timerFired(data):
    # if leap_sensing.isPointing(data):
    if data.dim:
        for light in data.lights:
            if light.intensity >= 127 or light.intensity <= 0:
                data.moveRight = not data.moveRight
            if data.moveRight:
                light.intensity += data.step
            elif light.intensity <= 1:
                light.intensity = 0
            else:
                light.intensity -= data.step
    sendToLights(data)



def redrawAll(canvas, data):
    for light in data.lights:
        offset = 0
        if light.channel == 2:
            offset = 50
        canvas.create_text(data.width/2, data.height/2 + offset, \
            text='intensity: ' + str(light.intensity) + 
                '  pan: ' + str(light.position[0]) + '  tilt: ' + str(light.position[1]))



####################################

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