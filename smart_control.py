"""
   written by Mitch Zakocs from Ordertech.com
   licensed as GPLv3
  commands:
    A00100A10D0A opens relay
    A00101A20D0A closes relay
"""

from machine import UART


class CONTROLLER:
    def __init__(self):
        #print("Booting Controller")
        self.uart = UART(1, 9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self.on = bytearray('A00101A20D0A')
        self.off = bytearray('A00100A10D0A')

    def turnON(self):
        self.uart.write(self.on)

    def turnOFF(self):
        self.uart.write(self.off)



