class Light(object):
    def __init__(self):
        self.intensity = 1

    def __repr__(self):
        return str(type(self)) + str(self.channel) + " at " + str(self.intensity)

    def changeIntensity(self, newIntensity):
        self.intensity = newIntensity



class Intelligent(Light):
    def __init__(self):
        super(Intelligent, self).__init__()
        self.color = [0, 0, 0] # red, green, blue

    def changeColor(self, newColor):
        self.Color = newColor



class Moving(Intelligent):
    def __init__(self):
        super(Moving, self).__init__()
        self.position = [0, 0] # pan, tilt

    def changePosition(self, newPosition):
        self.position = newPosition


