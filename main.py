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
    def __init__(self, ssid=None, password=None, type='AP'):
        if(type != 'AP'):
            self.wlan = network.WLAN(network.STA_IF)    # create station interface
            self.wlan.active(True)                      # activate the interface
            self.wlan.scan()                            # scan for access points
            self.wlan.isconnected()                     # check if the station is connected to an AP
            self.wlan.connect(ssid, password)           # connect to an AP
            self.wlan.config('mac')                     # get the interface's MAC adddress
            self.wlan.ifconfig()                        # get the interface's IP/netmask/gw/DNS addresses
        else:
            self.ap = network.WLAN(network.AP_IF)       # create access-point interface
            self.ap.config(essid='CS Smart Outlet')     # set the ESSID of the access point
            self.ap.config(authmode=network.AUTH_WPA_WPA2_PSK)
            self.ap.config(password="circuit1234")
            self.ap.active(True)                        # activate the interface

class WDT: #Software WatchDog system to reset the board if it shuts off unexpectedly
    def __init__(self, id=0, timeout=120, use_rtc_memory=True): #Thank you kevinkk525 on the MicroPython Forums
        self._timeout = timeout / 10
        self._counter = 0
        self._timer = machine.Timer(id)
        self._use_rtc_memory = use_rtc_memory
        self.init()
        try:
            with open("watchdog.txt", "r") as f:
                if f.read() == "True":
                    print("Reset reason: Watchdog")
        except Exception as e:
            print(e)  # file probably just does not exist
        try:
            with open("watchdog.txt", "w") as f:
                f.write("False")
        except Exception as e:
            print("Error saving to file: {!s}".format(e))
            if use_rtc_memory and platform == "esp8266":
                rtc = machine.RTC()
                if rtc.memory() == b"WDT reset":
                    print("Reset reason: Watchdog")
                rtc.memory(b"")

    def _wdt(self, t):
        self._counter += self._timeout
        if self._counter >= self._timeout * 10:
            try:
                with open("watchdog.txt", "w") as f:
                    f.write("True")
            except Exception as e:
                print("Error saving to file: {!s}".format(e))
                if self._use_rtc_memory and platform == "esp8266":
                    rtc = machine.RTC()
                    rtc.memory(b"WDT reset")
            machine.reset()

    def feed(self):
        self._counter = 0

    def init(self, timeout=None):
        timeout = timeout or self._timeout
        self._timeout = timeout
        self._timer.init(period=int(self._timeout * 1000), mode=machine.Timer.PERIODIC, callback=self._wdt)

    def deinit(self):  # will not stop coroutine
        self._timer.deinit()

