import time
import rtmidi
from Tkinter import *

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")
    print "Virtual port opened"

# Martin rush par RGBW 5ch



red_off = [0x80, 60, 0]
green_off = [0x80, 61, 0]
blue_off = [0x80, 62, 0]

def allOff():
    midiout.send_message(red_off)
    midiout.send_message(blue_off)
    midiout.send_message(green_off)

def init(data):
    data.color = set()
    data.midiout = midiout
    data.intensity = 100

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if event.keysym == 'Up':
        if data.intensity >= 80:
            data.intensity = 100
        else: 
            data.intensity += 20
    elif event.keysym == 'Down':
        if data.intensity <= 20:
            data.intensity = 0
        else:
            data.intensity -= 20
    if event.char == 'r':
        data.color.add('red')
    elif event.char == 'g':
        data.color.add('green')
    elif event.char == 'b':
        data.color.add('blue')
    elif event.keysym == 'space':
        allOff()
        data.color = set()
    elif event.char == 'q':
        print 'quitting'
        allOff()
        del midiout
    sendToLights(data)

def sendToLights(data):
    i = data.intensity*127//100
    red = [0x90, 60, i] # channel 1, middle C, velocity 127
    green = [0x90, 61, i]
    blue = [0x90, 62, i]
    if 'red' in data.color:
        data.midiout.send_message(red)
    if 'green' in data.color:
        data.midiout.send_message(green)
    if 'blue' in data.color:
        data.midiout.send_message(blue)


def redrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2, text=str(data.color) + str(data.intensity))



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

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
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
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)