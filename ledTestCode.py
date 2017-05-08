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
    time.sleep(0.5)
    print "led OFF"
i = int(raw_input("How many times the light will blink>"))
#<<<<<<< HEAD
#for n in range(i+1):
    #blink()

#def runServo():
#    RPL.servoWrite(ledPin,3000)
#=======
#for n in range(i):
 #   blink()

def runServo():
    RPL.servoWrite(ledPin,250)
#>>>>>>> 3ac775063ea8cbb37bfec0d8876d97d7aa6310ac
    print "led On"
    print "motor On"
    time.sleep(2)
    RPL.servoWrite(ledPin,0)
    print "motor and ledOff"
runServo()

#runServo()
#>>>>>>> 3ac775063ea8cbb37bfec0d8876d97d7aa6310ac
