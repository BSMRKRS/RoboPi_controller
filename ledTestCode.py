import RoboPiLib_pwm as RPL
import time as time
RPL.RoboPiInit("/dev/ttyAMA0",115200)

#pins
ledPin = 1
RPL.pinMode(ledPin,OUTPUT)



#commands
def blink():
    RPL.digitalWrite(ledPin,1)
    print "led ON"
    time.sleep(2)
    RPL.digitalWrite(ledPin,0)
    print "led OFF"

blink()
