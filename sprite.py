#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

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
DISPLAY = pi3d.Display.create(frames_per_second=25.0)

#create shaders
flatsh = pi3d.Shader("uv_flat")

#Create textures
spritetex = pi3d.Texture("spriteSheet_2X4.jpg")

#Create camera
CAMERA = pi3d.Camera(is_3d=False)

#Create shape
mysprite = pi3d.LodSprite(w=800.0, h=480.0, n=6)
mysprite.set_draw_details(flatsh,[spritetex],umult=.5,vmult=.25)

tick = 0
av_fps = 0
spf = 0.1 # seconds per frame
next_time = time.time() + spf
offset = 0.0 # uv v offset
do = -0.25 # uv v increment



# Fetch key presses.
mykeys = pi3d.Keyboard()

# Display scene and rotate shape
while DISPLAY.loop_running():

  mysprite.draw()

  if time.time() > next_time:
    next_time = time.time() + spf
    av_fps = av_fps*0.9 + tick/spf*0.1 # exp smooth moving average
    print(av_fps,"FPS\r")
    tick = 0
    offset = (offset + do) % 1.0 # move texture offset in v direction
    mysprite.set_offset((0.0, offset))

  tick += 1

  k = mykeys.read()
  if k==112:
    pi3d.screenshot("water1.jpg")
  elif k==27:
    mykeys.close()
    DISPLAY.destroy()
    break

quit()
