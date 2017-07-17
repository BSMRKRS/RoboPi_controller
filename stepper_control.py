import RoboPiLib_pwm as RPL
import time as time
RPL.RoboPiInit("/dev/ttyAMA0",115200)

shoulder_pul = 7
shoulder_dir = 6
elbow_pul = 5
elbow_dir = 3

up = True
down = False

RPL.pinMode(shoulder_pul, RPL.PWM)
RPL.pinMode(shoulder_dir, RPL.OUTPUT)
RPL.pinMode(elbow_pul, RPL.PWM)
RPL.pinMode(elbow_dir, RPL.OUTPUT)

speed = 1000

def stop():
  RPL.pwmWrite(shoulder_pul, 0, 10000)
  RPL.pwmWrite(elbow_pul, 0, 10000)

def shoulder(dir, run_for = 1, speed = speed):
  if(dir):
    RPL.digitalWrite(shoulder_dir, 1)
  else:
    RPL.digitalWrite(shoulder_dir, 0)
  RPL.pwmWrite(shoulder_pul, speed, speed * 2)
  time.sleep(run_for)
  stop()


def elbow(dir, run_for = 1, speed = speed):
  if(dir):
    RPL.digitalWrite(elbow_dir, 1)
  else:
    RPL.digitalWrite(elbow_dir, 0)
  RPL.pwmWrite(elbow_pul, speed, speed * 2)
  time.sleep(run_for)
  stop()
def wristRotateClockwise():
  RPL.servoWrite(9, 10)
  time.sleep(1)
  RPL.servoWrite(9,0)

def wristRotateCounter():
  RPL.servoWrite(9,3000)
  time.sleep(1)
  RPL.servoWrite(9,0)

def wristFlipUp():
  RPL.servoWrite(10,10)
  time.sleep(1)
  RPL.servoWrite(10,0)

def wristGrasperOpen():
  RPL.servoWrite(11,10)
  time.sleep(1)
  RPL.servoWrite(11,0)
#ui control for ar control. a = shoulder back. s = shoulder forward. d = elbow backward. f = elbow forward
def ui():
  input = raw_input()
  if input == "a":
    shoulder(False,1,100)
  elif input == "s":
    shoulder(True,1,100)
  elif input == "d":
    elbow(False,1,100)
  elif input == "f":
    elbow(True,1,100)
  elif input == " ":
    stop()
  elif input == "q":
    quit()
  elif input == "w":
    wristRotateClockwise()
  elif input == "r":
    wristFlipUp()
  elif input == "t":
    wristGrasperOpen()
  else:
    print "Not a command"
  ui()  

ui()
# python
# import stepper_control as st
# st.elbow(True)
# st.elbow(False) Run in the other direction
# st.elbow(True, 2) Run for 2 seconds
# st.elbow(True, 2, 100) Run for 2 seconds much faster
