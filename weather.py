#!/usr/bin/python
__author__ = 'mattiasd'

import xml.etree.ElementTree as ET
import urllib


def getWeather():
    getWeatherUrl = "http://www.yr.no/place/Sweden/Stockholm/Stockholm/forecast.xml"
    r = urllib.urlopen(getWeatherUrl)
    tree = ET.parse(r)
    #print tree
    root = tree.getroot().tag
    #print root
    for timedata in tree.findall('./forecast/tabular/'):
        dayWeather = []
        weatherTimeData = timedata.attrib['from'].split('T')
        weatherTimeDataLast = timedata.attrib['to'].split('T')
        dayWeather.append(weatherTimeData[1] + " - " + weatherTimeDataLast[1])
        for weatherdata in timedata.getchildren():

            if weatherdata.attrib.has_key('name'):
                if weatherdata.tag == "symbol":
                    dayWeather.append ("General Forecast: " + weatherdata.attrib['name'])
                else:
                    dayWeather.append (weatherdata.tag + ": " + weatherdata.attrib['name'])
            elif weatherdata.tag == "temperature":
                dayWeather.append (weatherdata.tag + ": " + weatherdata.attrib['value'] + "C")
        return dayWeather

if __name__ == "__main__":
    weather = getWeather()

    i = 0
    while i < len(weather):
        print weather[i]
    i = i + 1