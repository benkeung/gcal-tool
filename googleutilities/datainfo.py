import argparse
import cPickle
import os
import helpers
from pylab import *


EVENT_DATA = os.path.join(os.path.dirname(__file__),
    'credentials/eventdata.txt')


def loadSaveData():
    info = None
    try:
        inFile = open(EVENT_DATA, 'rb')
        try:
            info = cPickle.load(inFile)

        finally:
            inFile.close()
    except IOError, e:
        print 'loadSaveData, %s' % e
    return info


def printEventHistory():
    events = loadSaveData()

    for k, value in sorted(events.iteritems()):
        print k
        for v in value:
            print v[2],  helpers.diffBetweenTimes(v[0], v[1])


def timePerTitle():
    events = loadSaveData()
    info = []

    for k, value in sorted(events.iteritems()):
        time = 0

        for v in value:
            time += helpers.diffBetweenTimes(v[0], v[1])

        info.append((k, time))

    return info


def pieChartTitle():
    figure(1, figsize=(6, 6))
    info = timePerTitle()

    labels = [x[0] for x in info]
    fracs = [x[1] for x in info]
    print fracs

    pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    title('Time Spent on: ', bbox={'facecolor': '0.8', 'pad': 5})

    show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    pass