class INPUT:
    def __init__(self):
        files = uos.listdir()
        if("creds.txt" in files):
            self.getCreds()
        if("schedule.txt" in files):
            self.getTimes()
        self.convertUseable()
    def getCreds(self):
        f = open("creds.txt", "r")
        self.SSID = str(f.readline()).strip()
        self.password = str(f.readline()).strip()
        f.close()
    def getTimes(self):
        f = open ("schedule.txt")
        self.mondayV = f.readline()
        self.mondayON = str(f.readline()).strip()
        self.mondayOFF = str(f.readline()).strip()
        self.tuesdayV = f.readline()
        self.tuesdayON = str(f.readline()).strip()
        self.tuesdayOFF = str(f.readline()).strip()
        self.wednesdayV = f.readline()
        self.wednesdayON = str(f.readline()).strip()
        self.wednesdayOFF = str(f.readline()).strip()
        self.thursdayV = f.readline()
        self.thursdayON = str(f.readline()).strip()
        self.thursdayOFF = str(f.readline()).strip()
        self.fridayV = f.readline()
        self.fridayON = str(f.readline()).strip()
        self.fridayOFF = str(f.readline()).strip()
        self.saturdayV = f.readline()
        self.saturdayON = str(f.readline()).strip()
        self.saturdayOFF = str(f.readline()).strip()
        self.sundayV = f.readline()
        self.sundayON = str(f.readline()).strip()
        self.sundayOFF = str(f.readline()).strip()
        f.close()
    def convertUseable(self):
        self.mondayONHour = self.mondayON.split(":")[0]
        self.mondayONMinute = self.mondayON.split(":")[1]
        self.mondayOFFHour = self.mondayOFF.split(":")[0]
        self.mondayOFFMinute = self.mondayOFF.split(":")[1]
        self.tuesdayONHour = self.tuesdayON.split(":")[0]
        self.tuesdayONMinute = self.tuesdayON.split(":")[1]
        self.tuesdayOFFHour = self.tuesdayOFF.split(":")[0]
        self.tuesdayOFFMinute = self.tuesdayOFF.split(":")[1]
        self.wednesdayONHour = self.wednesdayON.split(":")[0]
        self.wednesdayONMinute = self.wednesdayON.split(":")[1]
        self.wednesdayOFFHour = self.wednesdayOFF.split(":")[0]
        self.wednesdayOFFMinute = self.wednesdayOFF.split(":")[1]
        self.thursdayONHour = self.thursdayON.split(":")[0]
        self.thursdayONMinute = self.thursdayON.split(":")[1]
        self.thursdayOFFHour = self.thursdayOFF.split(":")[0]
        self.thursdayOFFMinute = self.thursdayOFF.split(":")[1]
        self.fridayONHour = self.fridayON.split(":")[0]
        self.fridayONMinute = self.fridayON.split(":")[1]
        self.fridayOFFHour = self.fridayOFF.split(":")[0]
        self.fridayOFFMinute = self.fridayOFF.split(":")[1]
        self.saturdayONHour = self.saturdayON.split(":")[0]
        self.saturdayONMinute = self.saturdayON.split(":")[1]
        self.saturdayOFFHour = self.saturdayOFF.split(":")[0]
        self.saturdayOFFMinute = self.saturdayOFF.split(":")[1]
        self.sundayONHour = self.sundayON.split(":")[0]
        self.sundayONMinute = self.sundayON.split(":")[1]
        self.sundayOFFHour = self.sundayOFF.split(":")[0]
        self.sundayOFFMinute = self.sundayOFF.split(":")[1]

