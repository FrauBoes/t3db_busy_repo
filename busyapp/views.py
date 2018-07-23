from django.shortcuts import render
from django.http import HttpResponse
import requests
import os

from .forms import OnTheGoForm, PlannerForm, TouristForm
from .ml import predictor_svm
from .ml import predictor_regression
from .ml import predictor_ann
from .ml import predictor_ann_improved
from .ml import getWeather
from .ml import getNormalizedDayOfYear
from .ml import secondsSinceMidnight
from .ml import getWeekDayBinaryArray
from .ml import getNormalizedWeather
from .ml import secondsNormalizedSinceMidnight

from busy.settings import STATIC_ROOT

import random
import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')


def onthego(request):
    return render(request, 'onthego.html')


def theplanner(request):
    return render(request, 'theplanner.html')


def tourist(request):
    return render(request, 'tourist.html')

def busStops(request):
    r = requests.get("https://data.dublinked.ie/cgi-bin/rtpi/busstopinformation?format=json&operator=bac")
    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text)

    #if the above API fails, try another...
    r = requests.get("https://data.smartdublin.ie/cgi-bin/rtpi/busstopinformation?format=json&operator=bac")
    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text)
    else: #If all APIs fail, use local file
        with open(STATIC_ROOT+'/bus_data/busstopinformation.json', 'r', encoding="utf8") as file:
            return HttpResponse(file.read())

#function to return Google Directions API query results for the map
def directions(request):
    params = request.GET;
    r = requests.get("https://maps.googleapis.com/maps/api/directions/json",
                     params={'origin': params['origin'],
                             'destination': params['destination'],
                             'mode': params['mode'],
                             'transit_mode': params['transit_mode'],
                             'key': os.environ.get('directionsAPI')})
    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text)

#function to return RTPI query results for Bus Stop Autosuggests
def busStopAutosuggest(request):
    params = request.GET;
    r = requests.get("https://data.dublinked.ie/cgi-bin/rtpi/busstopinformation",
                     params={'format': params['format'],
                             'operator': params['operator'],
                             'stopname': params['stopname']})
    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text)
    else:
        return HttpResponse("format=" + params['format']+ ", operator=" + params['operator']+ ", stopname=" + params['stopname'])

#function to return RTPI query results for Bus Routes Autosuggests
def busRoutesAutosuggest(request):
    params = request.GET;
    r = requests.get("https://data.dublinked.ie/cgi-bin/rtpi/routelistinformation",
                     params={'format': params['format'],
                             'operator': params['operator']})
    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text)
    else:
        return HttpResponse("format=" + params['format']+ ", operator=" + params['operator'])
    
#Function for RTPI querying for Route Number Autosuggests.
def routeNumberAutosuggest(request):
    r = requests.get("https://data.dublinked.ie/cgi-bin/rtpi/routelistinformation")
    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text)

def loadTest(request):
    with open(STATIC_ROOT+'/load_testing/loaderio-e39f002a9fff5739d5e13b22d4f09b69.txt', 'r', encoding="utf8") as file:
        return HttpResponse(file.read())

def testView(request):
    #r = request.GET;
    #return render(request, 'testpage.html', {'msg1' : r['t']})
    return render(request, 'testpage.html')


def personas(request):
    return render(request, "personas.html")

def onthegoform(request):
    if request.method == 'GET':
        form = OnTheGoForm(request.GET)

        #Example of reading unvalidated form data. This may crash the app.
        #print(form['busnum'].value())
        #print(form.data['busnum'])

        #Prefered way of handling forms, validate first before using.
        if form.is_valid():
            busNum = form.cleaned_data['busnum_var']
            fromVar = form.cleaned_data['from_var']
            toVar = form.cleaned_data['to_var']
            busDirect = form.cleaned_data['bus_direction']

            #normalize the input data
            busNum = busNum

            time_of_day = secondsNormalizedSinceMidnight()
            weather = getNormalizedWeather()
            dayOfYear = getNormalizedDayOfYear()
            weekDay = getWeekDayBinaryArray()

            # call the machine learning function & parse the returned seconds into hours, minutes & seconds.
            journeyTimeSeconds = predictor_ann_improved(busNum=busNum,
                                                        busDirection=busDirect,
                                                        start_stop=fromVar,
                                                        end_stop=toVar,
                                                        time_of_day=time_of_day,
                                                        weatherCode=weather,
                                                        secondary_school=0,
                                                        primary_school=0,
                                                        trinity=0,
                                                        ucd=0,
                                                        bank_holiday=0,
                                                        event=0,
                                                        day_of_year=dayOfYear,
                                                        weekday=weekDay)

            journeyTime = {'h': 0, 'm': 0, 's': 0}
            journeyTime['m'], journeyTime['s'] = divmod(journeyTimeSeconds, 60)
            journeyTime['h'], journeyTime['m'] = divmod(journeyTime['m'], 60)
            journeyTime['s'] = round(journeyTime['s']) #get rid of trailing floating point for seconds.

            # some random numbers for TESTING
            cost = 2.85 #TESTING for now...
            bestStartTime = datetime.datetime.now() + datetime.timedelta(minutes=60) #note 1h addition for linux servers

            # server side rendering - replace with AJAX for client side rendering in the future
            return render(request, 'onthego.html', {'busNum' : busNum,
                                                    'from': fromVar,
                                                    'to': toVar,
                                                    'journeyTime' : journeyTime,
                                                    'cost' : cost,
                                                    'bestStartTime' : bestStartTime})
        else:
            return HttpResponse("Oops! Form invalid :/ Try again?")


def plannerform(request):
    if request.method == 'GET':
        form = PlannerForm(request.GET)

        # Example of reading unvalidated form data. This may crash the app.
        print(form['busnum_var'].value())
        print(form.data['busnum_var'])

        #Prefered way of handling forms, validate first before using.
        if form.is_valid():
            busVar = form.cleaned_data['busnum_var']
            fromVar = form.cleaned_data['from_var']
            toVar = form.cleaned_data['to_var']
            busDirect = form.cleaned_data['bus_direction']
            timeVar = form.cleaned_data['time']
            dateVar = form.cleaned_data['date']

            return HttpResponse("Bus Num: "+busVar+"<br>"+"From: "+fromVar+"<br>"+"To: "+toVar+"<br>"+"Direction: "+busDirect+"<br>"+"Time: "+timeVar+"<br>"+"Date: "+dateVar) #FOR DEBUGGING
        else:
            return HttpResponse("Oops! Form invalid :/ Try again?")


def touristform(request):
    if request.method == 'GET':
        form = TouristForm(request.GET)

        #Example of reading unvalidated form data. This may crash the app.
        #print(form['busnum'].value())
        #print(form.data['busnum'])

        #Prefered way of handling forms, validate first before using.
        if form.is_valid():
            busVar = form.cleaned_data['busnum_var']
            fromVar = form.cleaned_data['from_var']
            toVar = form.cleaned_data['to_var']
            whenVar = form.cleaned_data['when_var']

            return HttpResponse("Bus Num: "+busVar+"<br>"+"From: "+fromVar+"<br>"+"To: "+toVar+"<br>"+"When: "+whenVar) #FOR DEBUGGING
        else:
            return HttpResponse("Oops! Form invalid :/ Try again?")