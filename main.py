import network

class WiFi:
    def __init__(self, ssid, password):
        wlan = network.WLAN(network.STA_IF) # create station interface
        wlan.active(True)       # activate the interface
        wlan.scan()             # scan for access points
        wlan.isconnected()      # check if the station is connected to an AP
        wlan.connect(ssid, password) # connect to an AP
        wlan.config('mac')      # get the interface's MAC adddress
        wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

        ap = network.WLAN(network.AP_IF) # create access-point interface
        ap.config(essid='ESP-AP') # set the ESSID of the access point
        ap.active(True)         # activate the interface

class NTP:
    def __init__(self):
        rtc = RTC()
        rtc.datetime((2017, 8, 23, 1, 12, 48, 0, 0)) # set a specific date and time
        rtc.datetime() # get date and time

        # synchronize with ntp
        # need to be connected to wifi
        import ntptime
        ntptime.settime() # set the rtc datetime from the remote server
        rtc.datetime()    # get the date and time in UTC

if __name__ == "__main__":
    main = WiFi('circuitspecialists.com', 'C!rCu!t!')
    try:
        from machine import RTC
        NTP()
    except Exception as e:
        print(e)
    try:
        import smart_control
        main = smart_control.CONTROLLER()
    except Exception as e:
        print(e)
