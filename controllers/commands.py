# python web2py.py -c server.crt -k server.key -a 'Engineering1!' -i 0.0.0.0 -p 8000
# Kirwin's vi tab preferences: set shiftwidth=2 softtabstop=2 expandtab
import xml.etree.ElementTree as ET
import RoboPiLib as RPL
import subprocess
RPL.RoboPiInit("/dev/ttyAMA0",115200)

######################
## Motor Establishment
######################

motorL = 0
RPL.pinMode(motorL,RPL.SERVO)
motorR = 1
RPL.pinMode(motorR,RPL.SERVO)

def read_parameters_as_xml():
  parser = ET.ElementTree() # use .get('param')
  return parser.parse('command_parameters.txt')

################
## Web Functions
################

def dashboard():
  response.veiw = 'commands/dashboard.html'
  xml_params = read_parameters_as_xml() 
  return dict(start_camera=URL('start_camera'),forward=URL('receive'),update_parameters=URL('update_parameters'),motorL_forward=xml_params.get('motorL_forward'),motorL_backward=xml_params.get('motorL_backward'),motorR_forward=xml_params.get('motorR_forward'),motorR_backward=xml_params.get('motorR_backward'))

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

def start_camera():
  path = "/usr/src/mjpg-streamer/mjpg-streamer-experimental"
  #call([path+"/mjpg_streamer","&","-o","'"+path+"/output_http.so -w ./www -p 9080'", "-i", "'"+path+"/input_raspicam.so -x 640 -y 480 -fps 10 -rot 180'"],shell=True)
  subprocess.call(["sh","start_camera.sh"])
  print("Done loading camera")
  redirect(URL('dashboard'))
  

######################
## Individual commands
######################

def forward(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_forward')))
    RPL.servoWrite(motorR,int(xml_params.get('motorR_forward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def reverse(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_backward')))
    RPL.servoWrite(motorR,int(xml_params.get('motorR_backward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def right(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_forward')))
    RPL.servoWrite(motorR,int(xml_params.get('motorR_backward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def left(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_backward')))
    RPL.servoWrite(motorR,int(xml_params.get('motorR_forward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def forward_right(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_forward')))
    RPL.servoWrite(motorR,0)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def forward_left(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,int(xml_params.get('motorR_forward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def backward_right(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,int(xml_params.get('motorR_backward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

def backward_left(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_backward')))
    RPL.servoWrite(motorR,0)
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)

command_dictionary = dict([(87,forward),(83,reverse),(68,right),(65,left),(69,forward_right),(81,forward_left),(67,backward_right),(90,backward_left)])
# 87:w, 83:s, 68:d, 65:a, 69:e, 81:q, 90:z, 67:c
# Each entry in this dictionary of the format (number, command_name) references the commands in the Individual commands section. The commands will get either 'go' or 'stop' from the receive function at the top of this document.
# The numeric keys are the letters returned from javascript. You can view key presses by opening the javascript console in the web browser.
