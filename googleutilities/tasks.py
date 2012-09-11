import httplib2
import cPickle
import argparse
import mykeys #NOTE, this is only used to keep my google credentials private and make it easier to put up to github
import os

from datetime import datetime
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

SERVICE = None
IS_CONNECTION = True

TASK_ID = mykeys.CALID #calendar id
CLIENT_ID = mykeys.CLIENT_ID
CLIENT_SECRET = mykeys.CLIENT_SECRET
USER_AGENT = mykeys.USER_AGENT
DEVELOPER_KEY = mykeys.DEVELOPER_KEY


def authTask():
    global SERVICE
    global IS_CONNECTION

    FLOW = OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/tasks',
        user_agent=USER_AGENT)

    storage = Storage(DATA)
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    try:
        SERVICE = build(serviceName='tasks', version='v1', http=http,
               developerKey=DEVELOPER_KEY)
    except httplib2.ServerNotFoundError:
        IS_CONNECTION = False


if __name__ == '__main__'
