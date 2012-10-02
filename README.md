This is a command line utility that aims to help add and manage events/tasks to a user's Google account.It is written in Python and uses the Google API Client Library.

A notable feature of this utility is that a user is able to record and track their activities through Google Calendar. The user can initiate the starting and ending of an event using command line flags, which uses the datetimes when tool was called. The utility will take the start and end times and create an event wtih the specified name

This is an ongoing project.

Other Features:
  - Add an event by specifying start and end time, event name, location and description
  - Add TASKS by specifying date and name
  - Track total hours spent on a specific event or by broad categories
  - Plot the distribution of time spent on an 'event category' using matplotlib