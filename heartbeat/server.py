#!/usr/bin/python

import threading
import urllib2

timerInterval = 10.0

def sendBeat():
	try:
		resp = urllib2.urlopen("http://127.0.0.1:5000/monitor").read()
		if resp == "Ok":
			print "Beat successfully sent"
		else:
			print "Error in sending beat"
		timer = threading.Timer(timerInterval, sendBeat)
		timer.start()
	except Exception as inst:
		print inst
		timer = threading.Timer(timerInterval, sendBeat)
		timer.start()

timer = threading.Timer(0, sendBeat)
timer.start()
