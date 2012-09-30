import cPickle
import argparse
import os
import helpers

from my_oauth import CALID
from my_oauth import getCalOauth
from datetime import datetime


SERVICE = None
IS_CONNECTION = True

FILENAME = os.path.join(os.path.dirname(__file__), 'credentials/start.txt')
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'credentials/cache.txt')
DATA = os.path.join(os.path.dirname(__file__), 'credentials/calendar.dat')
EVENT_DATA = os.path.join(os.path.dirname(__file__),
    'credentials/eventdata.txt')


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
        try:
            start = cPickle.load(inFile)
        finally:
            inFile.close()
        return start[0]
    except IOError:
        try:
            outFile = open(FILENAME, 'wb')
            try:
                start = (isStart, getCurrentTime(), summary)
                cPickle.dump(start, outFile)
            finally:
                outFile.close()

            if not isStart:
                print '''Need to first \'start\' an event before \'ending\' one.
                    Use the -s [Summary] flag to \'start\' and event'''
                return isStart

            return isStart
        except IOError:
            print '''IOError: Could not find any previous data and could not
                initialize one (pickle).'''


def createStartEvent(summary='Did not specify a summary', title=None):
    if checkIfStart(True):
        try:
            inFile = open(FILENAME, 'rb')
            try:
                start = cPickle.load(inFile)
                print 'An event is already in progress. %s started at %s.)' \
                    % (start[2], start[1])
                return
            finally:
                inFile.close()
        except:
            print '''An event has already been created. Cannot retrieve previous
                information.'''

    else:
        # if the event has not been started, want to save the current time and
        # argument passed
        if not title:
            if not helpers.promptYesOrNo(question="No title was specified? " \
                "Are you sure you want to proceed?"):
                print 'Quitting..'
                return

        try:
            outFile = open(FILENAME, 'wb')
            try:
                start = (True, getCurrentTime(), summary, title)
                cPickle.dump(start, outFile)
                print 'Starting event, \'%s\', at %s' % (start[1], start[2])
            finally:
                outFile.close()
        except IOError:
            print 'Problem saving start time information'


def createEndEvent():
    if not checkIfStart(False):
        print 'Need to start an event before you can end one'

    else:
        authGCal()

        try:
            inFile = open(FILENAME, 'rb')
            start = cPickle.load(inFile)
        except IOError:
            print 'Error loading start summary information'
        finally:
            inFile.close()

        # use the start info and getCurrentTime() to save the data of event
        saveEventData(start, getCurrentTime())

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
            print '''No internet acces. Caching your event end time. Information
                will be updated to GCal when you next submit an event with
                internet access.'''
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


def createEventInterface():
    '''
    Initilizes a command prompt interface to create a new event. Includes:
    - start time
    - end time
    - title (opt)
    - location (opt)
    - details (opt)
    '''

    check = True
    if helpers.promptYesOrNo("Are you sure you want to create a new event?"):
        try:
            while check:
                st = helpers.promptQuestion("Input start time (Q to quit): ")
                if st and helpers.validateDateTime(st):
                    check = False
                else:
                    print '%s is not a valid date time' % st
            check = True

            while check:
                et = helpers.promptQuestion('Input end time (Q to quit): ')
                if et and helpers.validateDateTime(et):
                    check = False
                else:
                    print '%s is not a valid date time' % et

            check = True

            title = helpers.promptQuestion('Input event title (Optional, leave '
                'blank. Q to quit): ')
            loc = helpers.promptQuestion('Input location (Optional, leave '
                'blank. Q to quit): ')
            desc = helpers.promptQuestion('Input description: (Optional, leave '
                'blank. Q to quit): ')

        except helpers.QuitException:
            print 'Quitting creating event.'
            return

        st = helpers.formatDateTime(st)
        et = helpers.formatDateTime(et)

        tup = (st, et, title, loc, desc)
        return tup
    else:
        print 'Cancelling creating an event'
        return None


def createEvent():
    details = createEventInterface()
    if details:
        authGCal()
        event = {
            "end": {
                "dateTime": str(details[1])
            },
            "start": {
                "dateTime": str(details[0])
            },
            "summary": str(details[2]),
            "location": str(details[3]),
            "description": str(details[4])
            }

        SERVICE.events().insert(calendarId='primary', body=event).execute()


def getStatus():
    try:
        inFile = open(FILENAME, 'rb')
        try:
            start = cPickle.load(inFile)
            if start[0]:
                print 'An event \'%s\' started at % s is already in progress' \
                    % (start[1], start[2])
                return True
            else:
                print 'No event is in progress.'
                return False
        except IndexError, e:
            'IndexError: %s' % e
        finally:
            inFile.close()
    except IOError, e:
        print 'IOError: %s' % e


def cancelEvent():

    if not checkIfStart():
        print 'No event to cancel'

    else:
        try:
            inFile = open(FILENAME, 'rb')
            try:
                start = cPickle.load(inFile)
                event = start[2]
            finally:
                inFile.close()

            if helpers.promptYesOrNo('Are you sure you want to cancel %s'
                % event):

                outFile = open(FILENAME, 'wb')
                start = (False,)

                try:
                    cPickle.dump(start, outFile)
                    print '%s cancelled' % event
                finally:
                    outFile.close()

        except IOError, e:
            print 'IOError: %s' % e
        except IndexError, e:
            print 'Index Error: %s' % e


def saveEventData(start, stop):
    '''
    pickle it as a dictionary?
    ie. data['CPSC320'] = (('start', 'end', 'summary'))
    '''
    try:
        inFile = open(EVENT_DATA, 'rb')
        try:
            data = cPickle.load(inFile)
        finally:
            inFile.close()

    except IOError:
        try:
            outFile = open(EVENT_DATA, 'wb')
            data = dict()

        finally:
            outFile.close()

    toSave = (start[1], stop, start[2])
    title = start[3]

    print title
    print toSave


    if title in data:
        if data[title]:
            temp = data[title]
            temp.append(toSave)
            data[title] = temp
        else:
            data[title] = [toSave]

    else:
        data[title] = [toSave]

    try:
        outFile = open(EVENT_DATA, 'wb')
        try:
            cPickle.dump(data, outFile)
        finally:
            outFile.close()
    except IOError:
        print 'saveEventData IOError.'


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', help='''Use this to initialize the
        starting of an event; the argument should be the summary of event''', \
        type=str)
    parser.add_argument('-e', '--end', help='''Use to end
        an event and create a GCal event using this end time, and start time and
        information''', nargs='?', const=True)
    parser.add_argument('-i', '--info', action='store_true', \
        help='Returns information about a started event if there is one')
    parser.add_argument('-c', '--cancel', action='store_true', \
        help='Cancels event if it needs to be cancelled')
    parser.add_argument('-q', '--quickevent', action='store_true', \
        help='Goes through an interface to create a new event')
    parser.add_argument('-t', '--title', help='The header we store the event\
        as')

    args = parser.parse_args()

    if args.info:
        getStatus()
    elif args.quickevent:
        createEvent()
    elif args.cancel:
        cancelEvent()
    elif args.end:
        createEndEvent()
    elif args.start:
        if args.title:
            createStartEvent(args.start, title=args.title)
        else:
            createStartEvent(args.start)
    elif not args.end and not args.start:
        parser.print_help()
