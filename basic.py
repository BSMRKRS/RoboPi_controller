from setup import RPL
import post_to_web as PTW # see post_to_web.py for instructions

sensor_pin = 16
RPL.pinMode(sensor_pin,RPL.INPUT)

while True:
  PTW.state['d1'] = RPL.digitalRead(sensor_pin)
  PTW.post()
