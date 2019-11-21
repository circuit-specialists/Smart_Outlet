"""
   written by Mitch Zakocs from CircuitSpecialists.com
   licensed as GPLv3
  commands:
    A00101A2 closes relay (On)
    A00100A1 opens relay (Off)
"""

from machine import UART
import ubinascii


class CONTROLLER:
    def __init__(self):
        #print("Booting Controller")
        self.uart = UART(0, 9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)

    def turnON(self):
        self.uart.write(ubinascii.unhexlify('A00101A2'))


    def turnOFF(self):
        self.uart.write(ubinascii.unhexlify('A00100A1'))
        #\x0D\x0A


