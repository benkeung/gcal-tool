import httplib2
import mykeys
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


'''
NOTE:
Replace all instances of mykeys.** with your own Google API keys.
mykeys.py was not provided as it contained my Google credentials.

I'm using a separate mykeys.py file to store my credentials because I don't have
to continually remove my credentials when posting to github.
'''
CALID = mykeys.CALID
TASK_ID = ''
CLIENT_ID = mykeys.CLIENT_ID
CLIENT_SECRET = mykeys.CLIENT_SECRET
USER_AGENT = mykeys.USER_AGENT
DEVELOPER_KEY = mykeys.DEVELOPER_KEY

path = os.path.dirname(__file__) + '/credentials/'

def getCalOauth():
    return auth('https://www.googleapis.com/auth/calendar',
        'calendar',
        'v3',
        path + '/calendar.dat')


def getTaskOauth():
    return auth('https://www.googleapis.com/auth/tasks',
        'tasks', 'v1', path + 'tasks.dat')


def auth(scope, serviceName, version, storage):
    FLOW = OAuth2WebServerFlow(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=scope,
    user_agent=USER_AGENT)

    storage1 = Storage(storage)
    credentials = storage1.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage1)

    http = httplib2.Http()
    http = credentials.authorize(http)
    try:
        service = build(serviceName=serviceName, version=version, http=http,
            developerKey=DEVELOPER_KEY)
        return service, True
    except httplib2.ServerNotFoundError, e:
        print 'httplib2.ServerNotFoundError: %s' % e
        return None, False
