import lightshow
import tuct_leds
import time
import json

try:
    import uasyncio as asyncio
except:
    import asyncio

from machine import Pin
from http_server import HttpServer, connect_wifi

class Tuct:

    def __init__(self) -> None:
        self.tree = tuct_leds.Tree(14,1,0,3,2)
        self.lightshow = lightshow.LightshowRunner(self.tree)

        self.tree.b1.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.b1_callback)

    def b1_callback(self, other) -> None:
        self.lightshow.switch_ls()

    def blink_all_leds(self, r):

        led_ids = [(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13)]
        rgbs = [(250,0,0),(0,250,0),(0,0,250)]

        # r = 0
        for led_id in led_ids:
            self.tree.set_all_leds(0,0,0,0)
            self.tree.leds[led_id[0]].set_intens(1)
            self.tree.leds[led_id[0]].set_rgb(rgbs[r])
            self.tree.leds[led_id[1]].set_intens(1)
            self.tree.leds[led_id[1]].set_rgb(rgbs[r])
            self.tree.update_tree()
            time.sleep_ms(50)

    def get_callback2(self):
        # SHould not be used...
        print("GET CALLBACK")
        return self.lightshow.get_current_ls()

    def post_callback2(self, obj):
        print("POST CALLBACK")
        obj = json.loads(obj)
        print(obj)
        print(type(obj))

        if obj['request'] == 'return_custom_ls':
            return {'custom_ls':self.lightshow.custom_ls}


        elif obj['request'] == 'set_custom_ls':
            ls_obj = json.loads(obj['lightshow'])
            self.lightshow.set_custom_ls(ls_obj)
            return {'custom_ls_status':'ok'}


        elif obj['request'] == 'search':
            return {'tree':'ok'}

        else:
            return {'status':'bad request'}

    async def run_lightshow(self):
        while True:
            self.lightshow.lightshow_step()
            await asyncio.sleep_ms(20)

    async def main(self):
        self.blink_all_leds(0)

        connect_wifi()

        self.blink_all_leds(1)

        self.server = HttpServer(self.get_callback2, self.post_callback2)
        new_server = await asyncio.start_server(self.server.socket_handler, '0.0.0.0', 80)

        self.blink_all_leds(2)

        self.tree.set_all_leds(200,0,0,10)

        asyncio.create_task(self.run_lightshow())

        while True:
            await asyncio.sleep(10)


if __name__ == '__main__':
    tuct_object = Tuct()
    asyncio.run(tuct_object.main())
