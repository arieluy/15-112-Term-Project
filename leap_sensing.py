import sys, thread, time
sys.path.insert(0, "../LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap

class LeapHand(object):
    # Some code from Leap Motion SDK v2 sample files https://developer.leapmotion.com/sdk/v2/
    # Also from 112 starter code
    @staticmethod
    def init(self, data):
        data.controller = Leap.Controller()
        data.frame = data.controller.frame()
        data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        data.pointing = False
        data.increasing = True
        data.speed = 15

    @staticmethod
    def isPointing(self, data): # check if a hand is pointing at the screen or not
        data.frame = data.controller.frame() # updates Leap Motion data
        data.pointing = True
        for hand in data.frame.hands:
            for finger in hand.fingers:
                # print data.fingerNames[finger.type], finger.direction
                if data.fingerNames[finger.type] == 'Index' and not(-0.3 < finger.direction[1] < 0.3):
                    data.pointing = False
                elif data.fingerNames[finger.type] in ['Ring', 'Middle', 'Pinky'] and finger.direction[1] > 0.1:
                    data.pointing = False
        return data.pointing

    @staticmethod
    def indexDirection(self, data):
        data.frame = data.controller.frame()
        for hand in data.frame.hands:
            for finger in hand.fingers:
                if finger.type == 1:
                    return finger.direction

    @staticmethod
    def isHand(self, data):
        data.frame = data.controller.frame()
        for hand in data.frame.hands:
            return True
        return False

    @staticmethod
    def handDistance(self, data):
        frame = data.controller.frame()
        hand = frame.hands[0]
        return hand.palm_position

    @staticmethod
    def handTilt(self, data):
        frame = data.controller.frame()
        hand = frame.hands[0]
        return hand.palm_normal.roll

