import datetime
import sys

TIMEZONE = '-07:00'


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
    t = str(ar[3]) + ':' + '00' + TIMEZONE
    dt = d + 'T' + t
    return dt


def validateDateTime(dtime):
    dt = dtime.split()
    h = dt[3].split(':')

    try:
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


if __name__ == '__main__':
    pass