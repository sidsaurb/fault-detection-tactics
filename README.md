# fault-detection-tactics

This is a python implemention of the following tactics used for fault detection in software systems:

* Ping-Echo: in the ping-echo directory you will find a file monitor.py. It monitors whether the specified adderess is reachable or not. If not, it sends an email to mentioned email addresses.
* Heartbeat: in the heartbeat directory you will find two files: server.py and monitor.py. The file server.py is a dummy server which sends http requests to monitor.py. If monitor.py didn't get any request within a given duration is sends email to specied email addresses.
