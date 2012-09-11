import unittest
import os
import sys
import cPickle

sys.path.insert(0, os.path.abspath(".."))
import cal


import cPickle

from os import remove

FILENAME = '../credentials/start.txt'
CACHE_FILE = '../credentials/test_cache_file.txt'


def createCacheFile():
        outFile = open(CACHE_FILE, 'wb')
        start = (True, '2012-9-6T10:25:00-07:00','Test summary')
        endTime = 'End-time'
        cached = (start, endTime)
        cPickle.dump(cached, outFile)
        outFile.close()

def createStartFile(start):
    try:
        outFile = open(FILENAME, 'wb')
        start = (start, '2012-9-6T10:25:00-07:00', 'EXAMPLE SUMMARY')
        cPickle.dump(start, outFile)
        outFile.close()
    except IOError:
        pass

class GCalAuthTest(unittest.TestCase):

# 2012-9-6T10:25:00-07:00
    values = (((2012, 9, 5, 13, 30), '2012-9-5T13:30:00-07:00'),
                ((2012, 12, 6, 14, 20), '2012-12-6T14:20:00-07:00'),
                ((2012, 1, 1, 1, 00), '2012-1-1T1:0:00-07:00'),
                ((2012, 12, 31, 23, 59), '2012-12-31T23:59:00-07:00'),)

    def testR3339Time(self):
        for val in self.values:
            self.assertEqual(cal.getR3339time(*val[0]), val[1])


class CheckStartTest(unittest.TestCase):

    def tearDown(self):
        try:
            remove(FILENAME)
        except OSError:
            pass

    def testIsStart(self):
        createStartFile(True)
        self.assertTrue(cal.checkIfStart())

    def testIsNotStart(self):
        createStartFile(False)
        self.assertFalse(cal.checkIfStart())

    def testNoFileAndStart(self):
        '''
        User wants to start and no file has been created
        '''
        self.assertTrue(cal.checkIfStart(True))

    def testNoFileAndEnd(self):
        '''
        User wants to end and no file has been created
        '''
        self.assertEqual(cal.checkIfStart(False), False)


class CreateStartTest(unittest.TestCase):

    def testCreateStartEvent_1(self):
        '''
        Test to create an event if a previous start event isn't already in progress
        '''
        self.assertTrue(True)


class CreateEndEventTest(unittest.TestCase):


    def tearDown(self):
        try:
            remove(CACHE_FILE)
        except OSError:
            pass
        try:
            remove(FILENAME)
        except OSError:
            pass

    def testWhatever(self):
        createCacheFile()
        self.assertTrue(True)

    def testNoEventStarted(self):
        createStartFile(False)
        self.assertEqual(None, cal.createEndEvent())
        inFile = open(FILENAME, 'rb')
        start = cPickle.load(inFile)
        # file should still be false
        self.assertFalse(start[0])

    def testEventStartedWithConnection(self):
        createStartFile(True)
        ()

        cal.createEndEvent()
        inFile = open(FILENAME, 'rb')
        start = cPickle.load(inFile)
        self.assertEqual(False, start[0])

    def testEventStartedWithoutConnection(self):
        pass
        #not sure how to do this yet
        # need to disable internet some how

def runTests():
    unittest.main()

unittest.main()
