import RoboPiLib_pwm as RPL
import time as time
RPL.RoboPiInit("/dev/ttyAMA0",115200)

ledPin = 1

RPL.pinMode(ledPin,OUTPUT)

def blink():
    RPL.digitalWrite(ledPin,1)
    time.sleep(2)
    RPL.digitalWrite(ledPin,0)
