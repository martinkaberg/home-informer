#!/usr/bin/python
import gdata.service
import gdata.calendar
import gdata.calendar.service
from gdata.calendar.service import CalendarService
#from gdata.calendar.service import CalendarQuery

feedUrl = "https://www.google.com/calendar/feeds/dahlgrenm%40gmail.com/private-fea9eaeb73c2ee8b8e31ad62921222e9/basic"

myCal = gdata.calendar.service.CalendarService("test")
myQuery = gdata.calendar.service.CalendarService()

myQuery.CalendarQuery("2013-08-26T00:00:00")

myCal.setUserCredentials("dahlgrenm@gmail.com", "!H0rkaova81!")

feed = myCal.query(myQuery)
#print myCal.getTitle().getPlainText()
