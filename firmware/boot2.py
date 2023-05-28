import tuct_leds
import time
from machine import Pin, Timer
from http_server import HttpServer, connect_wifi
import json
import lightshow


b1 = Pin(3,Pin.PULL_DOWN)
b2 = Pin(2,Pin.PULL_DOWN)

tree = tuct_leds.Tuct(14,1,0)

LS = lightshow.LightshowRunner(tree)

def get_callback2():
    print("GET CALLBACK")

    return {"kebab_lvl":13337, "svarv_lvlv":10009009420, "rgb":"fett"}

def post_callback2(obj):
    print("POST CALLBACK")
    print(obj)
    #obj = obj.replace('\n','')
    #print(type(obj))
    obj = json.loads(obj)
    print(type(obj))

    for ri in range(14):
        for ci in range(5):
            LIGHTSHOW['leds'][ri][ci] = obj['leds'][ri][ci]

    return {"status":'glenn'}

def b1_callback(obj):
    global LS 
    LS.switch_ls()

r = (250,0,0)
g = (0,250,0)
b = (0,0,250)

LIGHTSHOW = {
    'time':[0.0,1.0,1.1,2.1,2.2],
    'leds':[
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r],
        [r,r,g,g,r]
        ]
}

def blink_all_leds(r):
    global tree
    
    led_ids = [(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13)]
    rgbs = [(250,0,0),(0,250,0),(0,0,250)]

    r = 0
    for i in range(7):
        LI = led_ids[i]
        tree.set_all_leds(0,0,0,0)
        tree.leds[LI[0]].set_intens(1)
        tree.leds[LI[0]].set_rgb(rgbs[r])
        tree.leds[LI[1]].set_intens(1)
        tree.leds[LI[1]].set_rgb(rgbs[r])
        tree.update_tree()
        time.sleep_ms(50)


blink_all_leds(0)

connect_wifi()

blink_all_leds(1)

server = HttpServer(get_callback2,post_callback2)
server.start_server()

blink_all_leds(2)

def light_tim_callback(e):
    LS.lightshow_step()

tree.set_all_leds(200,0,0,10)

b1.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=b1_callback)

soft_timer = Timer(mode=Timer.PERIODIC, period=90, callback=light_tim_callback)

server._server_thread()
