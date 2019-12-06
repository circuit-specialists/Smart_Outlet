"""
   written by Mitch Zakocs from CircuitSpecialists.com
   licensed as GPLv3
"""

import network
import esp

norepl = False

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


class NTP:
    def __init__(self):
        self.rtc = RTC()
        # set a specific date and time
        self.rtc.datetime((2019, 8, 23, 1, 12, 48, 0, 0))
        self.rtc.datetime()  # get date and time

        # synchronize with ntp
        # need to be connected to wifi
        import ntptime
        ntptime.settime()  # set the rtc datetime from the remote server
        self.rtc.datetime()    # get the date and time in UTC


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
        from machine import RTC
        rtc = NTP()
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
            try:
                httpd.socketListener()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)