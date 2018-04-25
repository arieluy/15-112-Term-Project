from __future__ import division
import rtmidi # from https://github.com/gostopa1/BachMC/blob/master/RunRealtime_dur_amp.py
from lights import *
from Tkinter import *
from leap_sensing import *
import sys, thread, time, math
sys.path.insert(0, "../LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    print "Virtual port opened"



class Button(object):
    def __init__(self, x1, y1, x2, y2, label):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.label = label
        self.fill = 'white'

    def __repr__(self):
        return self.label

    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.fill)
        canvas.create_text((self.x1 + self.x2)/2, (self.y1 + self.y2)/2, text=self.label)

    def changeFill(self, newFill):
        self.fill = newFill

    def isClicked(self, event):
        if (self.x1 <= event.x <= self.x2) and (self.y1 <= event.y <= self.y2):
            return True
        else:
            return False

def init(data):
    data.midiout = midiout
    data.lights = dict()
    LeapHand.init(LeapHand, data)
    data.step = 1
    data.dim = False
    data.lights[1] = Moving()
    data.lights[2] = Moving()
    data.currentLight = 1
    data.selection = None # keeps track of which attribute is selected
    data.timesFired = 0
    intButton = Button(20, 20, 100, 50, 'intensity')
    colButton = Button(120, 20, 200, 50, 'color')
    posButton = Button(220, 20, 300, 50, 'position')
    data.buttons = [intButton, colButton, posButton]

def mousePressed(event, data):
    for button in data.buttons:
        if button.isClicked(event):
            button.changeFill('yellow')
            data.selection = str(button)
            print(data.selection)
        else:
            button.changeFill('white')


'''# switch between lights
    fd_plus = [0x91, 1, 127]
    fd_minus = [0x91, 2, 127]
    if data.currentLight == 1:
        data.currentLight = 2
        data.midiout.send_message(fd_plus)
    elif data.currentLight == 2:
        data.currentLight = 1
        data.midiout.send_message(fd_minus)'''

def allOff(data): # turn all lights off
    for i in data.lights:
        light = data.lights[i]
        light.color = [0, 0, 0]
        light.intensity = 0
        light.position = [0, 0]

def keyPressed(event, data):
    light = data.lights[data.currentLight]
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
    light = data.lights[data.currentLight]
    f1 = [0x90, 60, light.intensity] # channel 1, middle C, velocity 127
    f2 = [0x90, 61, light.position[0]]
    f3 = [0x90, 62, light.position[1]]
    data.midiout.send_message(f1)
    data.midiout.send_message(f2)
    data.midiout.send_message(f3)

def getPossiblePositions(pos):
    x = pos[0]
    y = pos[1]
    z = pos[2]
    theta = math.acos(y/(math.sqrt(x**2 + y**2 + z**2)))
    phi = math.atan2(x, z)
    tilt = int(128*(theta/math.pi))
    pan = int(64*(phi/math.pi + 1))
    return [pan, tilt]

def timerFired(data):
    data.timesFired += 1
    light = data.lights[data.currentLight]
    if data.timesFired % 10 == 0:
        if isinstance(light, Intelligent) and LeapHand.isHand(LeapHand, data):
            pos = LeapHand.indexDirection(LeapHand, data)
            lst = getPossiblePositions(pos)
            # find best position
            light.changePosition(lst)
        print LeapHand.indexDirection(LeapHand, data)
    # if LeapHand.isPointing(LeapHand, data):
    if data.dim: # This is the replacement in case Leap Motion doesn't work
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
    for button in data.buttons:
        button.draw(canvas)
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