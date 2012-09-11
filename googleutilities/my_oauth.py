import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

# different google tool ids
CALID = "k4lb250s87sc3ugvsi0uvjji54@group.calendar.google.com"
TASK_ID = ''

# oauth credentials
CLIENT_ID = '''232456248451-ckqsj6jm08ampdrg7o06dppkgtganmj9.apps.googleusercontent.com'''
CLIENT_SECRET = 'v2AXx9_0XPuBeAaZd7wdIY7e'
USER_AGENT = 'Benk/V1'
DEVELOPER_KEY = 'AIzaSyCn75d6AaMgNOKo0vkrmPc2lxjXVyLdq1w'


def getCalOauth():
    return auth('https://www.googleapis.com/auth/calendar',
        'calendar',
        'v3',
        'credentials/calendar.dat')


def auth(scope, serviceName, version, storage):
    FLOW = OAuth2WebServerFlow(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=scope,
    user_agent=USER_AGENT)

    storage = Storage(storage)
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)
    try:
        service = build(serviceName=serviceName, version=version, http=http,
            developerKey=DEVELOPER_KEY)
        return service, True
    except httplib2.ServerNotFoundError:
        return None, False
