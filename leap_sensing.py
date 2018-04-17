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
    data.moveRight = True
    data.speed = 15

def isPointing(data):
    updateLeapMotionData(data)
    data.pointing = True
    for hand in data.frame.hands:
        for finger in hand.fingers:
            print data.fingerNames[finger.type], finger.direction[1]
            if data.fingerNames[finger.type] == 'Index' and not(-0.3 < finger.direction[1] < 0.3):
                data.pointing = False
            elif data.fingerNames[finger.type] in ['Ring', 'Middle', 'Pinky'] and finger.direction[1] > 0.1:
                data.pointing = False
    return data.pointing


def updateLeapMotionData(data):
    data.frame = data.controller.frame()

