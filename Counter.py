from tkinter import *
from tkinter import font  
import serial
import sys
import glob
import time

currTransmitter = ""
startFlag = False
count = 0
byte = 0
ComPort = ""
currCount = 0

# hard coded; use a map in the future
Counter1ID = "b\'\\x00\'b\'\\x00\'b\'8\'b\'g\'"
Counter2ID = "b\'\\x00\'b\'\\x00\'b\'6\'b\'\\xf7\'"
Counter3ID = "b\'\\x00\'b\'\\x00\'b\'6\'b\'}\'"

def run():
    global startFlag
    global count
    global byte
    global Counter1ID
    global Counter2ID
    global Counter3ID
    global currTransmitter
    global currCount
    
    byte = Receiver.read(1)
    
    if byte == b'S':
        count = 0
        startFlag = True
        currTransmitter = ""

    if startFlag == True:
        count += 1

    if count == 12:
        count = 0
        startFlag = False
        
    elif count > 4 and count < 9:
        currTransmitter += str(byte)    
        
    elif count == 9:
        if currTransmitter == Counter1ID or currTransmitter == Counter2ID or currTransmitter == Counter3ID:
            if byte == b'\x00':
                currCount += 1
                DoorStatLabel.configure(text = str(currCount) + " love Airy")
                DoorStatLabel.update_idletasks()


    root.after(1, run)       

root = Tk()  
root.title("Counter")

Receiver = serial.Serial('com5', 57600, timeout = 0.002)

DoorStatLabel = Label(root, text = str(currCount) + " love Airy", font = (None, 150))
DoorStatLabel.grid(row = 0, column = 1)

OneLabel = Label(root, text = "25 came for free drinks", font = (None, 65))
OneLabel.grid(row = 1, column = 1)

TwoLabel = Label(root, text = "15 hate the pineapple on pizza", font = (None, 40))
TwoLabel.grid(row = 2, column = 1)

ThreeLabel = Label(root, text = "1 team thought of Battery-less sensors", font = (None, 25))
ThreeLabel.grid(row = 3, column = 1)

##ComPorts = Listbox(root, width=20, height=6)
##ComPorts.grid(row=3, column=1)
##
##if sys.platform.startswith('win'):
##    ports = ['COM%s' % (i + 1) for i in range(256)]
##elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
##    # this excludes your current terminal "/dev/tty"
##    ports = glob.glob('/dev/tty[A-Za-z]*')
##elif sys.platform.startswith('darwin'):
##    ports = glob.glob('/dev/tty.*')
##else:
##    raise EnvironmentError('Unsupported platform')
##
##
##for port in ports:
##    try:
##        s = serial.Serial(port)
##        s.close()
##        ComPorts.insert(END, port)
##    except (OSError, serial.SerialException):
##        pass

run()
root.mainloop()
