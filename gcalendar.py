from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import gdata.calendar

class googleCal:

    def __init__(self, email, password):
        self.cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
        self.cal_client.ClientLogin(email, password, self.cal_client.source)
        self.calendar_service = gdata.calendar.service.CalendarService()
        self.calendar_service.email = '<email adress>'
        self.calendar_service.password = '<password>'
        self.calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
        self.calendar_service.ProgrammaticLogin()

    def _PrintOwnCalendars(self):
        feed = self.cal_client.GetOwnCalendarsFeed()
        print 'Printing owncalendars: %s' % feed.title.text
        for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text)

    def _DateRangeQuery(self, start_date = '2013-08-25T00:00:00', end_date = '2013-08-27T00:00:00'):
        query = gdata.calendar.client.CalendarEventQuery(start_min=start_date, start_max=end_date)
        feed = self.cal_client.GetCalendarEventFeed(q=query)
        return feed

    def _ParseTheData(self, myEvents):
        eventObject = []
        tempObject = []
        root = ET.fromstring(str(myEvents))
        if len(root) > 1:
            for events in root.getchildren():
                for eventdata in events:
                    if eventdata.tag == '{http://www.w3.org/2005/Atom}title':
                        eventObject.append('Event Title: ' + eventdata.text)
                    if eventdata.tag == '{http://schemas.google.com/g/2005}when':
                        eventObject.append('Starts: ' + eventdata.attrib['startTime'])
                        eventObject.append('Ends: ' + eventdata.attrib['endTime'])
                    if eventdata.tag == '{http://www.w3.org/2005/Atom}link':
                        tempObject.append(eventdata.attrib['href'])

        else:
            eventObject.append('No events found for today!')
        print eventObject
        return eventObject

    def getEvents(self):
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        rawCalendarData = self._DateRangeQuery(yesterday, tomorrow)
        parsedCalendarData = self._ParseTheData(rawCalendarData)
        return parsedCalendarData

    def FullTextQuery(self, text_query = '2013-08-03'):
        print 'Full text query for events...'
        query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', text_query)
        feed = self.calendar_service.CalendarQuery(query)
        for i, an_event in enumerate(feed.entry):
            for a_when in an_event.when:
                print '---'
                print an_event.title.text, 'Number:', i, 'Event Time: '


