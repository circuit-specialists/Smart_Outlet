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

class TIME:
    isupdated = False
    def logToFile(status, time):
        with open('log.txt','w') as file:
            file.write(status)
            file.write(str(time))
        file.close()
    def updateTime(self):
        if utime.localtime()[4]%15==0 and not is_updated: #Checks if its been 15 minutes
            try:
                ntptime.settime()
            except Exception as e:
                print(e)
            isupdated = True
            time.sleep(0.5)
        elif utime.localtime()[3]%15 != 0 and is_updated: #If it hasn't been 15 mins, set to not updated
            isupdated = False
    def checkTime(self):
        if t[3]>=23 or t[3]<7 and led.value() == OFF:
            write_to_file("ON", utime.localtime())
            led.off()
            print("ON")
            utime.localtime()
        elif t[3]>=7 and t[3]<23 and led.value() == ON:
            led.on()
            print("OFF")
            utime.localtime()
            write_to_file("OFF", utime.localtime())


class CREDS:
    def __init__(self):
        import uos
        files = uos.listdir()
        if("creds.txt" in files):
            self.getCreds()
        else:
            if(norepl):
                pass
            else:
                print('No creds stored')

    def getCreds(self):
        f = open("creds.txt", "r")
        self.SSID = str(f.readline()).strip()
        self.password = str(f.readline()).strip()
        f.close()


if __name__ == "__main__":
    try:
        creds_handler = CREDS()
        wifi = WiFi(ssid=creds_handler.SSID, password=creds_handler.password, type='client')
    except Exception as e:
        wifi = WiFi()
        print(e)
        print("Creating Access Point...")

    try:
        timeSchedule = TIME()
        watchDog = WDT()
    except Exception as e:
        print(e)

    try:
        import smart_control
        #controller = smart_control.CONTROLLER()
    except Exception as e:
        print(e)

    try:
        import nanoWebSrv
        httpd = nanoWebSrv.NANOWEBSRV()
        while True:
            httpd.socketListener()
            timeSchedule.checkTime()
            watchDog.feed()
    except Exception as e:
        print(e)