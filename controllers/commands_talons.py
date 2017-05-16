# python web2py.py -c server.crt -k server.key -a 'Engineering1!' -i 0.0.0.0 -p 8000
# Kirwin's vi tab preferences: set shiftwidth=2 softtabstop=2 expandtab
import xml.etree.ElementTree as ET
import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

######################
## Motor Establishment
######################

freq = 3000
motorL = 0
RPL.pinMode(motorL,RPL.PWM)
RPL.pwmWrite(motorL,1500,freq)
motorR = 1
RPL.pinMode(motorR,RPL.PWM)
RPL.pwmWrite(motorR,1500,freq)

def read_parameters_as_xml():
  parser = ET.ElementTree() # use .get('param')
  return parser.parse('command_parameters.txt')

################
## Web Functions
################

def dashboard():
  response.veiw = 'commands/dashboard.html'
  xml_params = read_parameters_as_xml() 
  return dict(forward=URL('receive'),update_parameters=URL('update_parameters'),motorL_forward=xml_params.get('motorL_forward'),motorL_backward=xml_params.get('motorL_backward'),motorR_forward=xml_params.get('motorR_forward'),motorR_backward=xml_params.get('motorR_backward'))

def update_parameters():
  commands = ET.Element('commands') # Create an xml object
  for command in ['motorL_forward','motorL_backward','motorR_forward','motorR_backward']: # write all parameters to the xml object
    commands.set(command, request.vars[command])
  ET.ElementTree(commands).write('command_parameters.txt')
  redirect(URL('dashboard'))

def receive():
  try:
    command_dictionary[int(request.vars['key'])](request.vars['command'])
  except:
    pass
  else:
    pass

######################
## Individual commands
######################

def forward(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,int(xml_params.get('motorL_forward')), freq)
    RPL.pwmWrite(motorR,int(xml_params.get('motorR_forward')), freq)
  else:
    RPL.pwmWrite(motorL,1500, freq)
    RPL.pwmWrite(motorR,1500, freq)

def reverse(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,int(xml_params.get('motorL_backward')), freq)
    RPL.pwmWrite(motorR,int(xml_params.get('motorR_backward')), freq)
  else:
    RPL.pwmWrite(motorL,1500, freq)
    RPL.pwmWrite(motorR,1500, freq)

def right(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,int(xml_params.get('motorL_forward')), freq)
    RPL.pwmWrite(motorR,int(xml_params.get('motorR_backward')), freq)
  else:
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,1500,freq)

def left(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,int(xml_params.get('motorL_backward')),freq)
    RPL.pwmWrite(motorR,int(xml_params.get('motorR_forward')),freq)
  else:
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,1500,freq)

def forward_right(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,int(xml_params.get('motorL_forward')),freq)
    RPL.pwmWrite(motorR,1500,freq)
  else:
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,1500,freq)

def forward_left(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,int(xml_params.get('motorR_forward')),freq)
  else:
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,1500,freq)

def backward_right(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,int(xml_params.get('motorR_backward')),freq)
  else:
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,1500,freq)

def backward_left(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.pwmWrite(motorL,int(xml_params.get('motorL_backward')),freq)
    RPL.pwmWrite(motorR,1500,freq)
  else:
    RPL.pwmWrite(motorL,1500,freq)
    RPL.pwmWrite(motorR,1500,freq)

command_dictionary = dict([(87,forward),(83,reverse),(68,right),(65,left),(69,forward_right),(81,forward_left),(67,backward_right),(90,backward_left)])
# 87:w, 83:s, 68:d, 65:a, 69:e, 81:q, 90:z, 67:c
# Each entry in this dictionary of the format (number, command_name) references the commands in the Individual commands section. The commands will get either 'go' or 'stop' from the receive function at the top of this document.
# The numeric keys are the letters returned from javascript. You can view key presses by opening the javascript console in the web browser.
