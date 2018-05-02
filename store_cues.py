# from 112 course notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)


'''store = [0x91, 3, 127] # runs the 'store' command on grandMA2

def storeCue(data):
    data.midiout.send_message(store)'''

def writeCue(msg):
    file = ''
    # sleepTime = raw_input('Time: ')
    sleepTime = 2
    for m in msg:
        file += '\tdata.midiout.send_message(' + str(m) + ')\n'
    file += '\ttime.sleep(%d) \n' % sleepTime
    return file

def writeSequence(lst):
    sequence = 'import time\ndef playSequence(data):\n'
    for l in lst:
        sequence += l
    writeFile('MySequence1.py', sequence)

