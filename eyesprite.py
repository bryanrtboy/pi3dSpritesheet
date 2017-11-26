#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

""" 
This demo also shows the effect of set_material() in combination with a
uv mapped texture.
"""
import math, random, time
import pi3d

print("=====================================================")
print("press escape to escape")
print("move this terminal window to top of screen to see FPS")
print("=====================================================")

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(frames_per_second=12.0)
CAMERA = pi3d.Camera(is_3d=False)

#create shaders and textures
flatsh = pi3d.Shader("uv_flat")
spritetex = pi3d.Texture("spriteSheet_2X4.jpg")

#Create shape and offset variables
mysprite = pi3d.LodSprite(w=800.0, h=480.0, n=6)
mysprite.set_draw_details(flatsh,[spritetex],umult=.5,vmult=.25)

rows=4
columns = 2
frame=0

# Fetch key presses.
mykeys = pi3d.Keyboard()

#Handle touches and start Touch thread (runs independent of DISPLAY loop)
ts = Touchscreen()
isIdle = False
isActive = True

def touch_handler(event, touch):
  global isIdle
  global isActive

  if event == TS_PRESS:
    #print("\r\rGot Press\r", touch)
    if isIdle == True :
      print("Idle mode, making video active\r")
      isIdle=False
      isActive=True
    elif isActive == True :
      print("video was active and paused, now unpausing it\r")
      isIdle=True
      isActive=False
    else:
      print("Touch happened, but Idle and isActive were both false")

  if event == TS_RELEASE:
    print("Got release", touch,"\r")

  if event == TS_MOVE:
    print("Got move\r")

for touch in ts.touches:
   touch.on_press = touch_handler
   touch.on_release = touch_handler
   touch.on_move = touch_handler

ts.run()  

idleSequence = []

for i in range(2):
  x=0
  y=i*0.25
  idleSequence.append([x,y])

activeSequence = []

#this is not quite right, y goes past 1.0 and really should reset to 0.0 instead
for i in range(7):
  x=0
  if i > 3:
    x=.5
  y=i*0.25

  if i > 2 :
    activeSequence.append([x,y])

#activeSequence = [(0,.75),(0.5,0.0),(0.5,0.25),(0.5,0.5)]
print(activeSequence)

# Display scene and rotate shape
while DISPLAY.loop_running():
  frame += 1
  mysprite.draw()

  if isIdle == True :
    if frame >= len(idleSequence):
      frame=0
    mysprite.set_offset(idleSequence[frame])
  else:
    if frame >= len(activeSequence):
      frame=0
    mysprite.set_offset(activeSequence[frame])

  k = mykeys.read()
  if k==112:
    pi3d.screenshot("water1.jpg")
  elif k==27:
    mykeys.close()
    DISPLAY.destroy()
    break

ts.stop()
quit()


