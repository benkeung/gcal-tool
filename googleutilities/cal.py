import cPickle
import argparse
import os

from my_oauth import CALID
from my_oauth import getCalOauth
from datetime import datetime


SERVICE = None
IS_CONNECTION = True

FILENAME =  os.path.join(os.path.dirname(__file__), 'credentials/start.txt')
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'credentials/cache.txt')
DATA = os.path.join(os.path.dirname(__file__), 'credentials/calendar.dat')

# Replace all these values with your own google credentials in string format.
# ie. CLIENT_SECRET = 'v2AXx9_0XPuBe8afJKadsj''
CALID = CALID #calendar id


def authGCal():
    global SERVICE
    global IS_CONNECTION
    SERVICE, IS_CONNECTION = getCalOauth()


def getCurrentTime():
    dt = datetime.now()
    return getR3339time(dt.year, dt.month, dt.day, dt.hour, dt.minute)


def getR3339time(year, month, day, hour, minute):
    '''
    Returns an R3339 formatted time, ie.     # 2012-9-6T10:25:00-07:00
    '''
    # set default to 0 sec and Pacific timezone
    TAIL = '00-07:00'

    date = str(year) + '-' + str(month) + '-' + str(day)
    time = str(hour) + ':' + str(minute) + ":" + TAIL

    return date + 'T' + time


def checkIfStart(isStart=False, summary='Did not specify'):
    '''
    Returns true if an event has been 'started'; false if not
    '''
    try:
        inFile = open(FILENAME, 'rb')
        start = cPickle.load(inFile)
        inFile.close()
        return start[0]
    except IOError:
        try:
            outFile = open(FILENAME, 'wb')
            start = (isStart, getCurrentTime(), summary)
            cPickle.dump(start, outFile)
            outFile.close()

            if not isStart:
                print 'Need to first \'start\' an event before \'ending\' one. Use the -s [Summary] flag to \'start\' and event'
                return isStart

            return isStart
        except IOError:
            print 'IOError: Could not find any previous data and could not initialize one (pickle).'


def createStartEvent(summary='Did not specify a summary'):
    if checkIfStart(True):
        try:
            inFile = open(FILENAME, 'rb')
            start = cPickle.load(inFile)
            inFile.close()
            print 'An event is already in progress. %s started at %s.)' % (start[2], start[1])
            return
        except:
            print 'An event has already been created. Cannot retrieve previous information.'
    else:
        # if the event has not been started, want to save the current time and # argument passed
        try:
            outFile = open(FILENAME, 'wb')
            start = (True, getCurrentTime(), summary)
            cPickle.dump(start, outFile)
            outFile.close()
            print 'Starting event, \'%s\', at %s' % (start[1], start[2])
        except IOError:
            print 'Problem saving start time information'


def createEndEvent():
    if not checkIfStart(False):
        # if there hasn;t been a start event initiated, terminate and
        # return a help message
        print 'Need to start an event before you can end one'
    
    else:
        # if the event has been started, create an event using the
        # information from the start event
        # authGCal()
        authGCal()

        try:
            inFile = open(FILENAME, 'rb')
            start = cPickle.load(inFile)
        except IOError:
            print 'Error loading start summary information'
        finally:
            inFile.close()

        if IS_CONNECTION:
            try:
                event = {
                "end": {
                    "dateTime": getCurrentTime()
                },
                "start": {
                    "dateTime": start[1]
                },
                "summary": start[2]
                }

                SERVICE.events().insert(calendarId=CALID, body=event).execute()

                start = (False,)
                outFile = open(FILENAME, 'wb')
                try:
                    cPickle.dump(start, outFile)
                finally:
                    outFile.close()
            except IOError:
                print 'IOError in creating event'


        # no internet connection, we we're going to add the event information 
        # to a pickle object
        else:
            print 'No internet acces. Caching your event end time. Information will be updated to GCal when you next submit an event with internet access.'
            toLoad = (start, getCurrentTime())

            try:
                inFile = open(CACHE_FILE, 'rb')
                try:
                    cached = cPickle.load(inFile)
                    cached.append(toLoad)  
                finally:
                    inFile.close()

                try:
                    outFile = open(CACHE_FILE, 'wb')
                    cPickle.dump(cached, outFile)
                finally:
                    outFile.close()      

            except IOError:
                # this should happen when CACHE_FILE does not exist
                try:
                    inFile = open(CACHE_FILE, 'wb')
                    cPickle.dump(toLoad, inFile)
                finally:
                    inFile.close()


def quickEventInterface():
    begin = raw_input('Start time, ie. "16 Aug 2012 16:30"')
    end = raw_input('End time, ie. "16 Aug 2012 16:30"')
    sumary = raw_input('Summary of event. Leave blank for none')
    location = raw_input('Location of event. Leave blank for none')




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', help='Use this to initialize the starting of an event; the argument should be the summary of event', type=str)
    parser.add_argument('-e', '--end',  action='store_true', help='''Use to end an event and create a GCal event using this end time, and start time and information''')

    args = parser.parse_args()

    if args.end:
        createEndEvent()
    elif args.start:
        createStartEvent(args.start)
    elif not args.end and not args.start:
        print 'Help\n -s [summary] to start an event\n-e to end an event.'
