"""
   written by Mitch Zakocs from Ordertech.com
   licensed as GPLv3
  commands:
    0xA00100A1 opens relay
    0xA00101A2 closes relay
"""

from machine import UART


class CONTROLLER:
    def __init__(self):
        print("Booting Controller")
        self.uart = UART(1, 9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)

    def turnON(self):
        self.uart.write('0xA00101A2')

    def turnOff(self):
        self.uart.write('0xA00100A1')



