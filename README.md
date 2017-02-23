## Welcome

I hope you enjoy working with the BSMRKRS Direct Robot Contol System. The DRCS only allows direct control of motors through a web interface with no autonomy.

The DRCS can be modified in 3 ways:

# Basic Usage

You can add or modify hard-coded outputs to motors in the existing button responses relatively easily. This process has two parts: 

1. If you want to use additional motor outputs, you'll need to initialize them in the Motor Establishment section. For example, if you want to add a new servo motor that runs on pin 5, you would add these lines of code:  
```  
motor_new = 4  
RPL.pinMode(motor_new,RPL.SERVO)  
```  
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

You can add or modify outputs to motors that are adjustable on the web page, but still use the same button settings. This process has 5 parts.

1. Follow step 1 in the Basic Usage section.

2. You will need to add new form fields on the view page. In `/views/commands/dashboard.html` you will find a block of code that has several elements like this:  
```  
  <p>L Motor Forward Setting</p>  
  <input name="motorL_forward" value={{=motorL_forward}} />  
```  
They all live between the `<form>` and `</form>` tag -- that's important. The text in the `<p>` section is the label, i.e., the text that shows above the input field. In the `<input>` tag, the text after `name=` -- in this case 'motorL_formard' -- is the name of the variable that will be stored, and can be accessed later by the motors. The variable after `value=` -- in this case {{=motorL_forward}} -- is value given to the web page that will show up in the input field when you view the page. Let's all agree to just give these the same name. You can add a new variable that will be accessible to the motors by duplicating these fields and setting the names.So we could add the following:  
```  
  <p>New Motor Forward Setting</p>  
  <input name="motor_new_forward" value={{=motor_new_forward}} />  
```  
When we hit 'submit' on the dashboard, all of the values from these input fields are written to a file in web2py folder called `command_parameters.txt`.

3. The dashboard needs to have access to the variables that we have input forms for. The `def dashboard()` function in `/controllers/commands.py` prepares information for the dashboard, so that's where this work is done.  
The `/views/commands/dashboard.html` file has access to everything in the dictionary established in the line that looks something like this:  
```  
return dict(forward=URL('receive'),update_parameters=URL('update_parameters'),motorL_forward=xml_params.get('motorL_forward'),motorL_backward=xml_params.get('motorL_backward'),motorR_forward=xml_params.get('motorR_forward'),motorR_backward=xml_params.get('motorR_backward'))  
```  
Each entry in that dictionary is a key=value pair separated by commas that can be called in `/views/commands/dashboard.html` like this: `{{=KEY_NAME}}`. The input fields will need to display the value stored in `command_parameters.txt`, so each key=value pair will look like `KEY_NAME=xml_params.get('VARIABLE_NAME')`. Like with step 2, let's just agree to name these the same things, so in this example, we'd add `,motor_new_forward=xml_params.get('motor_new_forward')` at the end of the list of entries in the dictionary. This will make `{{=motor_new_forward}}` return 2500 in `/views/commands/dashboard.html`.

4. Setting the motor outputs is similar to step 2 in the Basic Usage section. Instead of using numerical values, though, you can call the parameters you set in the view.  
```  
def forward(dir):  
  if(dir=='go'):  
    xml_params = read_parameters_as_xml()   
    RPL.servoWrite(motorL,int(xml_params.get('motorL_forward')))  
    RPL.servoWrite(motorR,int(xml_params.get('motorR_forward')))  
    RPL.servoWrite(motor_new,int(xml_params.get('motor_new_forward')))  
  else:  
    RPL.servoWrite(motorL,0)  
    RPL.servoWrite(motorR,0)  
    RPL.servoWrite(motor_new,0)  
```  
The `read_parameters_as_xml()` function loads the parameters from `command_parameters.txt` and the parameters can be called using the `.get()` command. If we set motor_new_forward using `name="motor_new_forward"` to 2500, then `int(xml_params.get('motor_new_forward'))` will return 2500.

5. Go to the web interface and set your new variables.  
