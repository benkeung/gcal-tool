import mykeys
import my_oauth
import helpers
import argparse

SERVICE = None
IS_CONNECTION = True


def authService():
    global SERVICE
    global IS_CONNECTION
    SERVICE, IS_CONNECTION = my_oauth.getTaskOauth()


def createTask(title, due, notes=""):

    authService()

    if not SERVICE:
        print 'Could not authenticate Tasks'

    else:
        if due:
            dd = helpers.formatDateTime(due)
            if not dd:
                print '%s is not a valid date' % due

            else:
                event = {
                    "title": title,
                    "due": dd,
                    "notes": notes
                    }
        else:
            event = {
                "title": title,
                "notes": notes
                }

        SERVICE.tasks().insert(tasklist=mykeys.TASK_ID, body=event).execute()

def getAllTasks():
    authService()

    if not SERVICE:
        print 'Could not authenticate Tasks'

    else:
        return SERVICE.tasks().list(tasklist=mykeys.TASK_ID).execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--due', help='The date for the task')
    parser.add_argument('-t', '--title', help='The title of the task')
    parser.add_argument('-n', '--notes', help='''Any additional notes for this
        task''')

    args = parser.parse_args()

    if args.title:
        if args.notes:
            createTask(args.title, args.due, notes=args.notes)
        else:
            createTask(title=args.title, due=args.due)
    else:
        parser.print_help()