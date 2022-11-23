import time, _thread, machine
from machine import Pin
from smol_webserver import startNet, getLedStatus


data_pin = Pin(0,Pin.OUT)
clock_pin = Pin(1,Pin.OUT)
num_leds = 24


"""
def clock_out_byte(val):
    
    if val > 255:
        print("ERROR IN CLOCK OUT BYTE")
        val = 255

    bits = []
    for i in range(8):
        bi = val % 2 
        val -= bi 
        val /= 2 
        bits.append(bi)
    bits.reverse()
    
    clock_pin.off()
    data_pin.off()

    time.sleep_us(1)

    for b in bits:

        data_pin.value(b)
        clock_pin.on()
        time.sleep_ms(1)
        clock_pin.off()
        time.sleep_ms(1)
    clock_pin.off()
    data_pin.off()
"""

def clock_out_bytev2(byte:int):
    
    clock_pin.off()
    data_pin.off()

    time.sleep_us(100)

    for i in range(8):

        b = byte & (1<<i)

        data_pin.value(b)
        clock_pin.on()
        clock_pin.off()


    clock_pin.off()
    data_pin.off()

def intens_bytes(intens):

    prefix = int('11100000', 2)

    return intens & prefix

def set_leds(r,g,b):
 
    # Start int32 all 0
    clock_out_bytev2(0)
    clock_out_bytev2(0)
    clock_out_bytev2(0)
    clock_out_bytev2(0)

    for i in range(num_leds):

        clock_out_bytev2(int('11100011',2))
        clock_out_bytev2(b)
        clock_out_bytev2(g)
        clock_out_bytev2(r)


    # final frame
    clock_out_bytev2(0xff)
    clock_out_bytev2(0xff)
    clock_out_bytev2(0xff)
    clock_out_bytev2(0xff)

#"""


def ledThread():
    print("started blink")
    time.sleep(1)
    while True:
        r = 0
        g = 0
        if (getLedStatus()):
            g = 100
        else:
            r = 100
    
        set_leds(r,g,0)
        set_leds(r,g,0)
        set_leds(r,g,0)
        time.sleep(0.3)
        set_leds(2*r,2*g,0)
        set_leds(2*r,2*g,0)
        set_leds(2*r,2*g,0)
        time.sleep(0.3)

#"""


"""
while True:
    data_pin.on()
    time.sleep(0.5)
    data_pin.off()
    time.sleep(0.5)
    print("debugigigbiigig")
"""

_thread.start_new_thread(ledThread, ())
startNet()