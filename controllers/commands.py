# python web2py.py -c server.crt -k server.key -a 'Engineering1!' -i 0.0.0.0 -p 8000
# Kirwin's vi tab preferences: set shiftwidth=2 softtabstop=2 expandtab
import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

def dashboard():
  response.veiw = 'commands/dashboard.html'
  return dict(forward=URL('receive'))

def receive():
  try:
    command_dictionary[int(request.vars['key'])](request.vars['command'])
  except:
    pass
  else:
    pass

######################
## Motor Establishment
######################

motorL = 0
RPL.pinMode(motorL,RPL.SERVO)
motorR = 1
RPL.pinMode(motorR,RPL.SERVO)

######################
## Individual commands
######################

def forward(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,1500)
    RPL.servoWrite(motorR,1500)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def reverse(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,2500)
    RPL.servoWrite(motorR,2500)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def right(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,1500)
    RPL.servoWrite(motorR,2500)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def left(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,2500)
    RPL.servoWrite(motorR,1500)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def forward_right(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,1500)
    RPL.servoWrite(motorR,0)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def forward_left(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,1500)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def backward_right(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,2500)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def backward_left(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,2500)
    RPL.servoWrite(motorR,0)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

command_dictionary = dict([(87,forward),(83,reverse),(68,right),(65,left),(69,forward_right),(81,forward_left),(67,backward_right),(90,backward_left)])
# 87:w, 83:s, 68:d, 65:a, 69:e, 81:q, 90:z, 67:c
# Each entry in this dictionary of the format (number, command_name) references the commands in the Individual commands section. The commands will get either 'go' or 'stop' from the receive function at the top of this document.
# The numeric keys are the letters returned from javascript. You can view key presses by opening the javascript console in the web browser.