class TIME:
    def updateTime(self):
        if utime.localtime()[4]%15==0: #Checks if its been 15 minutes
            try:
                ntptime.settime()
            except Exception as e:
                print(e)
            time.sleep(0.5)
    def checkCorrectTime(self, t):
        print("Current Time:" + str(t))
        if t[5]%30 == 0: #Check if it's the correct time  every 30 seconds
            if t[6] == 0: #Checks the weekday to see if it matches
                #Monday
                if text_handler.mondayV == 3: #Checks if it's set to use custom values
                    if t[3]>=text_handler.mondayONHour or t[3]<text_handler.mondayOFFHour: #Checks if the time is after the ON time
                        controller.turnON()
                        utime.localtime()
                    elif t[3]>=text_handler.mondayOFFHour and t[3]<text_handler.mondayONHour: #Checks if the time is after the OFF time
                        controller.turnOFF()
                        utime.localtime()
                elif text_handler.mondayV == 2 or text_handler.mondayV == 0: #Checks if it's set to always off or a blank value
                    controller.turnOFF()    
                else:
                    controller.turnON()   

                #Tuesday
                if t[6] == 0: #Checks the weekday to see if it matches
                    if text_handler.tuesdayV == 3: #Checks if it's set to use custom values
                        if t[3]>=text_handler.tuesdayONHour or t[3]<text_handler.tuesdayOFFHour: #Checks if the time is after the ON time
                            controller.turnON()
                            utime.localtime()
                        elif t[3]>=text_handler.tuesdayOFFHour and t[3]<text_handler.tuesdayONHour: #Checks if the time is after the OFF time
                            controller.turnOFF()
                            utime.localtime()
                    elif text_handler.tuesdayV == 2 or text_handler.tuesdayV == 0: #Checks if it's set to always off or a blank value
                        controller.turnOFF()    
                    else:
                        controller.turnON() 

                #Wednesday  
                if t[6] == 0: #Checks the weekday to see if it matches
                    if text_handler.wednesdayV == 3: #Checks if it's set to use custom values
                        if t[3]>=text_handler.wednesdayONHour or t[3]<text_handler.wednesdayOFFHour: #Checks if the time is after the ON time
                            controller.turnON()
                            utime.localtime()
                        elif t[3]>=text_handler.wednesdayOFFHour and t[3]<text_handler.wednesdayONHour: #Checks if the time is after the OFF time
                            controller.turnOFF()
                            utime.localtime()
                    elif text_handler.wednesdayV == 2 or text_handler.wednesdayV == 0: #Checks if it's set to always off or a blank value
                        controller.turnOFF()    
                    else:
                        controller.turnON()  

                #Thursday 
                if t[6] == 0: #Checks the weekday to see if it matches
                    if text_handler.thursdayV == 3: #Checks if it's set to use custom values
                        if t[3]>=text_handler.thursdayONHour or t[3]<text_handler.thursdayOFFHour: #Checks if the time is after the ON time
                            controller.turnON()
                            utime.localtime()
                        elif t[3]>=text_handler.thursdayOFFHour and t[3]<text_handler.thursdayONHour: #Checks if the time is after the OFF time
                            controller.turnOFF()
                            utime.localtime()
                    elif text_handler.thursdayV == 2 or text_handler.thursdayV == 0: #Checks if it's set to always off or a blank value
                        controller.turnOFF()    
                    else:
                        controller.turnON()

                #Friday   
                if t[6] == 0: #Checks the weekday to see if it matches
                    if text_handler.fridayV == 3: #Checks if it's set to use custom values
                        if t[3]>=text_handler.fridayONHour or t[3]<text_handler.fridayOFFHour: #Checks if the time is after the ON time
                            controller.turnON()
                            utime.localtime()
                        elif t[3]>=text_handler.fridayOFFHour and t[3]<text_handler.fridayONHour: #Checks if the time is after the OFF time
                            controller.turnOFF()
                            utime.localtime()
                    elif text_handler.fridayV == 2 or text_handler.fridayV == 0: #Checks if it's set to always off or a blank value
                        controller.turnOFF()    
                    else:
                        controller.turnON()   

                #Saturday        
                if t[6] == 0: #Checks the weekday to see if it matches
                    if text_handler.saturdayV == 3: #Checks if it's set to use custom values
                        if t[3]>=text_handler.saturdayONHour or t[3]<text_handler.saturdayOFFHour: #Checks if the time is after the ON time
                            controller.turnON()
                            utime.localtime()
                        elif t[3]>=text_handler.saturdayOFFHour and t[3]<text_handler.saturdayONHour: #Checks if the time is after the OFF time
                            controller.turnOFF()
                            utime.localtime()
                    elif text_handler.saturdayV == 2 or text_handler.saturdayV == 0: #Checks if it's set to always off or a blank value
                        controller.turnOFF()    
                    else:
                        controller.turnON()  

                #Sunday
                if t[6] == 0: #Checks the weekday to see if it matches
                    if text_handler.sundayV == 3: #Checks if it's set to use custom values
                        if t[3]>=text_handler.sundayONHour or t[3]<text_handler.sundayOFFHour: #Checks if the time is after the ON time
                            controller.turnON()
                            utime.localtime()
                        elif t[3]>=text_handler.sundayOFFHour and t[3]<text_handler.sundayONHour: #Checks if the time is after the OFF time
                            controller.turnOFF()
                            utime.localtime()
                    elif text_handler.sundayV == 2 or text_handler.sundayV == 0: #Checks if it's set to always off or a blank value
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
        watchDog = WDT()
        controller = smart_control.CONTROLLER()
        httpd = nanoWebSrv.NANOWEBSRV()
    except Exception as e:
        print(e)

    #Main execution loop
    try:
        while True:
            httpd.socketListener()
            timeSchedule.updateTime()
            timeSchedule.checkCorrectTime(utime.localtime())
            watchDog.feed()
            # schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print(e)