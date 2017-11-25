#!/usr/bin/python3

from subprocess import Popen
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE
import time
import os

cmd = "omxplayer /home/pi/hand/eyes.mp4 --no-osd --loop --aspect-mode stretch"
omxp = Popen ([cmd], shell=True)


ts = Touchscreen()
intruderAlert=False
idleMode=True
startTime = time.time()
isPaused = False

def PlayMovieAt(pos) :
	new_cmd = "/home/pi/dbuscontrol.sh setposition " + pos
	Popen([new_cmd], shell=True)

def TogglePause() :
	cmd = "/home/pi/dbuscontrol.sh pause"
	Popen([cmd], shell=True)

def touch_handler(event, touch):
	global intruderAlert
	global idleMode
	global isPaused

	if event == TS_PRESS:
		print("Got Press", touch)
		if intruderAlert == False:
			PlayMovieAt("3000000")
			print("Set Position to 3 secs")
			intruderAlert=True
			idleMode=False
			startTime=time.time()

	if event == TS_RELEASE:
		print("Got release", touch)
		idleMode=True
		intruderAlert=False
		startTime=time.time()
		if isPaused == True:
			TogglePause()
			isPaused=False
	if event == TS_MOVE:
		print("Got move", touch)
		startTime=time.time()

for touch in ts.touches:
	touch.on_press = touch_handler
	touch.on_release = touch_handler
	touch.on_move = touch_handler

ts.run()

while True:
	#Redraw Code etc
	t = int(round( time.time() - startTime))
	if t > 3:
		startTime= time.time()
		if idleMode==True:
			if isPaused==True:
				TogglePause()
				isPaused=False
			PlayMovieAt("000000")
		elif isPaused == False:
			TogglePause()
			isPaused=True
	try:
		pass
	except KeyboardInterrupt:
		cmd = "/home/pi/dbuscontrol.sh stop"
		Popen([cmd], shell=True)
		ts.stop()
		exit()



