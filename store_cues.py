# from 112 course notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents) 


def writeCue(msg):
    file = ''
    sleepTime = 0.2
    for m in msg:
        file += '\tdata.midiout.send_message(' + str(m) + ')\n'
    file += '\ttime.sleep(%2f) \n' % sleepTime
    return file

def writeSequence(data):
    sequence = 'import time\ndef playSequence(data):\n'
    for l in data.sequence:
        sequence += l
    filename = 'sequences/MySequence%d.py' % data.nextSequence
    writeFile(filename, sequence)


