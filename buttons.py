from Tkinter import *
from lights import *

class Button(object): 
    def __init__(self, x1, y1, x2, y2, label):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.label = str(label)
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

def buttonsInit(data):
    newLightButton = Button(120, 50, 200, 80, 'light')
    newIntelligentButton = Button(120, 80, 200, 110, 'intelligent')
    newMovingButton = Button(120, 110, 200, 140, 'moving')
    data.intButton = Button(220, 50, 300, 80, 'intensity')
    data.colButton = Button(220, 80, 300, 110, 'color')
    data.posButton = Button(220, 110, 300, 140, 'position')
    data.buttons = [data.intButton, data.colButton, data.posButton]
    data.newButtons = [newLightButton, newIntelligentButton, newMovingButton]
    data.lightButtons = [Button(20, 50, 100, 80, 1)]
    data.sequenceButtons = []

def drawButtons(canvas, data):
    canvas.create_rectangle(20, 20, 100, 50, fill='black')
    canvas.create_text(60, 35, text='lights', fill='white')
    canvas.create_rectangle(120, 20, 200, 50, fill='black')
    canvas.create_text(160, 35, text='add new:', fill='white')
    canvas.create_rectangle(220, 20, 300, 50, fill='black')
    canvas.create_text(260, 35, text='attribute', fill='white')
    canvas.create_rectangle(800, 20, 880, 50, fill='black')
    canvas.create_text(840, 35, text='sequence', fill='white')

    data.intButton.draw(canvas)
    light = data.lights[data.currentLight]
    if isinstance(light, Intelligent):
        data.colButton.draw(canvas)
    if isinstance(light, Moving):
        data.posButton.draw(canvas)

    for button in data.newButtons:
        button.draw(canvas)
    for button in data.lightButtons:
        button.draw(canvas)
    for button in data.sequenceButtons:
        button.draw(canvas)

