#!/usr/bin/env python
import datetime
import time
import urllib2
import urllib
import httplib
import csv
import boto3
import os
import json
import sys

pvo_host= "pvoutput.org"
pvo_key = os.environ['pvo_key']
pvo_systemid = os.environ['pvo_systemid']
pvo_statusInterval = 5
tzOffset = float(os.environ['tzOffset'])

sgDeviceId = os.environ['sgDeviceId']
apiDelay = 1 # time to delay after API calls

class Connection():
    def __init__(self, api_key, system_id, host):
        self.host = host
        self.api_key = api_key
        self.system_id = system_id

    def get_status(self, date=None, time=None):
        """
        Retrieves status information
        Return example:
          20101107,18:30,12936,202,NaN,NaN,5.280,15.3,240.1
        """
        path = '/service/r2/getstatus.jsp'
        params = {}
        if date:
            params['d'] = date
        if time:
            params['t'] = time
        params = urllib.urlencode(params)

        response = self.make_request("GET", path, params)

        if response.status == 400:
            # Initialise a "No status found"
            return "%s,00:00,,,,,,," % datetime.datetime.now().strftime('%Y%m%d')
        if response.status != 200:
            raise StandardError(response.read())

        return response.read()

    def add_output(self, date, comment):
        """
        Update PVOutput with Herculis' own status message.
        """
        path = '/service/r2/addoutput.jsp'
        params = {
                 'd': date
        }
        params['cm'] = comment
        params = urllib.urlencode(params)

        response = self.make_request('POST', path, params)

        if response.status == 400:
            raise ValueError(response.read())
        if response.status != 200:
            raise StandardError(response.read())       
        
    def add_status(self, date, time, energy_exp=None, power_exp=None, energy_imp=None, power_imp=None, temp=None, vdc=None, cumulative=False):
        """
        Uploads live output data
        """
        path = '/service/r2/addstatus.jsp'
        params = {
                'd': date,
                't': time
                }
        if energy_exp:
            params['v1'] = energy_exp
        if power_exp:
            params['v2'] = power_exp
        if energy_imp:
            params['v3'] = energy_imp
        if power_imp:
            params['v4'] = power_imp
        if temp:
            params['v5'] = temp
        if vdc:
            params['v6'] = vdc
        if cumulative:
            params['c1'] = 1
        params = urllib.urlencode(params)

        response = self.make_request('POST', path, params)

        if response.status == 400:
            raise ValueError(response.read())
        if response.status != 200:
            raise StandardError(response.read())
    
    def make_request(self, method, path, params=None):
        conn = httplib.HTTPConnection(self.host)
        headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain',
                'X-Pvoutput-Apikey': self.api_key,
                'X-Pvoutput-SystemId': self.system_id
                }
        conn.request(method, path, params, headers)

        return conn.getresponse()

def getSungrowData(start=time.strftime("%Y%m%d")):
    """
    Download Solar report for the day
    """
    response = urllib2.urlopen('http://www.solarinfobank.com/DataDownLoad/DownLoadRundata?deviceId='+sgDeviceId+'&yyyyMMDD='+start+'&type=csv')
    cr = csv.reader(response)
    return cr
    
def lambda_handler(event, context):
    now = datetime.datetime.now() + datetime.timedelta(hours=tzOffset)
    pvoutz = Connection(pvo_key, pvo_systemid, pvo_host)
    PVOStatus = pvoutz.get_status()
    date = PVOStatus.split(",")[0]
    timez = PVOStatus.split(",")[1]
    datez = datetime.datetime.strptime(date + " " + timez, "%Y%m%d %H:%M")
    datez += datetime.timedelta(minutes=5)
    if datez.date() < now.date():
        date = datetime.datetime.strftime(now, "%Y%m%d")
        timez = "00:00"
    else:
        date = datetime.datetime.strftime(datez, "%Y%m%d")
        timez = datetime.datetime.strftime(datez, "%H:%M")
    print "Loading %s %s" % (date, timez)
    sOut = getSungrowData(date)
    count = 0
    model = ""
    for row in sOut:
        count += 1
        if count == 1:
            if "SH5K" in row[0]:
                model = "SH5K"
            else:
                model = "SG5KTL"
        if count < 3:
            continue
        if row[0] > timez:
            if row[1] == "":
                continue
            powerTime = datetime.datetime.strptime(row[0], '%H:%M:%S')
            powerTime = datetime.datetime.strftime(powerTime, '%H:%M')
            if model == "SH5K":
                powerOut = row[7]
                consumption = row[18]
                temp = row[11]
                voltage1 = float(row[1])
                voltage2 = float(row[4])
            else:
                powerOut = float(row[11])*1000
                consumption = float(row[1])*1000
                temp = row[3]
                voltage1 = float(row[4])
                voltage2 = float(row[6])
            vdc = (voltage1 + voltage2)/2
            print "Time: " + str(powerTime) + " KW: " + str(powerOut) + " Load: " + str(consumption) + " Temp: " + str(temp) + " VDC: " + str(vdc)
            pvoutz.add_status(date, powerTime, power_exp=powerOut, power_imp=consumption, temp=temp, vdc=str(vdc))
            time.sleep(apiDelay)
    now_fmt = datetime.datetime.strftime(now, '%H:%M')
    pvoutz.add_output(date, "Monitored by Herculis at %s" % now_fmt)
