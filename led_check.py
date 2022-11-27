import time, _thread, machine
from machine import Pin

data_pin = Pin(0,Pin.OUT)
clock_pin = Pin(1,Pin.OUT)


def clock_out_bytev2(byte:int):
    
    T = 150

    clock_pin.off()
    
    for i in range(8):

        b = byte & (1<<(7-i))
        data_pin.value(b!=0)
        time.sleep_us(T)
        clock_pin.on()
        time.sleep_us(T)
        clock_pin.off()


    clock_pin.off()
    #data_pin.off()

def intens_bytes(intens):

    prefix = int('11100000', 2)

    return intens & prefix

def set_leds(r,g,b):
 
    # Start int32 all 0
    #clock_out_bytev2(0)
    clock_out_bytev2(0)
    clock_out_bytev2(0)
    clock_out_bytev2(0)
    clock_out_bytev2(0)

    for i in range(24):

        clock_out_bytev2(int('11100001',2))
        clock_out_bytev2(b)
        clock_out_bytev2(g)
        clock_out_bytev2(r)


    # final frame
    clock_out_bytev2(0xff)
    clock_out_bytev2(0xff)
    clock_out_bytev2(0xff)
    clock_out_bytev2(0xff)



N=1
while True:
    print("loop")
    time.sleep(0.5)

    for i in range(N):
        set_leds(200,0,0)
    time.sleep(0.5)

    for i in range(N):
        set_leds(0,200,0)

    time.sleep(0.5)

    for i in range(N):
        set_leds(0,0,200)

    time.sleep(0.5)
    for i in range(N):
        set_leds(100,0,100)
    time.sleep(0.5)
    for i in range(N):
        set_leds(0,100,100)

    time.sleep(0.5)

