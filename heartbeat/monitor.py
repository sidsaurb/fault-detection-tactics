#!/usr/bin/python

from flask import Flask
import time
import threading
import smtplib
import datetime
from email.utils import COMMASPACE
from email.mime.text import MIMEText

app = Flask(__name__)

alarmLevel = 0
alarmRaised = False
timerInterval = 10.0

sender = 'ftpmassignmentiitk@gmail.com'
receivers = ["sidsaurb@iitk.ac.in"]

smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login("ftpmassignmentiitk@gmail.com", "")

@app.route("/monitor")
def updateTime():
	try:
		fo = open("lasttime.txt", "wb")
		fo.write(str(int(round(time.time() * 1000))))
		fo.close()
		print "beat received"
		return "Ok"
	except:
		return "Error"

def checkTimestamp():
	try:
		global alarmLevel
		#print "timer hit"
		fo = open("lasttime.txt", "r")
		timestamp = int(fo.read(13))
		fo.close()
		currentTimestamp = int(round(time.time() * 1000))
		if currentTimestamp > timestamp + (timerInterval * 1000):
			raiseAlarm(timestamp)
		else:
			sendOkEmail()
			alarmLevel = 0
		timer = threading.Timer(timerInterval, checkTimestamp)
		timer.start()
	except Exception as inst:
		print inst
		pass
		
def raiseAlarm(timestamp):
	global alarmLevel
	global alarmRaised
	if alarmLevel < 4:
		alarmLevel += 1
	alarmRaised = True
	s = timestamp / 1000.0
	downSince = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
	message = MIMEText("No beat received since " + downSince)		
	message['To'] = COMMASPACE.join(receivers)
	if alarmLevel == 1:
		message['Subject'] = "Server possibly down: Alarm level 1"
		smtpObj.sendmail(sender, receivers, message.as_string())
	if alarmLevel == 2:		
		message['Subject'] = "Server possibly down: Alarm level 2"
		smtpObj.sendmail(sender, receivers, message.as_string())
	if alarmLevel == 3:		
		message['Subject'] = "Server possibly down: Alarm level 3"
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

if __name__ == '__main__':
	timer = threading.Timer(timerInterval, checkTimestamp)
	timer.start()
	#print "timer started"
	app.run()
