#!/usr/bin/python
# __author__ = 'mattiasd'

import requests
import xml.etree.ElementTree as ET
import datetime

api_key = "83952b3d97ea56a4d05f02b5b5649b17"
base_url = ""

def getStationNumber(stationName):
    api_key_real = "a18f31474637e3bf12325edec65dd108"
    getStationUrl = "https://api.trafiklab.se/sl/realtid/GetSite.json?stationSearch="
    completeUrl = getStationUrl + stationName + "&key=%s" % api_key_real
    response = requests.get(completeUrl)
    if response.status_code == requests.codes.ok:
        stationData = response.json()
        stationNum = stationData['Hafas']['Sites']['Site']['Number']
        stationName = stationData['Hafas']['Sites']['Site']['Name']
    else:
        print "Error submitting request."
        print "could not find station number for: " +stationName
        return False
    return stationNum

def getTrip(fromStation, toStation, leaveTime):
    api_key="83952b3d97ea56a4d05f02b5b5649b17"
    base_url = "https://api.trafiklab.se/sl/reseplanerare.xml?key=%s" % api_key
    #fromStationNum = getStationNumber(fromStation)
    #toStationNum = getStationNumber(toStation)
    completeUrl = base_url + "&S=%s&Z=%s&time=%s" % (fromStation, toStation, leaveTime)
#    print "FULL REQUEST: " + completeUrl
    response = requests.get(completeUrl)
    tripData = response.text
#    print "TRIP DATA: " + tripData
    return tripData

def parseTripData(tripData):
    root = ET.fromstring(tripData.encode('utf-8'))
    finalTrip = []
#    print "PARSINGS NOW-------"
    try:
        #finalTrip.append("#######################")
        finalTrip.append("From: " + str(root[4][1][0].text))
        finalTrip.append("To: " + str(root[4][1][1].text))
        #finalTrip.append("---------------------------------")
        finalTrip.append("Departure time: " + str(root[4][1][3].text))
        finalTrip.append("Arrival time: " + str(root[4][1][5].text))
        #finalTrip.append("---------------------------------")
        finalTrip.append("Travel: " + root[4][1][6][1].text + " towards " + root[4][1][6][3].text)
        #finalTrip.append("#######################")
    except Exception as e:
        finalTrip.append("Search failed. " + e.message)

    return finalTrip

def checkTrains():
    curTime = datetime.datetime.now().time()
    newMinute = curTime.minute + 10
    parsedTime = str(curTime.hour) + ":" + str(newMinute)
    print "TIME: " + parsedTime
    try:
        unparsedTripData = getTrip('svedmyra', 'gullmarsplan', parsedTime )
        tripInfo = parseTripData(unparsedTripData)
    except Exception as e:
        tripInfo = e.message
    return tripInfo


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SL Trip finder help")
    parser.add_argument("--start", help="From station")
    parser.add_argument("--to", help="To station")
    parser.add_argument("--time", help="Time of departure")

    args = parser.parse_args()

    if args.start and args.to and args.time:
        fromStation = args.start.strip()
        toStation = args.to.strip()
        departureTime = args.time.strip()
        unparsedTripData = getTrip(fromStation, toStation, departureTime)
        finalTrip = parseTripData(unparsedTripData)
        print "######### TRIP INFO #############################################"
        count = 0
        while count < len(finalTrip):
            print finalTrip[count]
            count = count + 1
        print "#################################################################"
    else:
        print "Incorrect arguments given"

