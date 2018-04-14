
import os, sys, inspect, thread, time
sys.path.insert(0, "../LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")

import Leap


from Tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    updateLeapMotionData(data)
    printLeapMotionData(data)

def updateLeapMotionData(data):
    data.frame = data.controller.frame()

def printLeapMotionData(data):
    frame = data.frame

    print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
          frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

    # Get hands
    for hand in frame.hands:

        handType = "Left hand" if hand.is_left else "Right hand"

        print "  %s, id %d, position: %s" % (
            handType, hand.id, hand.palm_position)

        # Get the hand's normal vector and direction
        normal = hand.palm_normal
        direction = hand.direction

        # Calculate the hand's pitch, roll, and yaw angles
        print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            direction.pitch * Leap.RAD_TO_DEG,
            normal.roll * Leap.RAD_TO_DEG,
            direction.yaw * Leap.RAD_TO_DEG)

        # Get arm bone
        arm = hand.arm
        print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            arm.direction,
            arm.wrist_position,
            arm.elbow_position)

        # Get fingers
        for finger in hand.fingers:

            print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                data.fingerNames[finger.type],
                finger.id,
                finger.length,
                finger.width)

            # Get bones
            for b in range(0, 4):
                bone = finger.bone(b)
                print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    data.boneNames[bone.type],
                    bone.prev_joint,
                    bone.next_joint,
                    bone.direction)

def redrawAll(canvas, data):
    # draw in canvas
    pass

####################################
# use the run function as-is
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

run(400, 200)
