from Tkinter import *

class Button(object):
    def __init__(self):
        '''self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.label = label'''
        self.fill = 'white'

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