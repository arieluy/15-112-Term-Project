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


sequence = ''
for m in msg:
    sequence += str(m) + '\n'
    sequence += 'time.sleep(%d)' % sleepTime


