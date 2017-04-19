import RoboPiLib as RoboPi
import time as time
RoboPi.RoboPiInit("/dev/ttyAMA0", 115200)
#AMA0 has a zero

servo = RoboPi.SERVO

left_servo = 1
right_servo = 2
up_servo = 3
down_servo = 4

RoboPi.pinMode (left_servo, servo)
RoboPi.pinMode (right_servo, servo)
RoboPi.pinMode (up_servo, servo)
RoboPi.pinMode (down_servo, servo)

#stop = 0
#clockwise = 500
#counter_clockwise = 2500

def go_forward():
    RoboPi.servoWrite(left_servo, 500)
    RoboPi.servoWrite(right_servo, 2500)
    RoboPi.servoWrite(up_servo, 2500)
    RoboPi.servoWrite(down_servo, 500)

def go_backward():
    RoboPi.servoWrite(left_servo, 2500)
    RoboPi.servoWrite(right_servo, 500)
    RoboPi.servoWrite(up_servo, 500)
    RoboPi.servoWrite(down_servo, 2500)

def spin_counterclockwise():
    RoboPi.servoWrite(left_servo, 2500)
    RoboPi.servoWrite(right_servo, 2500)
    RoboPi.servoWrite(up_servo, 2500)
    RoboPi.servoWrite(down_servo, 2500)

def spin_clockwise():
    RoboPi.servoWrite(left_servo, 500)
    RoboPi.servoWrite(right_servo, 500)
    RoboPi.servoWrite(up_servo, 500)
    RoboPi.servoWrite(down_servo, 500)

def stop():
    RoboPi.servoWrite(left_servo, 0)
    RoboPi.servoWrite(right_servo, 0)
    RoboPi.servoWrite(up_servo, 0)
    RoboPi.servoWrite(down_servo, 0)

def wall_left():
    spin_clockwise()
    time.sleep(.4)
    go_forward()
    time.sleep(0.5)
    spin_counterclockwise()
    time.sleep(.25)

def wall_right():
    spin_counterclockwise()
    time.sleep(.4)
    go_forward()
    time.sleep(0.5)
    spin_clockwise()
    time.sleep(.25)
