import datetime
import re
import sys
import timeit


TIMEZONE = '-07:00'
NUMDAYSINMONTH = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
    9: 30, 10: 31, 11: 30, 12: 31}


class MonthException(Exception):
    pass


class MinuteException(Exception):
    pass


class DateException(Exception):
    pass


class QuitException(Exception):
    pass


def formatDateTime(datetime):
    '''
    datetime must be inputted exactly like the following example:
    12 March 2012 15:30

    and return it as R3339 format:
    2012-9-6T10:25:00-07:00

    Return None if the time is not valid
    '''
    ar = datetime.split()

    # validate month
    try:
        month = str(convertMonth(ar[1]))
    except MonthException:
        print '%s is not a valid month' % ar[1]
        return None

    d = str(ar[2]) + '-' + month + '-' + str(ar[0])

    if len(ar) == 3:
        return d + 'T00:00:00' + TIMEZONE
    else:
        t = str(ar[3]) + ':' + '00' + TIMEZONE
        dt = d + 'T' + t
        return dt


def validateDateTime(dtime):
    try:
        dt = dtime.split()
        h = dt[3].split(':')
        validateMinute(h[1])
        month = int(convertMonth(dt[1]))
        datetime.datetime(year=int(dt[2]), month=month, day=int(dt[0]),
        hour=int(h[0]))

        return True

    except MinuteException:
        print 'Invalid datetime: %s must be between 0 and 59 inclusive' % h[1]
        return False

    except MonthException:
        print 'Invalid datetime: %s is not a valid month' % dt[1]
        return False

    except ValueError, e:
        print 'Invalid datetime: %s' % e
        return False

    except IndexError:
        print 'Invalid datetime: %s is invalid' % dt
        return False


def validateMinute(minute):
    '''
    A simple check to make sure the minute is between 0 and 59 (inclusive)
    '''
    if int(minute) < 0 or int(minute) > 59:
        raise MinuteException('''%s must be an integer between and including 0
            and 59''')


def convertMonth(month):
    month_dict = {'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4,
                'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUGUST': 8, 'SEPTEMBER': 9,
                'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12}

    month_u = month.upper()
    keys = month_dict.keys()
    for i in keys:
        if month_u in i:
            return month_dict[i]

    raise MonthException("\'%s\' is not a valid month." % month)


def promptYesOrNo(question='Are you sure?'):

    choices = ' [Y/N]: '
    valid = {'y': True, 'yes': True, 'n': False, 'no': False}

    while True:
        sys.stdout.write(question + choices)
        choice = raw_input().lower()

        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write('Please return a yes or no.\n')


def promptQuestion(question):
    quit = ['q', 'quit']

    sys.stdout.write(question)
    ans = raw_input()

    if ans.lower() in quit:
        raise QuitException
    else:
        return ans

def diffBetweenTimes(time1, time2):
    # after splitting, time1 is [y, m, d, h, m, s, tz, 00]
    time1 = [re.split(r'[:-]', x) for x in time1.split('T')]
    time2 = [re.split(r'[:-]', x) for x in time2.split('T')]

    time1 = time1[0] + time1[1]
    time2 = time2[0] + time2[1]

    time1 = [int(x) for x in time1]
    time2 = [int(x) for x in time2]

    for i, v in enumerate(time1):
        if i < 5:
            if v > time2[i]:
                return diffBetweenTimes_aux(time2, time1)

    return diffBetweenTimes_aux(time1, time2)


def diffBetweenTimes_aux(time1, time2):
    '''
    Precondition:
        time1 is the earlier time; time2 is the later time
    '''
    sing_month = True
    sing_day = True
    mins = 0

    for i, v in enumerate(time1):
        if i == 1:
            if v == time2[1]:
                pass
                #TODO
        if i == 2 and v != time2[2]:
            mins += (1440 * (time2[2] - v -1))
            sing_day = False
        if i == 3:
            if sing_day:
                mins += (60 * (time2[3] - time1[3] - 1))
            else:
                mins += (60 * (24 - time1[3] - 1))
                mins += (60 * time2[3])
        if i == 4:
            if sing_day:
                mins += ((60 - time1[4]) + time2[4])
            else:
                mins += + (60 - time1[4])
                mins += time2[4]
    return abs(mins)

if __name__ == '__main__':
    pass