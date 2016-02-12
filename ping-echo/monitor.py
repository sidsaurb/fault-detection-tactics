#!/usr/bin/python

import threading
import urllib2
import os
import time
import smtplib
import datetime
from email.utils import COMMASPACE
from email.mime.text import MIMEText

timerInterval = 10.0
alarmLevel = 0;
alarmRaised = False

sender = 'ftpmassignmentiitk@gmail.com'
receivers = ["sidsaurb@iitk.ac.in"]

smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login("ftpmassignmentiitk@gmail.com", "iitk1234")

def sendPing():
        try:
		host = "google.com"
                response = os.system("ping -c 1 " + host + " > /dev/null")
		if response == 0:
                        print "Ping successful: Host reachable"
			sendOkEmail()
                else:
                        print "Ping failed: Host unreachable"
			raiseAlarm(time.time())
        except Exception as inst:
                print inst

        timer = threading.Timer(timerInterval, sendPing)
        timer.start()

def raiseAlarm(timestamp):
        global alarmLevel
        global alarmRaised
        if alarmLevel < 4:
                alarmLevel += 1
        alarmRaised = True
        failedOn = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
        message = MIMEText("Ping failed on " + failedOn)
        message['To'] = COMMASPACE.join(receivers)
        if alarmLevel == 1:
                message['Subject'] = "Server unreacheble: Alarm level 1"
                smtpObj.sendmail(sender, receivers, message.as_string())
        if alarmLevel == 2:
                message['Subject'] = "Server unreachable: Alarm level 2"
                smtpObj.sendmail(sender, receivers, message.as_string())
        if alarmLevel == 3:
                message['Subject'] = "Server unreachable: Alarm level 3"
                smtpObj.sendmail(sender, receivers, message.as_string())
        if alarmLevel < 4:
                print "Alarm raised Level %d" % (alarmLevel)

def sendOkEmail():
        global alarmRaised
        if alarmRaised == True:
                message = MIMEText("Server seems to be OK")
                message['Subject'] = "Server OK"
                message['To'] = COMMASPACE.join(receivers)
                smtpObj.sendmail(sender, receivers, message.as_string())
                alarmRaised = False


timer = threading.Timer(timerInterval, sendPing)
timer.start()

