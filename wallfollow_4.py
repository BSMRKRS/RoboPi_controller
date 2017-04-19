#!/usr/bin/python
import RoboPiLib as RoboPi
import time as time
import motor_instructions as motors

#INPUT = RoboPi.INPUT

#FRONT_BUMPER = 20
LEFT_GO = 0

#RoboPi.pinMode(FRONT_BUMPER, RoboPi.INPUT)
#RoboPi.pinMode(LEFT_GO, RoboPi.INPUT)
#RoboPi.pinMode(RIGHT_GO, RoboPi.INPUT)

def forward():
    motors.go_forward()
    print "Forward!"
def clockwise():
    motors.spin_clockwise()
    print "Clockwise!"
def counterclockwise():
    motors.spin_counterclockwise()
    print "Counter Clockwise"
def stop():
    motors.stop()
    print "Alto"
def wall_left():
    motors.wall_left()
    print "wall_left"
def wall_right():
    motors.wall_right()
    print "wall_right"

##Analog
while 1:

    left_sensor = RoboPi.analogRead(LEFT_GO)

    L_VOLTS = 1000 / (RoboPi.analogRead(LEFT_GO) + 0.0000000001)
    L_CM = RoboPi.analogRead(LEFT_GO)

    go_forward = False
    go_clockwise = False
    go_counterclockwise = False
    go_stop = False
    go_wall_left = False
    go_wall_right = False

    print RoboPi.analogRead(LEFT_GO)

    if L_CM > 400:
        go_wall_left = True
    elif L_CM > 200:
        go_forward = True
    else:
        go_wall_right = True

## DECISION
    if go_forward:
        forward()
    elif go_clockwise:
        clockwise()
    elif go_counterclockwise:
        counterclockwise()
    elif go_stop:
        stop()
    elif go_wall_left:
        wall_left()
    elif go_wall_right:
        wall_right()


RoboPi.RoboPiExit()
