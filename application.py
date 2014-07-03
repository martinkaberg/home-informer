#!/usr/bin/python
__author__ = 'mattiasd'
from flask import Flask, redirect, render_template, Response, request
from weather import getWeather
from trains import checkTrains
from gcalendar import googleCal
import datetime
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data

app = Flask(__name__)
#from app import views
app.debug = True
myCal = googleCal('LOGIN NAME', 'XXXXXXXX')

@app.route('/')
def index():
    return render_template("index.html", title = 'Home', weather = getWeather(),  tripData = checkTrains(), myEvents = myCal.getEvents())


if __name__ == "__main__":
    app.debug == True
    app.run(host='10.1.24.19', port=8080)
