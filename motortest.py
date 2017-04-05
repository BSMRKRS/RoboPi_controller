import RoboPiLib as r
r.RoboPiInit("/dev/serial0",115200)
print r.getProductID()
r.pwmWrite(0,1500,3000)