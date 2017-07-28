# Kirwin's vi tab preferences: set shiftwidth=2 softtabstop=2 expandtab
import xml.etree.ElementTree as ET
import RoboPiLib_pwm as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import time as time
import os
import random

import sys, tty, termios, select, time, signal

######################
## Motor Establishment
######################
#pins 2-5 do not work

freq = 3000
motorL = 0
motorR = 1
servo1 = 8 # Wrist Pitch
servo1_step = 10
servo2 = 9 # Wrist Roll
servo3 = 10 # grabber
servo4 = 14 # Front camera
servo5 = 15 # Front camera
elbow_dir = 6 # Original:3
elbow_pulse = 7 # Original:5
shoulder_dir = 12  # Original 6
shoulder_pulse = 13 # Original:7

motorR_forward = 2000
motorR_backward = 1000
motorL_forward = 2000
motorL_backward = 1000

try:
  RPL.pinMode(motorL,RPL.PWM)
  RPL.pwmWrite(motorL,1500,freq)
  RPL.pinMode(motorR,RPL.PWM)
  RPL.pwmWrite(motorR,1500,freq)
  RPL.pinMode(servo1,RPL.SERVO)
  RPL.servoWrite(servo1, 1500)
  RPL.pinMode(servo2,RPL.SERVO)
  RPL.pinMode(servo3,RPL.SERVO)
  RPL.pinMode(servo4,RPL.SERVO)
  RPL.pinMode(servo5,RPL.SERVO)
  RPL.pinMode(elbow_dir,RPL.OUTPUT)
  RPL.pinMode(elbow_pulse,RPL.PWM)
  RPL.pwmWrite(elbow_pulse,0, 500)
  RPL.pinMode(shoulder_dir,RPL.OUTPUT)
  RPL.pinMode(shoulder_pulse,RPL.PWM)
  RPL.pwmWrite(shoulder_pulse,0, 500)
except:
  pass
######################
## Individual commands
######################
def stopAll():
  try:
    RPL.pwmWrite(motorL,1500, freq)
    RPL.pwmWrite(motorR,1500, freq)
    RPL.servoWrite(servo2,1500)
    RPL.servoWrite(servo3,1500)
    RPL.servoWrite(servo4,1500)
    RPL.servoWrite(servo5,1500)
    RPL.pwmWrite(shoulder_pulse, 0, 400)
    RPL.pwmWrite(elbow_pulse, 0, 400)
  except:
    print "error except"
    pass

def forward():
  RPL.pwmWrite(motorL,motorL_forward, freq)
  RPL.pwmWrite(motorR,motorR_forward, freq)

def reverse():
  RPL.pwmWrite(motorL,motorL_backward, freq)
  RPL.pwmWrite(motorR,motorR_backward, freq)

def right():
  RPL.pwmWrite(motorL,motorL_forward, freq)
  RPL.pwmWrite(motorR,motorR_backward, freq)

def left():
  RPL.pwmWrite(motorL,motorL_backward,freq)
  RPL.pwmWrite(motorR,motorR_forward,freq)

def forward_right():
  RPL.pwmWrite(motorL,motorL_forward,freq)
  RPL.pwmWrite(motorR,1500,freq)

def forward_left():
  RPL.pwmWrite(motorL,1500,freq)
  RPL.pwmWrite(motorR,motorR_forward,freq)

def backward_right():
  RPL.pwmWrite(motorL,1500,freq)
  RPL.pwmWrite(motorR,motorR_backward,freq)

def backward_left():
  RPL.pwmWrite(motorL,motorL_backward,freq)
  RPL.pwmWrite(motorR,1500,freq)
#wrist pitch: working
def servo1up(): # Wrist pitch
  a = RPL.servoRead(servo1)
  if a >= 2400:
    RPL.servoWrite(servo1,2400)
    print  'Wrist pitch: ', a
  else:
    RPL.servoWrite(servo1,min( a + servo1_step, 2400))
    print  a
def servo1down():
    a = RPL.servoRead(servo1)
    if a <= 600:
      RPL.servoWrite(servo1, 600)
    else:
      RPL.servoWrite(servo1,max( a - servo1_step, 600))
    print  'Wrist pitch: ', a
#wrist rotate: wiring problem?
def servo2up():
  RPL.servoWrite(servo2,2500)
  RPL.servoWrite(servo3,2000)
def servo2down():
  RPL.servoWrite(servo2,500)
  RPL.servoWrite(servo3,1000)
#wrist grasp: working
def servo3up():
  RPL.servoWrite(servo3,2500)

def servo3down():
  RPL.servoWrite(servo3,500)

def servo4up():
  RPL.servoWrite(servo4, 2000)
def servo4down():
  RPL.servoWrite(servo4, 1000)

def servo5up():
  RPL.servoWrite(servo5, 2000)
def servo5down():
  RPL.servoWrite(servo5, 1000)

