import serial

arduinoSerialData = serial.Serial('com3',9600)

while(1):
    if(arduinoSerialData.inWaiting()>0):
        myData=arduinoSerialData.readline()
        Data=int(myData)
        print (Data)
        #print "aaaaaaaaaaaaa"
