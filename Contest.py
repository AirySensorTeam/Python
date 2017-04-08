from tkinter import *
from tkinter import font
from ubidots import ApiClient
import serial
import sys
import glob
import time

startFlag = False
count = 0
byte = 0
currTransmitter = ""
PortOpen = 0
Receiver = 0

# hard coded; use a map in the future
DoorID = "b\'\\x00\'b\'\\x00\'b\')\'b\'\\xd3\'"

WindowID = "b\'\\x00\'b\'\\x00\'b\')\'b\'\\xd4\'"

DrawerID = "b\'\\x00\'b\'\\x00\'b\')\'b\'\\xcc\'"

# UbiDots variable ID
DoorVar = '58dc37997625427defdcbfa9'
WindowVar = '58dc37a07625427df23bd747'
DrawerVar = '58dc37a77625427df0a47061'

DoorAPI =  ""
WindowAPI = ""
DrawerAPI = ""

def run():
    global startFlag
    global count
    global byte
    global currTransmitter
    global DoorID
    global WindowID
    global DrawerID

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
        if (currTransmitter == DoorID):
            if byte == b'\x00':
                DoorAPI.save_value({'value': 1, 'context': {"status": "Closed", "time": time.ctime()}})
##                DoorStatLabel.configure(image=DoorClosing)
##                DoorStatLabel.update_idletasks()
##                time.sleep(0.7)
                DoorStatLabel.configure(image=DoorClose)
            elif byte == b'\x01':
                DoorAPI.save_value({'value': 0, 'context': {"status": "Opened", "time": time.ctime()}})
##                DoorStatLabel.configure(image=DoorOpening)
##                DoorStatLabel.update_idletasks()
##                time.sleep(0.7)
                DoorStatLabel.configure(image=DoorOpen)

        elif (currTransmitter == WindowID):
            if byte == b'\x00':
                WindowAPI.save_value({'value': 1, 'context': {"status": "Closed", "time": time.ctime()}})
##                    WindowStatLabel.configure(image=WindowClosing)
##                    WindowStatLabel.update_idletasks()
##                    time.sleep(0.7)
                WindowStatLabel.configure(image=WindowClose)
            elif byte == b'\x01':
                WindowAPI.save_value({'value': 0, 'context': {"status": "Opened", "time": time.ctime()}})
##                    WindowStatLabel.configure(image=WindowOpening)
##                    WindowStatLabel.update_idletasks()
##                    time.sleep(0.7)
                WindowStatLabel.configure(image=WindowOpen)

        elif (currTransmitter == DrawerID):
            if byte == b'\x00':
                DrawerAPI.save_value({'value': 1, 'context': {"status": "Closed", "time": time.ctime()}})
##                    DrawerStatLabel.configure(image=DrawerClosing)
##                    DrawerStatLabel.update_idletasks()
##                    time.sleep(0.7)
                DrawerStatLabel.configure(image=DrawerClose)
            elif byte == b'\x01':
                DrawerAPI.save_value({'value': 0, 'context': {"status": "Opened", "time": time.ctime()}})
##                    DrawerStatLabel.configure(image=DrawerOpening)
##                    DrawerStatLabel.update_idletasks()
##                    time.sleep(0.7)
                DrawerStatLabel.configure(image=DrawerOpen)

    root.after(1, run)       

root = Tk()  
root.title("Hub")

Receiver = serial.Serial('com4', 57600, timeout = 0.002)

DoorOpen = PhotoImage(file='Door_OPEN.gif')
DoorClose = PhotoImage(file='Door_CLOSE.gif')
##DoorOpening = PhotoImage(file='Door_OPENING.gif')
##DoorClosing = PhotoImage(file='Door_CLOSING.gif')

WindowOpen = PhotoImage(file='Window_OPEN.gif')
WindowClose = PhotoImage(file='Window_CLOSE.gif')
##WindowOpening = PhotoImage(file='Window_OPENING.gif')
##WindowClosing = PhotoImage(file='Window_CLOSING.gif')

DrawerOpen = PhotoImage(file='Drawer_OPEN.gif')
DrawerClose = PhotoImage(file='Drawer_CLOSE.gif')
##DrawerOpening = PhotoImage(file='Drawer_OPENING.gif')
##DrawerClosing = PhotoImage(file='Drawer_CLOSING.gif')


DoorStatLabel = Label(root, image=DoorOpen)
DoorStatLabel.grid(row = 0, column = 1)


WindowStatLabel = Label(root, image=WindowOpen)
WindowStatLabel.grid(row = 0, column = 2)


DrawerStatLabel = Label(root, image=DrawerOpen)
DrawerStatLabel.grid(row = 0, column = 3)

##ComPorts = Listbox(root, width=20, height=6)
##ComPorts.grid(row=1, column=2)
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

api = ApiClient(token='xjLVoAJzTws7qwc0b9b8MhIh21ojux')
DoorAPI = api.get_variable(DoorVar)
WindowAPI = api.get_variable(WindowVar)
DrawerAPI = api.get_variable(DrawerVar)
DoorAPI.save_value({'value': 0, 'context': {"status": "Opened", "time": time.ctime()}})
WindowAPI.save_value({'value': 0, 'context': {"status": "Opened", "time": time.ctime()}})
DrawerAPI.save_value({'value': 0, 'context': {"status": "Opened", "time": time.ctime()}})

run()
root.mainloop()