def shoulder_up():
  RPL.digitalWrite(shoulder_dir, 0)
  RPL.pwmWrite(shoulder_pulse, 400, 800)

def shoulder_down():
  RPL.digitalWrite(shoulder_dir, 1)
  RPL.pwmWrite(shoulder_pulse, 400, 800)

def elbow_up():
  RPL.digitalWrite(elbow_dir, 0)
  RPL.pwmWrite(elbow_pulse, 400, 800)

def elbow_down():
  RPL.digitalWrite(elbow_dir, 1)
  RPL.pwmWrite(elbow_pulse, 400, 800)

def forwardSpeedChanges(change, mn = 1600, mx = 2900):
  global motorR_forward
  global motorL_forward
  motorR_forward += change
  motorL_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  motorL_forward = max(min(motorL_forward, mx), mn)
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

def backwardSpeedChanges(change, mn = 100, mx = 1400):
  global motorR_backward
  global motorL_backward
  motorR_backward += change
  motorL_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  motorL_backward = max(min(motorL_backward, mx), mn)
  print 'BACKWARD: Left Motor: ', motorL_backward, ' Right Motor: ', motorR_backward, '\r'

def backwardRightSpeedChange(change, mn = 100, mx = 1400):
  global motorR_backward
  motorR_backward += change
  motorR_backward = max(min(motorR_backward, mx), mn)
  print 'BACKWARD: Left Motor: ', motorL_backward, ' Right Motor: ', motorR_backward, '\r'

def backwardLeftSpeedChange(change, mn = 100, mx = 1400):
  global motorL_backward
  motorL_backward += change
  motorL_backward = max(min(motorL_backward, mx), mn)
  print 'BACKWARD: Left Motor: ', motorL_backward, ' Right Motor: ', motorR_backward, '\r'

def forwardRightSpeedChange(change, mn = 1600, mx = 2900):
  global motorR_forward
  motorR_forward += change
  motorR_forward = max(min(motorR_forward, mx), mn)
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

def forwardLeftSpeedChange(change, mn = 1600, mx = 2900):
  global motorL_forward
  motorL_forward += change
  motorL_forward = max(min(motorL_forward, mx), mn)
  print 'FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'

SHORT_TIMEOUT = 0.2 # number of seconds your want for timeout

fd = sys.stdin.fileno() # I don't know what this does
old_settings = termios.tcgetattr(fd) # this records the existing console settings that are later changed with the tty.setraw... line so that they can be replaced when the loop ends

######################################
## Other motor commands should go here
######################################

def interrupted(signum, frame): # this is the method called at the end of the alarm
  stopAll()

signal.signal(signal.SIGALRM, interrupted) # this calls the 'interrupted' method when the alarm goes off
tty.setraw(sys.stdin.fileno()) # this sets the style of the input

while True:
  signal.setitimer(signal.ITIMER_REAL,SHORT_TIMEOUT) # this sets the alarm
  ch = sys.stdin.read(1) # this reads one character of input without requiring an enter keypress
  signal.setitimer(signal.ITIMER_REAL,0) # this turns off the alarm
  if ch == '*': # pressing the asterisk key kills the process
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # this resets the console settings
    break # this ends the loop
  else:
    if ch == 'w':
      forward()
    elif ch == "a":
      left()
    elif ch == "s":
      reverse()
    elif ch == "d":
      right()
    elif ch == "e":
      forward_right()
    elif ch == "q":
      forward_left()
    elif ch == "t":
      shoulder_up()
    elif ch == "g":
      shoulder_down()
    elif ch == "y":
      elbow_up()
    elif ch == "h":
      elbow_down()
    elif ch == "u":
      servo1up()
    elif ch == "j":
      servo1down()
    elif ch == "i":
      servo2up()
    elif ch == "k":
      servo2down()
    elif ch == "o":
      servo3up()
    elif ch == "l":
      servo3down()
    elif ch == "m":
      servo4up()
    elif ch == "n":
      servo4down()
    elif ch == "b":
      servo5up()
    elif ch == "v":
      servo5down()
    elif ch == "z":
      backward_left()
    elif ch == "c":
      backward_right()
    elif ch == "]":
      forwardSpeedChanges(100)
    elif ch == "[":
      backwardSpeedChanges(-100)
    elif ch == "}":
      forwardSpeedChanges(-100)
    elif ch == "{":
      backwardSpeedChanges(100)
    elif ch == "1":
      forwardLeftSpeedChange(100)
    elif ch == "!":
      forwardLeftSpeedChange(-100)
    elif ch == "2":
      forwardRightSpeedChange(100)
    elif ch == "@":
      forwardRightSpeedChange(-100)
    elif ch == "3":
      backwardLeftSpeedChange(-100)
    elif ch == "#":
      backwardLeftSpeedChange(100)
    elif ch == "4":
      backwardRightSpeedChange(-100)
    elif ch == "$":
      backwardRightSpeedChange(100)
    else:
      stopAll()
