import tuct_leds
import time
from machine import Pin

print("hej")
b1 = Pin(3,Pin.PULL_DOWN)
b2 = Pin(2,Pin.PULL_DOWN)

tree = tuct_leds.Tuct(14,1,0)

tree.set_all_leds(200,0,0,1)
tree.update_tree()
time.sleep_ms(500)
start_lights = not b1.value()
tree.set_all_leds(0,0,0,0)
tree.update_tree()

print(start_lights)
