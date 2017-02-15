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

######################
## Individual commands
######################

def forward(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,1500)
  else:
    RPL.servoWrite(motorL,0)

def reverse(dir):
  if(dir=='go'):
    RPL.servoWrite(motorL,2500)
  else:
    RPL.servoWrite(motorL,0)

command_dictionary = dict([(87,forward),(83,reverse)])
# Each entry in this dictionary of the format (number, command_name) references the commands in the Individual commands section. The commands will get either 'go' or 'stop' from the receive function at the top of this document.
# The numeric keys are the letters returned from javascript. You can view key presses by opening the javascript console in the web browser.
