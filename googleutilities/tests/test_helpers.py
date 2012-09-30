import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import helpers


class MonthFormatter(unittest.TestCase):

    months = (('January', 1), ('February', 2), ('April', 4), ('December', 12),
                ('Jan', 1), ('Febru', 2), ('MArCH', 3), ('Ovember', 11),
                ('may', 5))

    def testMonth(self):
        for month in self.months:
            self.assertEqual(month[1], helpers.convertMonth(month[0]))


class testFormatDateTime(unittest.TestCase):

    # 2012-9-6T10:25:00-07:00 is R3339

    date_time = (('1 January 2012 11:30', '2012-1-1T11:30:00-07:00'),
                ('12 March 1999 15:30', '1999-3-12T15:30:00-07:00'),
                ('30 Dec 2001 18:45', '2001-12-30T18:45:00-07:00'),
                ('31 Decem 2012 13:30', '2012-12-31T13:30:00-07:00'),
                ('28 February 2011 23:59', '2011-2-28T23:59:00-07:00'),
                ('1 Jan 2001 00:00', '2001-1-1T00:00:00-07:00'))

    bad_date_time = (('32 Jan 2012 23:30'), ('30 Feb 2012 10:30'),
            ('31 April 2012 11:30'), ('10 April 2012 24:00'),
            ('24 April 2012 10:60'), ('25 Dec 2000 10:90'),
            ('10 NtReal 2011 10:30'))

    good_minute = (0, 1, 2, 30, 58, 59)

    bad_minute = (-1, 60, 61, 100, 999)

    def testFormatDateTime(self):
        for value in self.date_time:
            self.assertEqual(value[1], helpers.formatDateTime(value[0]))

    def testValidateTime(self):
        for minute in self.good_minute:
            self.assertEqual(None, helpers.validateMinute(minute))

    def testValidateTimeException(self):
        for minute in self.bad_minute:
            self.assertRaises(helpers.MinuteException, helpers.validateMinute,
            minute)

    def testValidateDateTime(self):
        for dt in self.date_time:
            self.assertTrue(helpers.validateDateTime(dt[0]))

    def testValidateDateTimeException(self):
        for dt in self.bad_date_time:
            self.assertFalse(helpers.validateDateTime(dt))


class testDiffBetweenMonths(unittest.TestCase):

    dates = ((('2012-9-6T10:25:00-07:00', '2012-9-6T10:50:00-07:00'), 25),
        (('2012-9-6T10:25:00-07:00', '2012-9-6T10:31:00-07:00'), 6),
        (('2012-9-6T10:25:00-07:00', '2012-9-6T16:10:00-07:00'), 345),
        (('2012-9-6T10:25:00-07:00', '2012-9-6T10:25:00-07:00'), 0),
        (('2012-9-6T00:00:00-07:00', '2012-9-6T23:59:00-07:00'), 1439),
        (('2012-9-6T20:25:00-07:00', '2012-9-7T02:00:00-07:00'), 335),
        (('2012-9-6T18:10:00-07:00', '2012-9-7T5:20:00-07:00'), 670),
        (('2012-9-6T18:10:00-07:00', '2012-9-8T5:20:00-07:00'), 2110),

        #this one is where t1 is a time after t2
        (('2012-9-6T16:10:00-07:00', '2012-9-6T10:25:00-07:00'), 345),
        )

    # 320 +
    def testDiffBetweenMonths(self):
        for d in self.dates:
            self.assertEqual(helpers.diffBetweenTimes(* d[0]), d[1])


unittest.main()
