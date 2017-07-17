# python web2py.py -c server.crt -k server.key -a 'Engineering1!' -i 0.0.0.0 -p 8000
# Kirwin's vi tab preferences: set shiftwidth=2 softtabstop=2 expandtab
import xml.etree.ElementTree as ET
import RoboPiLib_pwm as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import time as time
import os
import logging
import logging.handlers
import random
from math import cos
from math import sin
from math import degrees
from math import radians
from math import fabs
import pickle


import sys, tty, termios, select, time, signal
#creates array (technically, python list) of all 5000 points accsessible by the arm)
point = 0

with open("theMasterList.py","rb") as fp:    masterList = pickle.load(fp)

LOG_FILENAME = '/home/student/web2py/logs/logging_rotatingfile_example.out'
log = logging.getLogger('RoboPi_controller')
log.setLevel(logging.DEBUG)
if(len(log.handlers)==0):
  handler = logging.handlers.RotatingFileHandler(LOG_FILENAME)
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)
  log.addHandler(handler)

######################
## Motor Establishment
######################
#pins 2-5 do not work

freq = 3000
motorL = 0
motorR = 1
servo1 = 8 # Wrist Pitch
servo2 = 9 # Wrist Roll
servo3 = 10 # Grabber
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
  RPL.pinMode(servo2,RPL.SERVO)
  RPL.pinMode(servo3,RPL.SERVO)
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
    #stops both drive motors
    RPL.pwmWrite(motorL,1500, freq)
    RPL.pwmWrite(motorR,1500, freq)
    #stops all wrist servos
    RPL.servoWrite(servo2,1500)
    RPL.servoWrite(servo3,1500)
    #stops shoulder and elbow
    RPL.pwmWrite(shoulder_pulse, 0, 400)
    RPL.pwmWrite(elbow_pulse, 0, 400)

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
    if a > 2400:
       RPL.servoWrite(servo1,1700)
    else:
       RPL.servoWrite(servo1,min( a + 100, 2400))

def servo1down():
    a = RPL.servoRead(servo1)
    if a < 600:
       RPL.servoWrite(servo1, 1700)
    else:
       RPL.servoWrite(servo1,max( a - 100, 600))
#wrist rotate: wiring problem?
def servo2up():
    RPL.servoWrite(servo2,2500)

def servo2down():
    RPL.servoWrite(servo2,500)
#wrist grasp: working
def servo3up():
    RPL.servoWrite(servo3,2500)

def servo3down():
    RPL.servoWrite(servo3,500)
#
def shoulder_up():
    RPL.digitalWrite(shoulder_dir, 0)
    RPL.pwmWrite(shoulder_pulse, 200, 400)

def shoulder_down():
    RPL.digitalWrite(shoulder_dir, 1)
    RPL.pwmWrite(shoulder_pulse, 200, 400)

def elbow_up():
    RPL.digitalWrite(elbow_dir, 0)
    RPL.pwmWrite(elbow_pulse, 200, 400)

def elbow_down():
    RPL.digitalWrite(elbow_dir, 1)
    RPL.pwmWrite(elbow_pulse, 200, 400)

#takes current position, and makes a list of all points accsessible by the arm within a certain vertical tolerance (currently 0.1 in, but this can be changed)
def planeX():
    yInPlane = []
    readout = []
    global masterListPosition
    position = masterList[masterListPosition]
    for i in range(len(masterList)):
        if fabs(position[1] - masterList[i][1]) <= 0.1:
            deltaShoulder = masterList[i][2] - position[2]
            deltaElbow = masterList[i][3] - position[3]
            yInPlane.append([masterList[i][0],masterList[i][1],deltaShoulder,deltaElbow,i])
            yInPlane.sort()
    for i in range(len(yInPlane)):
        if yInPlane[i][4] == masterListPosition:
            global point
            point = i
            print "-" * 10
            print yInPlane[i]
            print "-" * 10
        else:
            print yInPlane[i]
    print len(yInPlane)
    return yInPlane

def planeY():
    xInPlane = []
    readout = []
    global masterListPosition
    position = masterList[masterListPosition]
    for i in range(len(masterList)):
        if fabs(position[0] - masterList[i][0]) <= 0.1:
            deltaShoulder = masterList[i][2] - position[2]
            deltaElbow = masterList[i][3] - position[3]
            xInPlane.append([masterList[i][1],masterList[i][0],deltaShoulder,deltaElbow,i])
            xInPlane.sort()
    for i in range(len(xInPlane)):
        if xInPlane[i][2] == 0 and xInPlane[i][3] == 0:
            global point
            point = i
            masterListPosition = xInPlane[i][4]
            print "-" * 10
            print xInPlane[i]
            print "-" * 10
        else:
            print xInPlane[i]
    print len(xInPlane)
    return xInPlane


shoulderStepTest = 0
elbowStepTest = 0


def shoulderPulse(direction):
    RPL.digitalWrite(12,direction)
    RPL.pinMode(13,RPL.OUTPUT)
    RPL.digitalWrite(13,0)
    RPL.digitalWrite(13,1)
    RPL.digitalWrite(13,0)
    global shoulderStepTest
    global shoulderStep
    if direction == 1:
        shoulderStepTest += 1
        shoulderStep += 1

    else:
        shoulderStepTest -= 1
        shoulderStep -= 1

def elbowPulse(direction):
    RPL.digitalWrite(6,direction)
    RPL.pinMode(7,RPL.OUTPUT)
    RPL.digitalWrite(7,0)
    RPL.digitalWrite(7,1)
    RPL.digitalWrite(7,0)
    global elbowStepTest
    global elbowStep
    if direction == 1:
        elbowStepTest += 1
        elbowStep += 1
    else:
        elbowStepTest -= 1
        elbowStep -= 1
