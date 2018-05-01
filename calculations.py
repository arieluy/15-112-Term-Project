import math

def getIntensityFromDistance(distance):
    distance -= 40
    if distance <= 0:
        distance = 0
    elif distance >= 180:
        distance = 180
    return int(distance*127//180)

def getColorFromTilt(tilt): # fades through the rainbow
    maxm = 127
    slope = maxm/60
    if tilt >= 2.5:
        tilt = 2.5
    elif tilt <= -2:
        tilt = -2
    tilt = (tilt+2)*90
    if tilt < 60:
        r = maxm
        g = tilt*slope
        b = 0
    elif tilt < 120:
        r = maxm-(tilt-60)*slope
        g = maxm
        b = 0
    elif tilt < 180:
        r = 0
        g = maxm
        b = (tilt-120)*slope
    elif tilt < 240:
        r = 0
        g = maxm-(tilt-180)*slope
        b = maxm
    elif tilt < 300:
        r = (tilt-240)*slope
        g = 0
        b = maxm
    elif tilt < 360:
        r = maxm
        g = 0
        b = maxm-(tilt-300)*slope
    else:
        r = maxm
        g = ((tilt-360)*slope*2) % 127
        b = ((tilt-360)*slope*2) % 127
    return [int(r), int(g), int(b)]

# converts from rectangular to spherical coordinates
def getPossiblePositions(pos):
    x = pos[0]
    y = pos[1]
    z = pos[2]
    theta = 180 - math.degrees(math.acos(y/(math.sqrt(x**2 + y**2 + z**2))))
    if theta >= 135:
        theta = 135
    phi = math.degrees(math.atan2(x, z))
    return findAllPositions(phi, theta)

def findAllPositions(phi, theta):
    lst = [(phi, theta)]
    if phi + 360 <= 270:
        lst.append([phi + 360, theta])
    if phi - 360 >= -270:
        lst.append([phi - 360, theta])
    if phi + 180 <= 270:
        lst.append([phi + 180, -theta])
    if phi - 180 >= -270:
        lst.append([phi - 180, -theta])
    return lst

def getPanTilt(lst, pos):
    bestPosition = None
    bestDistance = 1000000
    for item in lst:
        currentDistance = (item[0] - pos[0])**2 + (item[1] - pos[1])**2
        if currentDistance < bestDistance:
            bestDistance = currentDistance
            bestPosition = item
    return bestPosition
