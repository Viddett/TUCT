import tuct_leds
import server_connect
import time 
from machine import Pin

b1 = Pin(3,Pin.PULL_DOWN)
b2 = Pin(2,Pin.PULL_DOWN)

tree = tuct_leds.Tuct(14,1,0)


led_ids = [(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13)]
rgbs = [(250,0,0),(0,250,0),(0,0,250)]
for r in range(3):
    for i in range(7):
        LI = led_ids[i]
        tree.set_all_leds(0,0,0,0)
        tree.leds[LI[0]].set_intens(1)
        tree.leds[LI[0]].set_rgb(rgbs[r])
        tree.leds[LI[1]].set_intens(1)
        tree.leds[LI[1]].set_rgb(rgbs[r])
        tree.update_tree()
        time.sleep_ms(50)

start_lights = not b1.value()
tree.set_all_leds(0,0,0,0)
tree.update_tree()

if start_lights:
    #tuct_leds.light_main(tree)
    server_connect.main()
    

