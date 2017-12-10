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
DISPLAY = pi3d.Display.create(frames_per_second=60.0)
CAMERA = pi3d.Camera(is_3d=True)

#create shaders and textures
flatsh = pi3d.Shader("uv_flat")
cell = pi3d.Shader("star")
spritetex = pi3d.Texture("bryan2.jpg")

rows=4
columns = 4

frames = []

#Frames start in upper left, go down first and then across
for i in range(columns):
  x= i * (1/columns)
  for r in range(rows):
    y = r * (1/rows)
    frames.append([x,y])

#print(frames)
#quit()

#Create shape and offset variables
mysprite = pi3d.LodSprite(w=800.0, h=500.0, n=6)
mysprite.set_draw_details(flatsh,[spritetex],umult=1/columns,vmult=1/rows)

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

def play(start,end):
  global frame
  global mysprite
  if frame >= end:
    frame=start
  mysprite.set_offset(frames[frame])
  frame += 1

myplane = pi3d.Plane(w=80,h=40)
#myplane.set_shader(cell)

myplane.set_draw_details(cell,[spritetex])
#myplane.rotateToX(180)
myplane.translateZ(100)

# Display scene and rotate shape
while DISPLAY.loop_running():
 # mysprite.draw()
  myplane.draw()
  myplane.rotateIncX(2)
  myplane.rotateIncY(2)

#frame 3,4,5 play once with this setup, and then it loops 
  if isIdle == True :
    play(0,5)
  else:
    play(12,15)

  k = mykeys.read()
  if k==112:
    pi3d.screenshot("water1.jpg")
  elif k==27:
    mykeys.close()
    DISPLAY.destroy()
    break

ts.stop()
quit()


