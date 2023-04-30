import tuct_leds
import time
from machine import Pin, Timer
from http_server import HttpServer, connect_wifi
import json


b1 = Pin(3,Pin.PULL_DOWN)
b2 = Pin(2,Pin.PULL_DOWN)

tree = tuct_leds.Tuct(14,1,0)

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


def get_tick():
    return time.ticks_cpu()*1/1e6

TICK_OLD = -1

def lightshow_step(tree):

    global TICK_OLD, LIGHTSHOW

    tf = LIGHTSHOW['time'][-1]


    if TICK_OLD == -1:
        TICK_OLD = get_tick()

    t = get_tick() - TICK_OLD

    # Reset clock
    if t > tf or t < 0:
        TICK_OLD = get_tick()
        t = 0


    # Interpolate each led's shedule
    for i in range(tree.nr_leds):

        rgb = tuct_leds.interp_leds(t,LIGHTSHOW['time'],LIGHTSHOW['leds'][i])
        tree.leds[i].set_rgb(rgb)

    tree.update_tree()




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
connect_wifi()

r=1
for i in range(7):
    LI = led_ids[i]
    tree.set_all_leds(0,0,0,0)
    tree.leds[LI[0]].set_intens(1)
    tree.leds[LI[0]].set_rgb(rgbs[r])
    tree.leds[LI[1]].set_intens(1)
    tree.leds[LI[1]].set_rgb(rgbs[r])
    tree.update_tree()
    time.sleep_ms(50)

server = HttpServer(get_callback2,post_callback2)
server.start_server()

r=2
for i in range(7):
    LI = led_ids[i]
    tree.set_all_leds(0,0,0,0)
    tree.leds[LI[0]].set_intens(1)
    tree.leds[LI[0]].set_rgb(rgbs[r])
    tree.leds[LI[1]].set_intens(1)
    tree.leds[LI[1]].set_rgb(rgbs[r])
    tree.update_tree()
    time.sleep_ms(50)

def light_tim_callback(e):

    #tree.set_all_leds(0,0,0,0)
    lightshow_step(tree)
    #tree.update_tree()

tree.set_all_leds(200,0,0,10)

soft_timer = Timer(mode=Timer.PERIODIC, period=90, callback=light_tim_callback)

server._server_thread()

#if start_lights:
#    tuct_leds.light_main(tree)

