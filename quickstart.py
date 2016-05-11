from __future__ import print_function
import httplib2
import os
from pprint import pprint
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import time
from time import strftime
from twilio.rest import TwilioRestClient
import clock #forTimeChecking

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.
        
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        
        Returns:
        Credentials, the obtained credential.
        """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    listOfReminderTimes = []
    listOfTitle = []
    listOfStarting = []
    listOfDescription = []
    listOfEnding = []
    counterOfEvents = 0
    listOfNumberEvents = []
    listOfHour = []
    go = True
    
    """Shows basic usage of the Google Calendar API.
        
        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('\nGETTING THE UPCOMING EVENTS\n')
    eventsResult = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = eventsResult.get('items', [])
                                         
	#Time right now
    if not events:
        print('No upcoming events found.')
    for event in events:
        '''Start time code'''
        start = event['start'].get('dateTime', event['start'].get('date','description'))
        syear = start[0:4]
        smonth = start[5:7]
        sday=start[8:10]
        shour=start[11:13]
        sminute=start[14:16]
		
        time = str(datetime.datetime.now())
        time = time[0:10]
        eventDate=syear+"-"+smonth+"-"+sday

        if shour:
            shour=int(shour)
        else:
            shour=12

        if sminute:
            sminute=sminute
        else:
            sminute=10

        am = True
        if shour > 12:
            shour = shour-12
            am = False
            shour = str(shour)
                                                                                                 
        '''End Time code'''
        am2=True
        end = event['end'].get('dateTime',event['end'].get('date'))
        eyear = end[0:4]
        emonth = end[5:7]
        eday=end[8:10]
        ehour=end[11:13]
        eminute=end[14:16]
        if ehour:
            ehour=int(ehour)
        else:
            ehour=11
            am2=False
        if eminute:
            eminute = eminute
        else:
            eminute = 59

        if ehour > 12:
            ehour = ehour-12
            am2 = False
            ehour = str(ehour)

        if (am2 ==True) or (am ==True):
            ToD = " AM"
        else:
            ToD = " PM"

        description = event.get('description')
        date = event['start'].get('date','description')
        title = event['summary']
        location = event.get('location')
        woop = start

        starting ="START: "+str(shour)+":"+str(sminute)+str(ToD)
        ending ="ENDS: "+str(ehour)+":"+str(eminute)+str(ToD)
        title="EVENT: "+title

        useHoursMinutes = False
        time = str(datetime.datetime.now())
        time = time[11:16]
        counterOfEvents = counterOfEvents + 1

        if event['reminders']['useDefault'] == False:
            minutesBeforeReminder = int(event['reminders']['overrides'][0]['minutes'])
            hoursReminder = int(shour)
            minutesReminder = int(sminute)
        else:
            minutesBeforeReminder = 30
            hoursReminder=int(shour)
            minutesReminder=int(sminute)

        if(minutesBeforeReminder >= 60):
            useHoursMinutes = True
            hoursBeforeReminder = minutesBeforeReminder / 60
            minutesBeforeReminder = (minutesBeforeReminder % 60)
        if(minutesBeforeReminder >= minutesReminder):
            minutesReminder = minutesReminder + 60
            hoursReminder = hoursReminder-1

        if(useHoursMinutes):
            useHoursMinutes = False
            minutesReminder = minutesReminder - minutesBeforeReminder
            hoursReminder = hoursReminder - hoursBeforeReminder
        else:
            minutesReminder = minutesReminder - minutesBeforeReminder

        if shour==12 and ToD==" AM":
            hoursReminder = 12
            minutesReminder = 0

        if(minutesReminder <= 10):
            if(ToD == " PM"):
                hoursReminder=hoursReminder
                if hoursReminder==0:
                    hoursReminder=12
                hoursReminder = abs(hoursReminder)
                timeToBeReminded = str(hoursReminder+12)+":0"+ str(minutesReminder)
            else:
                timeToBeReminded = str(hoursReminder)+":0"+ str(minutesReminder)
        else:
            if minutesReminder==60:
                minutesReminder=str(minutesReminder)
                minutesReminder="00"
            if(ToD == " PM"):
                hoursReminder=hoursReminder
                if hoursReminder==0:
                    hoursReminder=12
                hoursReminder=abs(hoursReminder)
                timeToBeReminded = str(hoursReminder+12)+":"+ str(minutesReminder)
            else:
                timeToBeReminded = str(hoursReminder)+":"+ str(minutesReminder)

		timeNew = str(datetime.datetime.now())
		
		if timeNew[11:13]=='00':
			timeDigits=12
			timeMin=int(timeNew[14:16])
		else:
			timeDigits = int(timeNew[11:13])
			timeMin = int(timeNew[14:16])

		append = True

#		if (timeDigits)abs(int(hoursReminder)-1) and str(eventDate)==str(time[0:10]):
#			append = False
#			print("FALSE")
#		else:
#			append = True
#			print("APPENDED")

        listOfReminderTimes.append(timeToBeReminded)
        listOfStarting.append(starting)
        listOfTitle.append(title)
        listOfDescription.append(description)
        listOfEnding.append(ending)

        '''Print code for testing'''
        print(starting)
        print(title)
        if description:
            description ="Description: " + description
            print(description)
                                                                                                                                                                                                                                                                                                                                                                             
        elif (str(event.get('description')) == "None"):
            description = "No Description Entered"
            print(description)
        if location:
            location ="Location: " + location
            print(location)
        print(ending)
                                                                                                                                                                                                                                                                                                                                                                                                         
        print(" ")

        print (minutesBeforeReminder)
        #print("Minutes to be reminded before Event", minutesBeforeReminder)
        print("calculated time ", timeToBeReminded + ToD)

        print ("the counterOfEvents ", counterOfEvents)
        listOfNumberEvents.append(counterOfEvents)
        print(" ")
    else:
        reminder = "\n\nNo Reminder"

    clock.alerter(listOfReminderTimes, listOfStarting, listOfTitle, listOfDescription,listOfEnding,counterOfEvents)

if __name__ == '__main__':
    main()