
from machine import Pin
import time
import _thread
import random

class LedState:

    def __init__(self):
        # default colors
        self._red = 100
        self._green = 0 
        self._blue = 0 
        self._intens = 5

    def set_rgb(self,rgb):
        self._red = self.limit_val(rgb[0],255)
        self._green = self.limit_val(rgb[1],255)
        self._blue = self.limit_val(rgb[2],255)

    def set_intens(self,i):
        self._intens = self.limit_val(i,32)

    def limit_val(self,x,max):
        if x > max:
            x = max 
        return x



class Tuct:

    def __init__(self,nr_leds,clock_pin,data_pin):
        self.clock_T_us = 15
        self.nr_leds = nr_leds
        
        self.data_pin = Pin(data_pin,Pin.OUT)
        self.clock_pin = Pin(clock_pin,Pin.OUT)

        self.leds = [LedState() for i in range(nr_leds)]


    def clock_out_bytev2(self,byte:int):
        self.clock_pin.off()
        
        for i in range(8):

            b = byte & (1<<(7-i))
            self.data_pin.value(b!=0)
            time.sleep_us(self.clock_T_us)
            self.clock_pin.on()
            time.sleep_us(self.clock_T_us)
            self.clock_pin.off()


        self.clock_pin.off()

    def set_all_leds(self,r,g,b,inte):
        for led in self.leds:
            led.set_intens(inte)
            led.set_rgb((r,g,b))

    def update_tree(self):

        # First empty frame
        self.clock_out_bytev2(0)
        self.clock_out_bytev2(0)
        self.clock_out_bytev2(0)
        self.clock_out_bytev2(0)

        for led in self.leds:
            intens_int = led._intens | int('11100000', 2)
            self.clock_out_bytev2(intens_int)
            self.clock_out_bytev2(led._blue)
            self.clock_out_bytev2(led._green)
            self.clock_out_bytev2(led._red)

        # final frame
        self.clock_out_bytev2(0xff)
        self.clock_out_bytev2(0xff)
        self.clock_out_bytev2(0xff)
        self.clock_out_bytev2(0xff)



def test_leds1():
    tree = Tuct(12,1,0)

    intes = 1
    while True:
        intes += 1

        if intes > 15:
            intes = 0
        for i in range(12):

            tree.set_all_leds(0,0,0,0)

            tree.leds[i].set_intens(intes)
            tree.leds[i].set_rgb((100,10,0))
            tree.update_tree()
            time.sleep_ms(10)

        
def christmas1(tree:Tuct):

    intens = 1

    odd_leds = [1,3,4,6,9,10]

    step = 0

    odd_colors = [(100,0,0),(0,100,0)]
    even_colors = [(0,100,0),(100,0,0)]
    
    tree.set_all_leds(0,0,0,intens)

    while True:
        if step >= len(odd_colors):
            step = 0

        for i,led in enumerate(tree.leds):
            if i in odd_leds:
                r,g,b = odd_colors[step]
                led.set_rgb((r,g,b))
            else:
                r,g,b = even_colors[step]
                led.set_rgb((r,g,b))

        tree.update_tree()
        time.sleep_ms(1000)

        step += 1
            

def gen_random_color():
    r = random.randrange(0,255)
    g = random.randrange(0,255)
    b = random.randrange(0,255)
    return (r,g,b)


def christmas2(tree:Tuct):


    red = (250,0,0)
    green = (0,250,0)
    blue =(0,0,250)
    purple = (250,0,250)
    yellow = (0,250,250)

    colors = [red,green,blue,purple,yellow]
    colors = [red,green,blue]

    t_tr_s = 0.2
    t_hold_s = 2.0

    intens = 1
    
    tree.set_all_leds(0,0,0,intens)
    N = tree.nr_leds

    old_colors = [random.choice(colors) for i in range(N)]
    next_colors = [random.choice(colors) for i in range(N)]

    to = time.ticks_cpu()

    while True:
        ti_s = (time.ticks_cpu() - to)*1/1e6
        
        if ti_s > t_hold_s + t_tr_s:
            # pick new colors 
            to = time.ticks_cpu()
            print("new colors")
            old_colors = next_colors
            next_colors = [random.choice(colors) for i in range(N)]
        
        elif ti_s < t_tr_s:
            # interpolate between colors for each led
            
            k0 = (time.ticks_cpu() - to)/(t_tr_s*1e6)
            k1 = 1 - k0
            for i in range(N):

                old = old_colors[i]
                nex = next_colors[i]
                
                inter_color = [k1*old[j] + k0*nex[j] for j in range(3)]
                inter_color = [int(ic) for ic in inter_color]
                tree.leds[i].set_rgb(inter_color)
        else:            
            for i in range(N):

                tree.leds[i].set_rgb(next_colors[i])
            
        tree.update_tree()
        time.sleep_ms(10)








def main():
    # Test led thread
    print("eeyo")
    tree = Tuct(12,1,0)
    args = [tree]
    #args = (tree)
    _thread.start_new_thread(christmas2,args)
    while True:
        time.sleep(1)
        print("wazup")


if __name__ == '__main__':
    main()

