import RoboPiLib as RPL
import setup
import time

def Stop():
    RPL.servoWrite(8,1500)
    RPL.servoWrite(9,1500)

def Forward():
    RPL.servoWrite(8,2000)
    RPL.servoWrite(9,1000)
    time.sleep(2)
    Stop()

def Backward():
    RPL.servoWrite(8,1000)
    RPL.servoWrite(9,2000)
    time.sleep(0)
    Stop()

def Clock():
    RPL.servoWrite(8,2000)
    RPL.servoWrite(9,2000)
    time.sleep(2)
    Stop()

def Counterclock():
    RPL.servoWrite(8,1000)
    RPL.servoWrite(9,1000)
    time.sleep(2)
    Stop()


Counterclock()
