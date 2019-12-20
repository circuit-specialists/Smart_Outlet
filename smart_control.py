"""
   written by Mitch Zakocs from CircuitSpecialists.com
   licensed as GPLv3
  commands:
    A00101A2 closes relay (On)
    A00100A1 opens relay (Off)
"""

from machine import UART
from machine import Pin
import ubinascii

class CONTROLLER:
    # This is the class to control the on/off functionality of the relay
    # Since the ESP8266 has only 1 UART connection, which is used for terminal access through PUTTY,
    # if you have the UART connection being used by the relay you can no longer get access through PUTTY.
    # To fix this, simply set the consoleOutput variable to True and it will disable the relay until turned off again
    # so you can access the terminal of the ESP.
    consoleOutput = False
    def __init__(self):
        if self.consoleOutput == False:
            self.uart = UART(0, 9600)
            self.uart.init(9600, bits=8, parity=None, stop=1)
        self.led = Pin(2, Pin.OUT)
    def turnON(self):
        if self.consoleOutput == False:
            self.uart.write(ubinascii.unhexlify('A00101A2'))
        self.led.on()
    def turnOFF(self):
        if self.consoleOutput == False:
            self.uart.write(ubinascii.unhexlify('A00100A1'))
        self.led.off()

