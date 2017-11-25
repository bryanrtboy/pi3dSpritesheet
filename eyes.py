#!/usr/bin/python3

from subprocess import Popen
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE
import time
import os

cmd = "omxplayer /home/pi/hand/eyes.mp4 --no-osd --loop --aspect-mode stretch"
omxp = Popen ([cmd], shell=True)


ts = Touchscreen()

isIdle = False
isActive = False
pauseDelay = 1

def PlayMovieAt(pos) :
	new_cmd = "/home/pi/dbuscontrol.sh setposition " + pos
	Popen([new_cmd], shell=True)

def TogglePause() :
	cmd = "/home/pi/dbuscontrol.sh pause"
	Popen([cmd], shell=True)

def touch_handler(event, touch):
	global isIdle
	global isActive

	if event == TS_PRESS:
		print("Got Press", touch)
		if isIdle == True :
			print("Making video active")
			isIdle=False
			isActive=True
			TogglePause()
			time.sleep(3)
			TogglePause()
		elif isActive == True :
			print("video was active and paused, now unpausing it")
			TogglePause()
			time.sleep(3)
			PlayMovieAt("0")
			time.sleep(pauseDelay)
			TogglePause()
			isIdle=True
			isActive=False
			print("going back to idle mode")

	if event == TS_RELEASE:
		print("Got release", touch)

	if event == TS_MOVE:
		print("Got move", touch)

for touch in ts.touches:
	touch.on_press = touch_handler
	#touch.on_release = touch_handler
	#touch.on_move = touch_handler

ts.run()

PlayMovieAt("0")
time.sleep(3)
PlayMovieAt("0")
time.sleep(pauseDelay)
TogglePause()
isIdle=True

print("movie is paused at begginning")

while True:
	try:
		pass
	except KeyboardInterrupt:
		cmd = "/home/pi/dbuscontrol.sh stop"
		Popen([cmd], shell=True)
		ts.stop()
		exit()



