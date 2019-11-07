import network
import esp


class WiFi:
    def __init__(self, ssid, password):
        self.wlan = network.WLAN(network.STA_IF)  # create station interface
        self.wlan.active(True)       # activate the interface
        self.wlan.scan()             # scan for access points
        self.wlan.isconnected()      # check if the station is connected to an AP
        self.wlan.connect(ssid, password)  # connect to an AP
        self.wlan.config('mac')      # get the interface's MAC adddress
        self.wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

        self.ap = network.WLAN(network.AP_IF)  # create access-point interface
        self.ap.config(essid='ESP-AP')  # set the ESSID of the access point
        self.ap.active(True)         # activate the interface


class NTP:
    def __init__(self):
        self.rtc = RTC()
        # set a specific date and time
        self.rtc.datetime((2017, 8, 23, 1, 12, 48, 0, 0))
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

    def createCreds(self, ssid, password):
        f = open("creds.txt", "w")
        f.write(str(ssid) + "\n")
        f.write(str(password))
        f.close()
        self.SSID = ssid
        self.password = password

    def getCreds(self):
        f = open("creds.txt", "r")
        self.SSID = str(f.readline()).strip()
        self.password = str(f.readline()).strip()
        f.close()


if __name__ == "__main__":
    print(esp.check_fw())

    try:
        creds_handler = CREDS()
        wifi = WiFi(creds_handler.SSID, creds_handler.password)
    except Exception as e:
        print(e)

    try:
        from machine import RTC
        rtc = NTP()
    except Exception as e:
        print(e)

    try:
        import smart_control
        controller = smart_control.CONTROLLER()
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