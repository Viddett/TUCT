
from machine import Pin
import time

class LedState:

    def __init__(self):
        # default colors
        self._red = 100
        self._green = 0
        self._blue = 0
        self._intens = 5

    def set_rgb(self,rgb):
        self._red = self.limit_val(rgb[0],255)
        self._green = self.limit_val(rgb[1],255)
        self._blue = self.limit_val(rgb[2],255)

    def set_intens(self,i):
        self._intens = self.limit_val(i,32)

    def limit_val(self,x,max):
        if x > max:
            x = max
        return x


class Tree:

    def __init__(self,nr_leds: int,clock_pin,data_pin,b1_pin=3,b2_pin=2):
        self.clock_T_us = 15
        self.nr_leds = nr_leds

        self.b1 = Pin(b1_pin,Pin.PULL_DOWN)
        self.b2 = Pin(b2_pin,Pin.PULL_DOWN)

        self.data_pin = Pin(data_pin,Pin.OUT)
        self.clock_pin = Pin(clock_pin,Pin.OUT)

        self.leds = [LedState() for i in range(nr_leds)]

    def clock_out_bytev2(self,byte:int):
        self.clock_pin.off()

        for i in range(8):

            b = byte & (1<<(7-i))
            self.data_pin.value(b!=0)
            time.sleep_us(self.clock_T_us)
            self.clock_pin.on()
            time.sleep_us(self.clock_T_us)
            self.clock_pin.off()

        self.clock_pin.off()

    def set_all_leds(self,r,g,b,inte):
        for led in self.leds:
            led.set_intens(inte)
            led.set_rgb((r,g,b))

    def update_tree(self):

        # First empty frame
        self.clock_out_bytev2(0)
        self.clock_out_bytev2(0)
        self.clock_out_bytev2(0)
        self.clock_out_bytev2(0)

        for led in self.leds:
            intens_int = led._intens | int('11100000', 2)
            self.clock_out_bytev2(intens_int)
            self.clock_out_bytev2(led._blue)
            self.clock_out_bytev2(led._green)
            self.clock_out_bytev2(led._red)

        # final frame
        self.clock_out_bytev2(0xff)
        self.clock_out_bytev2(0xff)
        self.clock_out_bytev2(0xff)
        self.clock_out_bytev2(0xff)
