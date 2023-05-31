import lightshow
import tuct_leds
import time
import uasyncio
import json

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
        # print(type(obj))
        print(type(obj['leds'][0][0]))
        if type(obj['leds'][0][0]) == str:
            for i in range(len(obj['leds'])):
                for j in range(len(obj['leds'][i])):
                    obj['leds'][i][j]= eval(obj['leds'][i][j])
            # print(type(obj['leds'][0][0]))
            # print(obj)

        self.lightshow.set_custom_ls(obj)

        """
        for ri in range(14):
            for ci in range(5):
                LIGHTSHOW['leds'][ri][ci] = obj['leds'][ri][ci]
        """

        return {"status":'glenn'}
    
    async def run_lightshow(self):
        while True:
            self.lightshow.lightshow_step()
            await uasyncio.sleep_ms(50)

    async def main(self):
        r = (250,0,0)
        g = (0,250,0)
        b = (0,0,250)

        _lightshow = {
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

        self.blink_all_leds(0)

        connect_wifi()

        self.blink_all_leds(1)

        self.server = HttpServer(self.get_callback2, self.post_callback2)
        new_server = await uasyncio.start_server(self.server.socket_handler, '0.0.0.0', 80)

        self.blink_all_leds(2)
        
        self.tree.set_all_leds(200,0,0,10)

        uasyncio.create_task(self.run_lightshow())
        
        while True:
            await uasyncio.sleep(10)

if __name__ == '__main__':

    tuct_object = Tuct()

    uasyncio.run(tuct_object.main())
