#*****************************************************************************
#
# RoboPyLib_v0_97.py
#
# Copyright 2016 William Henning
#
# http://Mikronauts.com
#
# April 27, 2016: Initial Release
# May 20, 2016: First "Real" Release
# June 21, 2016: updated pulseGen
#
# Pure Python support library for RoboPi firmware, for use with RoboPi
#
# This version does not rely on the C RoboPiLib.o library and swc, and as such
# is multi-platform and should work on any SBC
#
# Currently the resetRoboPi(pin) call is an ugly hack dependant on pigpiod
# it will be replaced by generic sysfs gpio handling for multi-platform use
#
# This is a work in progress, and subject to change. I used non-blocking I/O as
# I intend to add timeouts at a future date.
#
# The code is NOT publication quality, not enough comments, later versions will
# be nicer :)
#
#******************************************************************************

import serial 		# import the pyser library
#import pigpio		# import the pigpio library
import time		# import the time library

# control characters used to indicate start & end of packet

SOH		= '\x01'
EOT		= '\x04'

# packet identifiers

GETINFO		=  0 	# returns product string
READMODE   	= 11 	# write pin mode
WRITEMODE   	= 12 	# write pin mode
DIGREAD     	= 13 	# digital read
DIGWRITE    	= 14 	# digital write
ANREAD      	= 15 	# analog read 10 bit result
ANREADRAW   	= 16 	# analog read at raw resolution
ANWRITE     	= 17 	# analog write 0..255 used for PWM
SERVOWRITE  	= 18 	# write a servo 0..20000us, normally 500-2500us
SERVOREAD   	= 19 	# read last value written to servo
READDIST  	= 20 	# read distance sensor
PULSEGEN	= 21	# start high frequency pulse train generator
PULSESTOP	= 22	# stop pulse train generator

# pin types

INPUT 		= 0
OUTPUT 		= 1
PWM 		= 16
SERVO 		= 32

# API

API_REVISION    = 0.97

# Global variables

myaddr 		=  1 	# default RoboPi address

ser		= -1

#**********************************************************************************
#
# Low level packet handling routines
#
# buff = bytearray(100) # creates 0 filled 100 long array of bytes
# buff = bytearray([32] * 100) # creates 100 space (val 32) array
#
#**********************************************************************************

def putPacket(cmd, buffr, plen):
  global myaddr

  chk = int(myaddr)+int(cmd)+int(plen)

  for i in range(0,plen):
    chk += int(buffr[i])

  packet = bytearray([SOH, myaddr, cmd, plen]) + buffr + bytearray([chk&255, EOT])

  ser.write(packet)

def getPacket():

  count=0
  
  while (ser.read(1) != SOH):
    count = count+1

#  print "Received garbage chars", count

  header = bytearray(ser.read(3))

  addr = header[0]
  cmd  = header[1]
  plen = header[2]
  
#  print "Header ", addr, cmd, plen

  checksum = addr + cmd + plen
  

#  print "b4"
  buf2 = bytearray(ser.read(plen))
#  print "buf2 length is",len(buf2)

  for i in range(0,plen):
#    print "byte",i,"=",buf2[i]
    checksum += buf2[i]

  chk = bytearray(ser.read(1))[0]

  if (checksum&255) != chk:
    print "Checksum Error!"

#  print "Waiting for EOT"

  while (ser.read(1) != EOT):
    count = count+1
    
#  print "Dropped ", count    

  #          0    1     2     3    4
  return [addr, cmd, plen, buf2, chk]

#**********************************************************************************
#
# Rest RoboPi - ugly hack version, next release will use sysfs to make it generic
#
# Does not seem to work when called right before / right after RoboPiInit
# suspect unusual interaction between python, pigpio, serial
# works fine stand-alone in resetRoboPi.py script
#
#**********************************************************************************

def RoboPiReset(pin): # pin is 17 on a Pi
#  pi3 = pigpio.pi()
  time.sleep(0.1)
