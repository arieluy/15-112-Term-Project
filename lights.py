# creates classes of lights that inherit from each other

class Light(object):
    def __init__(self):
        self.intensity = 127

    def __repr__(self):
        return str(type(self))

    def changeIntensity(self, newIntensity):
        self.intensity = newIntensity



class Intelligent(Light):
    def __init__(self):
        super(Intelligent, self).__init__()
        self.color = [0, 0, 0] # red, green, blue

    def changeColor(self, newColor):
        self.color = newColor



class Moving(Intelligent):
    def __init__(self):
        super(Moving, self).__init__()
        self.position = [0, 0] # pan, tilt
        # pan has a domain of [-270, 270]
        # tilt has a domain of [-135, 135]

    def changePosition(self, newPosition):
        self.position = newPosition


