from machine import Pin
import time

ledPin = Pin("LED", Pin.OUT)

while True:
    time.sleep_ms(1000)
    print("led ON")
    ledPin.value(1)
    time.sleep_ms(1000)
    print("led OFF")
    ledPin.value(0)
