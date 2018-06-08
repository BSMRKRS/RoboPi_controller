# --------------------------------File on Robot---------------------------------
# Hosts a TCP connection and interprets the data recieved
import sys, os, socket
import stepper_control as arm
from time import sleep

######################
##    Host Info     ##
######################
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
host = '0.0.0.0'
server_address = (host, 10001)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            data = connection.recv(9)
            data = data.split(' ')
            
            # Shoulder Forward
            if int(data[0]) == 1:
                #print "Forward"
                arm.shoulder(1, .05, 500)
             # Shoulder Backward
            if int(data[0]) == 2:
                #print "Backward"
                arm.shoulder(0, .05, 500)
            if int(data[0]) == 3:
                arm.elbow(1, .05, 100)
            if int(data[0]) == 4:
                arm.elbow(0, .05, 100)
    finally:
        connection.close()
