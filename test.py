import RoboPiLib_pwm1 as RPL
import setup
from time import sleep

freq = 3000

RPL.pinMode(8, RPL.PWM)
RPL.pinMode(9, RPL.PWM)

RPL.pwmWrite(8, 2000, freq)
sleep(.0001)
RPL.pwmWrite(9, 2000, freq)

sleep(1)

RPL.pwmWrite(8, 0, freq)
sleep(.0001)
RPL.pwmWrite(9, 0, freq)

RPL.RoboPiExit()
