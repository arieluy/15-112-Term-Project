from __future__ import division
import rtmidi # from https://github.com/superquadratic/rtmidi-python
from lights import *
from Tkinter import *
from leap_sensing import *
from store_cues import *
from calculations import *
from buttons import *

import sys, thread, time, math
sys.path.insert(0, "../LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap # https://developer.leapmotion.com/sdk/v2/

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    print "Virtual port opened"

#####################################################

def init(data):
    data.background = PhotoImage(file='concert.gif')
    data.midiout = midiout
    data.timerDelay = 20
    data.lights = dict()
    data.lights[1] = Intelligent()
    LeapHand.init(LeapHand, data)
    data.step = 1
    data.dim = False
    data.currentLight = 1
    data.selection = None # keeps track of which attribute is selected
    data.timesFired = 0
    buttonsInit(data)
    data.writeCue = False
    data.sequence = []
    data.playCue = False
    data.nextNumber = 2
    data.recording = False
    data.currentSequence = None
    data.nextSequence = 1
    data.circleBlink = False
    data.selectMode = True
    data.twoHands = False

def mousePressed(event, data):
    inCategory = False
    for button in data.buttons: # picks which attribute to control
        if button.isClicked(event):
            inCategory = True
    for button in data.buttons:
        if inCategory:
            if button.isClicked(event):
                button.changeFill('yellow')
                data.selection = str(button)
            else:
                button.changeFill('white')

    inCategory = False
    for button in data.lightButtons: # picks which light to control
        if button.isClicked(event):
            inCategory = True
    for button in data.lightButtons:
        if inCategory:
            if button.isClicked(event):
                button.changeFill('yellow')
                oldLight = data.currentLight
                data.currentLight = int(str(button))
                switchLights(oldLight, data)
            else:
                button.changeFill('white')

    for button in data.sequenceButtons: # picks which sequence to play
        if button.isClicked(event):
            data.currentSequence = int(str(button))
            button.changeFill('cyan')
            data.playCue = True
            file = 'MySequence%d.py' % data.currentSequence
            execfile(file)
            data.playCue = False
            button.changeFill('white')

    newLight = None
    for button in data.newButtons: # creates new lights
        if button.isClicked(event):
            newLight = str(button)
    if newLight != None:
        k = len(data.lightButtons)
        data.lightButtons.append(Button(20, 50+30*k, 100, 50+30*(k+1), data.nextNumber))
    if newLight == 'light':
        data.lights[data.nextNumber] = Light()
        data.nextNumber += 1
    elif newLight == 'intelligent':
        data.lights[data.nextNumber] = Intelligent()
        data.nextNumber += 1
    elif newLight == 'moving':
        data.lights[data.nextNumber] = Moving()
        data.nextNumber += 1
    

# switch which light you are controlling
def switchLights(oldLight, data):
    fd_plus = [0x91, 1, 127]
    fd_minus = [0x91, 2, 127]
    d = data.currentLight - oldLight
    if d > 0:
        for i in range(d):
            data.midiout.send_message(fd_plus)
    elif d < 0:
        for i in range(abs(d)):
            data.midiout.send_message(fd_minus)


def allOff(data): # turn all lights off
    for i in data.lights:
        light = data.lights[i]
        light.color = [0, 0, 0]
        light.intensity = 0
        light.position = [0, 0]

# gives an alternate way to control the lights besides LeapMotion
def keyPressed(event, data):
    if event.char == 'r':
        k = len(data.sequenceButtons)
        if data.recording:
            writeSequence(data)
            data.sequenceButtons.append(Button(800, 50+30*k, 880, 50+30*(k+1), data.nextSequence))
            data.recording = False
            data.nextSequence += 1
        elif k < 9:
            data.recording = True
    if event.char == 'g':
        data.playCue = True
        MySequence1.playSequence(data)
        data.playCue = False
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
        del data.midiout
    if data.playCue == False:
        sendToLights(data)

# this encodes the MIDI cues to send to control the lights
def sendToLights(data):
    light = data.lights[data.currentLight]
    if data.selection == 'intensity':
        msg = [[0x90, 1, light.intensity]]
    elif data.selection == 'color' and isinstance(light, Intelligent):
        msg = [[0x90, 2, light.color[0]], [0x90, 3, light.color[1]], [0x90, 4, light.color[2]]]
    elif data.selection == 'position' and isinstance(light, Moving):
        tilt = int(128*(light.position[1] + 135)/270)
        pan = int(128*(light.position[0] + 270)/540)
        msg = [[0x90, 5, pan], [0x90, 6, tilt]]
    else:
        msg = []
    print msg
    for m in msg:
        data.midiout.send_message(m)
    if data.recording:
        data.sequence.append(writeCue(msg))


def timerFired(data):
    data.timesFired += 1

    if LeapHand.twoHands(LeapHand, data) != data.twoHands:
        if not data.twoHands:
            data.selectMode = not data.selectMode
        data.twoHands = not data.twoHands

    # you can select another attribute by bringing both of your hands into the frame
    if data.selectMode:
        if data.selection == 'intensity':
            data.selection = 'position'
            data.posButton.changeFill('yellow')
            data.intButton.changeFill('white')
            data.selectMode = False
        elif data.selection == 'color':
            data.selection = 'intensity'
            data.intButton.changeFill('yellow')
            data.colButton.changeFill('white')
            data.selectMode = False
        elif data.selection == 'position':
            data.selection = 'color'
            data.colButton.changeFill('yellow')
            data.posButton.changeFill('white')
            data.selectMode = False


    light = data.lights[data.currentLight]
    if (not data.selectMode) and data.timesFired % 10 == 0 and LeapHand.isHand(LeapHand, data):
        if data.selection == 'intensity':
            distance = LeapHand.handDistance(LeapHand, data)[1]
            intensity = getIntensityFromDistance(distance)
            light.changeIntensity(intensity)
        elif data.selection == 'color' and isinstance(light, Intelligent):
            tilt = LeapHand.handTilt(LeapHand, data)
            color = getColorFromTilt(tilt)
            light.changeColor(color)
            print color
        elif data.selection == 'position' and isinstance(light, Moving):
            pos = LeapHand.indexDirection(LeapHand, data)
            lst = getPossiblePositions(pos)
            pt = getPanTilt(lst, light.position) # find best position
            light.changePosition(pt)
        # print LeapHand.indexDirection(LeapHand, data)

    if data.dim: # This is the replacement in case Leap Motion doesn't work
        light = data.lights[data.currentLight]
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

    if data.timesFired % 8 == 0:
        data.circleBlink = not data.circleBlink

    if data.timesFired % 10 == 0:
        sendToLights(data)


def redrawAll(canvas, data):
    canvas.create_image(0, 0, image=data.background, anchor='nw')
    canvas.create_text(450, 200, text='15-112 Term Project', font='Arial 36 bold', fill='white')
    canvas.create_text(450, 250, text='Ariel Uy', font='Arial 20', fill='white')
    if data.recording:
        canvas.create_text(730, 35, text='RECORDING', font='Arial 10', fill='white')
        if data.circleBlink:
            canvas.create_oval(770, 30, 780, 40, fill='red')
    drawButtons(canvas, data)
    light = data.lights[data.currentLight]
    capt = 'intensity: %d' % (light.intensity)
    if isinstance(light, Intelligent):
        capt += ' color: (%d, %d, %d)' % (light.color[0], light.color[1], light.color[2])
    if isinstance(light, Moving):
        capt += ' pan: %d tilt: %d' % (light.position[0], light.position[1])
    canvas.create_text(data.width/2, data.height/2, text=capt, fill='white')



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
    data.timerDelay = 100
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

run(900, 600)