#  pi3.set_mode(pin, pigpio.OUTPUT)
#  pi3.write(pin,0)
#  time.sleep(0.01)
#  pi3.write(pin,1)
#  time.sleep(0.5)
#  pi3.stop()

#**********************************************************************************
#
# RoboPi API - please see RoboPi User Manual for usage
#
#**********************************************************************************

def RoboPiExit():
  global ser

  if ser != -1:
    ser.close()

#**********************************************************************************

def RoboPiInit(device, bps):
  global ser

  if device == '':
    device = '/dev/ttyAMA0'

  ser = serial.Serial(device,bps)

  if ser == -1:
    print "Error - Unable to open ", device
    exit(1)

  return ser

#**********************************************************************************

def Address(n):
  global myaddr
  myaddr = n & 255

#**********************************************************************************

def getProductID(): # max 255 bytes plus 0, TESTED OK
  putPacket(GETINFO, bytearray(1), 1)
  buff = getPacket()
  return buff[3]

#**********************************************************************************

def getAPIRev():
  return API_REVISION

#**********************************************************************************

def pinMode(pin, mode):
  putPacket(WRITEMODE, bytearray([pin, mode]), 2);
  getPacket()

#**********************************************************************************

def readMode(pin):
  putPacket(READMODE, bytearray([pin]), 1)
  buff = getPacket()
  return buff[3][1]

#**********************************************************************************

def digitalWrite(pin, val):
  putPacket(DIGWRITE, bytearray([pin, val]), 2)
  getPacket()

#**********************************************************************************

def digitalRead(pin):
  putPacket(DIGREAD, bytearray([pin]), 1)
  buff = getPacket()
  return buff[3][1]

#**********************************************************************************

def analogRead(pin):
  putPacket(ANREAD, bytearray([pin]), 1)
  buff = getPacket()
  return int(buff[3][1]) | (int(buff[3][2]) << 8)

#**********************************************************************************

def analogReadRaw(pin):
  putPacket(ANREADRAW, bytearray([pin]), 1)
  buff = getPacket()
  return int(buff[3][1]) | (int(buff[3][2]) << 8)

#**********************************************************************************

def analogWrite(pin, val):
  putPacket(ANWRITE, bytearray([pin, val]), 2)
  getPacket()

#**********************************************************************************

def servoWrite(pin, val):
  putPacket(SERVOWRITE, bytearray([pin, val & 255, val >> 8]), 3)
  getPacket()

#**********************************************************************************

def servoRead(pin):
  putPacket(SERVOREAD, bytearray([pin]), 1)
  buff = getPacket()
  return int(buff[3][1]) | (int(buff[3][2]) << 8)

#**********************************************************************************

def readDistance(pin):
  putPacket(READDIST, bytearray([pin]), 1)
  buff = getPacket()
  return int(buff[3][1]) | (int(buff[3][2]) << 8)

#**********************************************************************************

def w2ba(x):
  return bytearray([x & 255, (x >> 8) & 255])

def wl2ba(lst):
  cl = w2ba(lst[0])
  for ix in range(1,len(lst)):
    cl = cl + w2ba(lst[ix])
  return cl

def pba(a):
  for ix in range(0,len(a)):
    print ix,a[ix]

#**********************************************************************************

def pulseGen(pin, dbg, stp, low_period, pls, pulse_list):
  putPacket(PULSEGEN, bytearray([pin,dbg,stp,pls])+w2ba(low_period)+wl2ba(pulse_list),pls+pls+6)
  buff = getPacket()
  return buff[3][0]

#**********************************************************************************

def pulseList(pin, low_period, pulse_list):
  return pulseGen(pin, 33, 33, low_period, len(pulse_list), pulse_list)  
  
#**********************************************************************************

def pulseStop():
  putPacket(PULSESTOP,bytearray([0]),1)
  buff = getPacket()
  return buff[3][0]
