import lightshow
import tuct_leds
import time
import json
import index

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
        print("GET CALLBACK")
        return self.lightshow.get_current_ls()

    def post_callback2(self, obj):
        print("POST CALLBACK")
        print(obj)
        #obj = obj.replace('\n','')
        #print(type(obj))
        # obj = json.loads(obj)
        if type(obj['leds'][0][0]) == str:
            print('Str objects found...')
            for i in range(len(obj['leds'])):
                for j in range(len(obj['leds'][i])):
                    obj['leds'][i][j]= eval(obj['leds'][i][j])

        success = self.lightshow.set_custom_ls(obj)

        """
        for ri in range(14):
            for ci in range(5):
                LIGHTSHOW['leds'][ri][ci] = obj['leds'][ri][ci]
        """

        if success:
            status = '201 Created'
            response = {"status":'glenn'}
        else:
            status = '400 Bad request'
            response = index.html_bad_request_invalid_lightshow

        return status, response

    async def run_lightshow(self):
        while True:
            self.lightshow.lightshow_step()
            await asyncio.sleep_ms(50)

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