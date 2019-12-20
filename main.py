"""
   written by Mitch Zakocs from CircuitSpecialists.com
   licensed as GPLv3
"""

import network
import ntptime
import utime
import time
import machine
import esp
import gc
import uos
# import schedule
import smart_control
import nanoWebSrv
from sys import platform
gc.collect()

class WiFi:
        # This simply sets up the Wi-Fi. The else section in the initialization definition simply sets up
        # an access point if there is no credentials file so you can set up the Wi-Fi ssid and password.
    def __init__(self, ssid=None, password=None, type='AP'):
        if(type != 'AP'):
            self.wlan = network.WLAN(network.STA_IF)    # create station interface
            self.wlan.active(True)                      # activate the interface
            self.wlan.scan()                            # scan for access points
            self.wlan.isconnected()                     # check if the station is connected to an AP
            self.wlan.connect(ssid, password)           # connect to an AP
            self.wlan.config('mac')          
            self.wlan.ifconfig()
            time.sleep(5)                        # get the interface's MAC adddress
        else:
            self.ap = network.WLAN(network.AP_IF)       # create access-point interface
            self.ap.config(essid='CS Smart Outlet')     # set the ESSID of the access point
            self.ap.config(authmode=network.AUTH_WPA_WPA2_PSK)
            self.ap.config(password="circuit1234")
            self.ap.active(True)                        # activate the interface

    def feed(self):
        self._counter = 0

    def init(self, timeout=None):
        timeout = timeout or self._timeout
        self._timeout = timeout
        self._timer.init(period=int(self._timeout * 1000), mode=machine.Timer.PERIODIC, callback=self._wdt)

    def deinit(self):  # will not stop coroutine
        self._timer.deinit()

class INPUT:
    # This is the input class. This handles all of the reading of the text files created from the nanoWebSrv library
    # and stores them into variables for use by the various other classes.
    def __init__(self):
        self.files = uos.listdir()
        if("creds.txt" in self.files):
            self.getCreds()
        if("schedule.txt" in self.files):
            self.getTimes()
            self.scheduleExists = True
        else:
            self.scheduleExists = False
    def getCreds(self):
        f = open("creds.txt", "r")
        self.SSID = str(f.readline()).strip()
        self.password = str(f.readline()).strip()
        f.close()
    def getTimes(self):
        f = open("schedule.txt", "r")
        self.mondayV = str(f.readline()).strip('\n')
        self.mondayON = str(f.readline()).strip('\n')
        self.mondayOFF = str(f.readline()).strip('\n')
        self.tuesdayV = str(f.readline()).strip('\n')
        self.tuesdayON = str(f.readline()).strip('\n')
        self.tuesdayOFF = str(f.readline()).strip('\n')
        self.wednesdayV = str(f.readline()).strip('\n')
        self.wednesdayON = str(f.readline()).strip('\n')
        self.wednesdayOFF = str(f.readline()).strip('\n')
        self.thursdayV = str(f.readline()).strip('\n')
        self.thursdayON = str(f.readline()).strip('\n')
        self.thursdayOFF = str(f.readline()).strip('\n')
        self.fridayV = str(f.readline()).strip('\n')
        self.fridayON = str(f.readline()).strip('\n')
        self.fridayOFF = str(f.readline()).strip('\n')
        self.saturdayV = str(f.readline()).strip('\n')
        self.saturdayON = str(f.readline()).strip('\n')
        self.saturdayOFF = str(f.readline()).strip('\n')
        self.sundayV = str(f.readline()).strip('\n')
        self.sundayON = str(f.readline()).strip('\n')
        self.sundayOFF = str(f.readline()).strip('\n')
        f.close()