def calibrate():
    shoulderStep = 0
    elbowStep = 0
    for i in range(201):
        shoulderPulse(1)
    for k in range(1593):
        elbowPulse(1)
    global masterListPosition
    masterListPosition = 3040
def debugSetup():
    for i in range(len(masterList)):
        if masterList[i][2] == 201 and masterList[i][3] == 1593:
            print i

def moveXforward():
    yInPlane = planeX()
    global shoulderStepTest
    global elbowStepTest
    shoulderStepTest = 0
    elbowStepTest = 0
    print point
    if yInPlane[point+1][2] >= 0:
        for i in range(int(fabs(yInPlane[point+1][2]))):
            shoulderPulse(1)
    else:
        for i in range(int(fabs(yInPlane[point+1][2]))):
            shoulderPulse(0)

    if yInPlane[point+1][3] >= 0:
        for i in range(int(fabs(yInPlane[point+1][3]))):
            elbowPulse(1)
    else:
        for i in range(int(fabs(yInPlane[point+1][3]))):
            elbowPulse(0)
    global masterListPosition
    masterListPosition = yInPlane[point + 1][4]
    print "The shoulder moved %d steps and the elbow moved %d steps" % (shoulderStepTest, elbowStepTest)
    print masterList[masterListPosition]
    print point

def moveXbackward():
    yInPlane = planeX()
    global shoulderStepTest
    global elbowStepTest
    shoulderStepTest = 0
    elbowStepTest = 0
    if yInPlane[point-1][2] >= 0:
        for i in range(int(fabs(yInPlane[point-1][2]))):
            shoulderPulse(1)
    else:
        for i in range(int(fabs(yInPlane[point-1][2]))):
            shoulderPulse(0)

    if yInPlane[point-1][3] >= 0:
        for i in range(int(fabs(yInPlane[point-1][3]))):
            elbowPulse(1)
    else:
        for i in range(int(fabs(yInPlane[point-1][3]))):
            elbowPulse(0)
    global masterListPosition
    masterListPosition = yInPlane[point - 1][4]
    print "The shoulder moved %d steps and the elbow moved %d steps" % (shoulderStepTest, elbowStepTest)
    print masterList[masterListPosition]
    print point


def moveYupward():
    xInPlane = planeY()
    global shoulderStepTest
    global elbowStepTest
    shoulderStepTest = 0
    elbowStepTest = 0
    print point
    if xInPlane[point+1][2] >= 0:
        for i in range(int(fabs(xInPlane[point+1][2]))):
            shoulderPulse(1)
    else:
        for i in range(int(fabs(xInPlane[point+1][2]))):
            shoulderPulse(0)

    if xInPlane[point+1][3] >= 0:
        for i in range(int(fabs(xInPlane[point+1][3]))):
            elbowPulse(1)
    else:
        for i in range(int(fabs(xInPlane[point+1][3]))):
            elbowPulse(0)
    global masterListPosition
    masterListPosition = xInPlane[point + 1][4]
    print "The shoulder moved %d steps and the elbow moved %d steps" % (shoulderStepTest, elbowStepTest)
    print masterList[masterListPosition]
    print point


def moveYdownward():
    xInPlane = planeY()
    global shoulderStepTest
    global elbowStepTest
    shoulderStepTest = 0
    elbowStepTest = 0
    if xInPlane[point-1][2] >= 0:
        for i in range(int(fabs(xInPlane[point-1][2]))):
            shoulderPulse(1)
    else:
        for i in range(int(fabs(xInPlane[point-1][2]))):
            shoulderPulse(0)

    if xInPlane[point-1][3] >= 0:
        for i in range(int(fabs(xInPlane[point-1][3]))):
            elbowPulse(1)
    else:
        for i in range(int(fabs(xInPlane[point-1][3]))):
            elbowPulse(0)
    global masterListPosition
    masterListPosition = xInPlane[point - 1][4]
    print "The shoulder moved %d steps and the elbow moved %d steps" % (shoulderStepTest, elbowStepTest)
    print masterList[masterListPosition]
    print point


command_dictionary = dict([(87,forward),(83,reverse),(68,right),(65,left),(69,forward_right),(81,forward_left),(67,backward_right),(90,backward_left),(74,servo1down),(85,servo1up),(75,servo2down),(73,servo2up),(76,servo3down),(79,servo3up), (84,shoulder_up), (71, shoulder_down), (89, elbow_up), (72, elbow_down)])
keys = list(command_dictionary.keys())
# 87:w, 83:s, 68:d, 65:a, 69:e, 81:q, 90:z, 67:c, 74: j, 85: u, 73: i, 75: k, 79: o, 76: l, 84: t, 71: g

masterListPosition = 0
shoulderStep = 0
elbowStep = 0
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
    elif ch == "q":
	forward_right()
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
    elif ch == "v":
        moveXbackward()
    elif ch == "b":
        moveXforward()
    elif ch == "n":
        moveYupward()
    elif ch == "m":
        moveYdownward()
    elif ch == "c":
        calibrate()
    else:
        stopAll()

################
## Logging Setup
################


def manControl():
	input == raw_input()
# Each entry in this dictionary of the format (number, command_name) references the commands in the Individual commands section. The commands will get either 'go' or 'stop' from the receive function at the top of this document.
# The numeric keys are the letters returned from javascript. You can view key presses by opening the javascript console in the web browser.
