import cal
import argparse
import os

DIR_CREDENTIALS = 'credentials'

def createDir():
    '''
    Creates a directory to store the credential files if it doesn't exist
    '''
    if not os.path.exists(DIR_CREDENTIALS):
        os.makedirs(DIR_CREDENTIALS)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', help='Use this to initialize the starting of an event; the argument should be the summary of event', type=str)
    parser.add_argument('-e', '--end',  action='store_true', help='''Use to end an event and create a GCal event using this end time, and start time and information''')

    args = parser.parse_args()

    createDir()

    if args.end:
        cal.createEndEvent()
    elif args.start:
        cal.createStartEvent(args.start)
    elif not args.end and not args.start:
        print 'Help\n -s [summary] to start an event\n-e to end an event.'
