## Welcome

I hope you enjoy working with the BSMRKRS Direct Robot Contol System. The DRCS only allows direct control of motors through a web interface with no autonomy.

The DRCS can be modified in 3 ways:

# Basic Usage

You can add or modify hard-coded outputs to motors in the existing button responses relatively easily. This process has two parts: 

1. If you want to use additional motor outputs, you'll need to initialize them in the Motor Establishment section. For example, if you want to add a new servo motor that runs on pin 5, you would add these lines of code:
> motor_new = 4
> RPL.pinMode(motor_new,RPL.SERVO)

Note that the pin labeled 5 on the RoboPi has to be called 4 in the code. Sigh. The pin labels are 1 indexed on the board, and 0 indexed in the code.

2. In `/controllers/commands.py`, under the section heading Individual Commands, you will find several blocks with this form:
```
def forward(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_forward')))
    RPL.servoWrite(motorR,int(xml_params.get('motorR_forward')))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)
```

This is the code that runs when key assigned to 'forward' (i.e., w) is pressed or released. When w is pressed `forward('go')` is called, and when w is released `forward('stop')` is called. You can change what happens when w is pressed by changing the code under `if(dir=='go'):`. Suppose you want the servo attached to pin 5 to spin at a setting of 1200us when w is pressed, and at 1800us when w is released, you would change to code to look like this:

```
def forward(dir):
  if(dir=='go'):
    xml_params = read_parameters_as_xml() 
    RPL.servoWrite(motorL,int(xml_params.get('motorL_forward')))
    RPL.servoWrite(motorR,int(xml_params.get('motorR_forward')))
    RPL.servoWrite(motor_new,1200))
  else:
    RPL.servoWrite(motorL,0)
    RPL.servoWrite(motorR,0)
    RPL.servoWrite(motor_new,1800))
```

You'll have to manually change the 1200 and 1800 to get the motor to behave they way you want it to.

# Intermediate Usage

You can add or modify outputs to motors that are adjustable on the web page, but still use the same button settings. This process has __ parts:

1. Follow step 1 in the Basic Usage section.

2. You will need to add new form fields on the view page. In `/views/commands/dashboard.html` you will find a block of code that has several elements like this:
```
  <p>L Motor Forward Setting</p>
  <input name="motorL_forward" value={{=motorL_forward}} />
```

They all live between the <form> and </form> tag -- that's important.
