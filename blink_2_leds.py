from machine import Pin
import time


data_pin = Pin(0,Pin.OUT)
clock_pin = Pin(1,Pin.OUT)



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
        time.sleep_us(100)
        clock_pin.on()
        time.sleep_us(100)
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

    for i in range(12):

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


while True:
    print("writiti")
    set_leds(200,0,0)
    set_leds(200,0,0)
    set_leds(200,0,0)
    time.sleep(1)
    set_leds(200,200,0)
    set_leds(200,200,0)
    set_leds(200,200,0)
    time.sleep(1)

#"""

"""
while True:
    data_pin.on()
    time.sleep(0.5)
    data_pin.off()
    time.sleep(0.5)
    print("debugigigbiigig")
"""