class TIME:
    # This class handles all of the time-based scheduling functionality of the smart outlet. It can update the time of the RTC,
    # which it does every 15 minutes, and it also checks to see if it's currently the correct time to turn the relay
    # on or off based on the scheduled times.
    def updateTime(self, firstbypass=False):
        if utime.localtime()[4]%15==0 or firstbypass == True: #Checks if its been 15 minutes
            try:
                ntptime.settime()
                print("Current Time:" + str(utime.localtime()))
            except Exception as e:
                print(e)
            time.sleep(0.5)
    def checkCorrectTime(self, t, firstbypass=False):
        if t[5]%20 == 0 or firstbypass == True: #Check if it's the correct time every 20 seconds
            print("Checking Time.... " + str(t))
            #Monday
            if t[6] == 0: #Checks the weekday to see if it matches
                if text_handler.mondayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.mondayOFF.split(":")[0])>=t[3]>=int(text_handler.mondayON.split(":")[0]) and int(text_handler.mondayOFF.split(":")[1])>=t[4]>=int(text_handler.mondayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.mondayV == '2'or text_handler.mondayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()   

            #Tuesday    
            if t[6] == 1: #Checks the weekday to see if it matches
                if text_handler.tuesdayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.tuesdayOFF.split(":")[0])>=t[3]>=int(text_handler.tuesdayON.split(":")[0]) and int(text_handler.tuesdayOFF.split(":")[1])>=t[4]>=int(text_handler.tuesdayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.tuesdayV == '2' or text_handler.tuesdayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON() 

            #Wednesday  
            if t[6] == 2: #Checks the weekday to see if it matches
                if text_handler.wednesdayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.wednesdayOFF.split(":")[0])>=t[3]>=int(text_handler.wednesdayON.split(":")[0]) and int(text_handler.wednesdayOFF.split(":")[1])>=t[4]>=int(text_handler.wednesdayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.wednesdayV == '2' or text_handler.wednesdayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()  

            #Thursday 
            if t[6] == 3: #Checks the weekday to see if it matches
                if text_handler.thursdayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.thursdayOFF.split(":")[0])>=t[3]>=int(text_handler.thursdayON.split(":")[0]) and int(text_handler.thursdayOFF.split(":")[1])>=t[4]>=int(text_handler.thursdayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.thursdayV == '2' or text_handler.thursdayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()

            #Friday   
            if t[6] == 4: #Checks the weekday to see if it matches
                if text_handler.fridayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.fridayOFF.split(":")[0])>=t[3]>=int(text_handler.fridayON.split(":")[0]) and int(text_handler.fridayOFF.split(":")[1])>=t[4]>=int(text_handler.fridayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.fridayV == '2' or text_handler.fridayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()   

            #Saturday        
            if t[6] == 5: #Checks the weekday to see if it matches
                if text_handler.saturdayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.saturdayOFF.split(":")[0])>=t[3]>=int(text_handler.saturdayON.split(":")[0]) and int(text_handler.saturdayOFF.split(":")[1])>=t[4]>=int(text_handler.saturdayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.saturdayV == '2' or text_handler.saturdayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()  

            #Sunday
            if t[6] == 6: #Checks the weekday to see if it matches
                if text_handler.sundayV == '3': #Checks if it's set to use custom values
                    if int(text_handler.sundayOFF.split(":")[0])>=t[3]>=int(text_handler.sundayON.split(":")[0]) and int(text_handler.sundayOFF.split(":")[1])>=t[4]>=int(text_handler.sundayON.split(":")[1]): #Checks if the time should be on and turns it on if it should be
                        controller.turnON()
                        utime.localtime()
                    else: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.sundayV == '2' or text_handler.sundayV == '0': #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()    

if __name__ == "__main__":
    #Wifi Setup
    try:
        text_handler = INPUT()
        wifi = WiFi(ssid=text_handler.SSID, password=text_handler.password, type='client')
    except Exception as e:
        wifi = WiFi()
        print(e)
        print("Creating Access Point...")

    #Setup webserver, time, WatchDog system and relay controller classes
    try:
        timeSchedule = TIME()
        controller = smart_control.CONTROLLER()
        httpserv = nanoWebSrv.NANOWEBSRV()
    except Exception as e:
        print(e)

    #Clear the terminal, update the time for the first time and print the IP address
    try:
        #Clears Console
        print("\x1B\x5B2J", end="")
        print("\x1B\x5BH", end="")
        timeSchedule.updateTime(firstbypass=True)
        if(text_handler.scheduleExists == True):
            timeSchedule.checkCorrectTime(utime.localtime(), firstbypass=True)
        print('Connected On: ' + str(wifi.wlan.ifconfig()[0]))
    except Exception as e:
        print(e)

    #Main execution loop
    try:
        while True:
            timeSchedule.updateTime()
            if(text_handler.scheduleExists == True):
                timeSchedule.checkCorrectTime(utime.localtime())
            httpserv.socketListener()
    except Exception as e:
        print(e)