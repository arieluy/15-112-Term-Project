# Some code from Leap Motion sample files
# Also from 112 starter code

import sys, thread, time
sys.path.insert(0, "../LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap

from Tkinter import *

#############################################

def init(data):
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.pointing = False
    data.circRadius = 50
    data.circX = data.width/2
    data.circY = data.height/2
    data.moveRight = True
    data.speed = 15


def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    updateLeapMotionData(data)
    data.pointing = True
    for hand in data.frame.hands:
        for finger in hand.fingers:
            print data.fingerNames[finger.type], finger.direction[1]
            if data.fingerNames[finger.type] == 'Index' and not(-0.3 < finger.direction[1] < 0.3):
                data.pointing = False
            elif data.fingerNames[finger.type] in ['Ring', 'Middle', 'Pinky'] and finger.direction[1] > 0.1:
                data.pointing = False
    if not data.pointing:
        if data.circX <= 0 or data.circX >= data.width:
            data.moveRight = not data.moveRight
        if data.moveRight:
            data.circX += data.speed
        else:
            data.circX -= data.speed




def updateLeapMotionData(data):
    data.frame = data.controller.frame()


def redrawAll(canvas, data):
    x = data.circX
    y = data.circY
    r = data.circRadius
    canvas.create_oval(x-r, y-r, x+r, y+r, fill='blue')


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
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)

