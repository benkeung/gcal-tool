'''
TEMPLATE for cmd line:

python quick_event_cal.py -b '2012-mm-dd-hh-mm' -e '2012-mm-dd-hh-mm' -s 'summary' -l 'location'

python quick_event_cal.py -b '2012-09-12-17-30' -e '2012-09-12-19-00' -s 'Telus employer info sessoin' -l 'WESB100'

'''

import gflags
import argparse

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

event_calid = 'pa09pe94jvf7fqit34ljud9ago@group.calendar.google.com'

def authGCal():
	global service
	FLAGS = gflags.FLAGS

	FLOW = OAuth2WebServerFlow(
	    client_id='232456248451-ckqsj6jm08ampdrg7o06dppkgtganmj9.apps.googleusercontent.com',
	    client_secret='v2AXx9_0XPuBeAaZd7wdIY7e',
	    scope='https://www.googleapis.com/auth/calendar',
	    user_agent='Benk/V1')

	storage = Storage('calendar.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid == True:
	  credentials = run(FLOW, storage)

	http = httplib2.Http()
	http = credentials.authorize(http)

	service = build(serviceName='calendar', version='v3', http=http,
	       developerKey='AIzaSyCn75d6AaMgNOKo0vkrmPc2lxjXVyLdq1w')

def createEvent(start, end, summary, location):

	start1 = getRCF(start)
	end1 = getRCF(end)

	print start1
	event = {
	 "end": {
	  "dateTime": end1
	 },
	 "start": {
	  "dateTime": start1
	 },
	 "summary": summary,
	 "location": location
	}

	# print event

	created_event = service.events().insert(calendarId=event_calid, body=event).execute()

def getRCF(time):
	time = time.split('-')
	RCF_date = str(time[0]) + '-' + str(time[1]) + '-' + str(time[2])
	RCF_time = str(time[3]) + ':' + str(time[4]) + ':' + '00-07:00'

	return RCF_date + 'T' + RCF_time

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', '--begin', help='The start date formatted as yyyy-mm-dd-hh-mm')
	parser.add_argument('-e', '--end', help='The end date formatted as yyyy-mm-dd-hh-mm')
	parser.add_argument('-s', '--summary', help='The summary name of the event',type=str)
	parser.add_argument('-l', '--location', help='The location of the event', default="N/A")
	args = parser.parse_args()
	if args.begin and args.end and args.summary:
		authGCal()
		createEvent(args.begin,args.end,args.summary,args.location)
		print 'Event created!'
	else:
		print ''''
				HOW TO USE:
				'-b', '--begin', help='The start date formatted as yyyy-mm-dd-hh-mm'
				'-e', '--end', help='The end date formatted as yyyy-mm-dd-hh-mm'
				'-s', '--summary', help='The summary name of the event'
				'-l', '--location', help='The location of the event'
	'''