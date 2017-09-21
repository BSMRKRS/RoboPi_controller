import RoboPiLib_pwm as RPL
import time as time
RPL.RoboPiInit("/dev/ttyAMA0",115200)

#pins
ledPin = 1

RPL.pinMode(ledPin,RPL.OUTPUT)



#commands
def blink():
    RPL.digitalWrite(ledPin,1)
    print "led ON"
    time.sleep(0.5)
    RPL.digitalWrite(ledPin,0)
    print "led OFF"
i = int(raw_input("How many times the light will blink>"))
for n in range(i+1):
    blink()
