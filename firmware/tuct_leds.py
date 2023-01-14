from machine import Pin
import time
import random
import micropython
import gc


class LedState:

    def __init__(self):
        # default colors
        self._red = 100
        self._green = 0 
        self._blue = 0 
        self._intensity = 5

    def set_rgb(self, rgb: int):
        self._red = self.limit_val(rgb[0],255)
        self._green = self.limit_val(rgb[1],255)
        self._blue = self.limit_val(rgb[2],255)

    def set_intensity(self, i: int):
        self._intensity = self.limit_val(i,32)

    def limit_val(self, x: int, max: int) -> int:
        """
        Bounds x between 0 and max.
        """
        if x > max:
            x = max 
        elif x < 0:
            x = 0
        return x


class TuctLeds:

    def __init__(self, nr_leds: int, clock_pin: int, data_pin: int, *args, **kwargs):
        super().__init__(*args ,**kwargs)
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

    def set_all_leds(self, r: int, g: int, b: int, intensity: int):
        for led in self.leds:
            led.set_intens(intensity)
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


class TuctButtons:

    def __init__(self, button_1_pin, button_2_pin, *args, **kwargs):
        super().__init__(*args ,**kwargs)
        self._b1 = Pin(button_1_pin,Pin.IN,Pin.PULL_DOWN)
        self._b2 = Pin(button_2_pin,Pin.IN,Pin.PULL_DOWN)


    @property
    def b1(self):
        return self._b1

    @property
    def b2(self):
        return self._b2


class Tuct(TuctLeds, TuctButtons):

    def __init__(self, nr_leds: int, clock_pin: int, data_pin: int, button_1_pin: int=2, button_2_pin: int=3):
        super().__init__(nr_leds=nr_leds, 
                         clock_pin=clock_pin,
                         data_pin=data_pin,
                         button_1_pin=button_1_pin,
                         button_2_pin=button_2_pin)
        self._show_number = 0
        self._last_trigg = 0

    @property
    def show_number(self):
        return self._show_number

    @show_number.setter
    def show_number(self, value):
        self._show_number = value

    def run_lightshow(self, lightshow):
        assert self.light_show_dict_valid(lightshow) # Invalid lightshow

        start_int = self._show_number

        to = time.ticks_cpu()*1/1e6

        intens = 1
        tree.set_all_leds(0,0,0,intens)

        tf = lightshow['time'][-1]

        while True:

            t = time.ticks_cpu()*1/1e6 - to

            # user changed lightshow
            if start_int != self._show_number:
                break

            # Reset clock
            if t > tf:
                to = time.ticks_cpu()*1/1e6
                break

            # Interpolate each led's shedule
            for i in range(tree.nr_leds):

                rgb = interp_leds(t,lightshow['time'],lightshow['leds'][i])
                tree.leds[i].set_rgb(rgb)

            tree.update_tree()
            time.sleep_ms(5)

    def light_show_dict_valid(self, light_show: dict):
        ls_valid = True

        nr_time_steps = len(light_show['time'])
        nr_leds_in_ls = len(light_show['leds'])

        ls_valid &= self.nr_leds == nr_leds_in_ls

        for led in light_show['leds']:

            if not ls_valid:
                break

            ls_valid &= len(led) == nr_time_steps

        return ls_valid

    def b1_callback(self):
        now = time.ticks_cpu()*1/1e6
        if now - self._last_trigg > 0.3:
            self._last_trigg = now
            print("b1")
            show_int += 1
            print(self._show_number)


def test_leds1():
    tree = Tuct(14,1,0)

    intes = 1
    while True:

        tree.set_all_leds(200,200,0,1)
        tree.update_tree()
        time.sleep(2)


        for i in range(14):

            tree.set_all_leds(0,0,0,0)

            tree.leds[i].set_intens(intes)
            tree.leds[i].set_rgb((100,10,0))
            tree.update_tree()
            time.sleep_ms(500)

        
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


def interp_leds(t, time_vec, leds:list):
    # Interpolates the color for a single led
    
    assert abs(time_vec[0]) < 0.0001 # Time vec must start at 0

    t0 = 0
    t1 = time_vec[1]

    ind0 = 0

    for i in range(0,len(time_vec)-1):

        if t > time_vec[i]:
            ind0 = i
            t0 = time_vec[i]
            t1 = time_vec[i+1]

    t_delta = t1 - t0 
    k1 = (t - t0)/t_delta
    
    if k1 > 1:
        k1 = 1

    k0 = 1-k1 

    c0 = leds[ind0]
    c1 = leds[ind0+1]

    c_interp = [c0[i]*k0 + c1[i]*k1 for i in range(3)]
    c_interp = [int(c) for c in c_interp]

    return c_interp
        

def test_ls1(tree):

    r = (250,0,0)
    g = (0,250,0)
    b = (0,0,250)

    ls = {
        'time':[0.0,1.0,1.1,2.1,2.2,3.2,3.3],
        'leds':[
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r],
            [r,r,g,g,b,b,r]
            ]
    }

    run_lightshow(tree,ls)

def test_ls2(tree):

    r = (250,0,0)
    g = (0,250,0)
    b = (0,0,250)


    th = 0.8
    td = 0.5
    tvec = []
    t0 = 0.0
    tvec.append(t0)
    for i in range(3):

        tvec.append(t0 + th)
        tvec.append(t0 + th + td)
        t0 += th + td


    #[0.0, 1.0, 1.01, 2.1, 2.11, 3.2, 3.21]
    ls = {
        'time':tvec,
        'leds':[
            [r,r,g,g,b,b,r],#1
            [r,r,g,g,b,b,r],#2
            [b,b,r,r,g,g,b],#2
            [b,b,r,r,g,g,b],#1
            [g,g,b,b,r,r,g],#1
            [g,g,b,b,r,r,g],#2
            [r,r,g,g,b,b,r],#2
            [r,r,g,g,b,b,r],#1
            [b,b,r,r,g,g,b],#1
            [b,b,r,r,g,g,b],#2
            [g,g,b,b,r,r,g],#2
            [g,g,b,b,r,r,g],#1
            [r,r,g,g,b,b,r],#1
            [r,r,g,g,b,b,r]#2
            ]
    }

    run_lightshow(tree,ls)
"""

    # Green and red side
    run_lightshow(tree,ls)

            [r,r,r,r,r,r,r], #1
            [g,g,g,g,g,g,g], #2
            [g,g,g,g,g,g,g], #2
            [r,r,r,r,r,r,r], #1
            [r,r,r,r,r,r,r], #1
            [g,g,g,g,g,g,g], #2
            [g,g,g,g,g,g,g], #2
            [r,r,r,r,r,r,r], #1
            [r,r,r,r,r,r,r], #1
            [g,g,g,g,g,g,g], #2
            [g,g,g,g,g,g,g], #2
            [r,r,r,r,r,r,r], #1
            [r,r,r,r,r,r,r], #1
            [g,g,g,g,g,g,g]  #2
            ]
"""

def cool_ls2(tree):

    r = (250,0,0)
    g = (0,250,0)
    b = (0,0,250)
    
    th = 0.8
    td = 0.1
    tvec = []
    t0 = 0.0
    tvec.append(t0)
    for i in range(3):

        tvec.append(t0 + th)
        tvec.append(t0 + th + td)
        t0 += th + td


    #[0.0, 1.0, 1.01, 2.1, 2.11, 3.2, 3.21]
    ls = {
        'time':tvec,
        'leds':[
            [r,r,g,g,b,b,r],#1
            [r,r,g,g,b,b,r],#2
            [b,b,r,r,g,g,b],#2
            [b,b,r,r,g,g,b],#1
            [g,g,b,b,r,r,g],#1
            [g,g,b,b,r,r,g],#2
            [r,r,g,g,b,b,r],#2
            [r,r,g,g,b,b,r],#1
            [b,b,r,r,g,g,b],#1
            [b,b,r,r,g,g,b],#2
            [g,g,b,b,r,r,g],#2
            [g,g,b,b,r,r,g],#1
            [r,r,g,g,b,b,r],#1
            [r,r,g,g,b,b,r]#2
            ]
    }

    run_lightshow(tree,ls)


def light_main(tree):
    tree.b1.irq(trigger=Pin.IRQ_FALLING, handler=tree.b1_callback)

    gc_ink = 0

    while True:
        gc.collect()
        gc_ink += 1
        if gc_ink > 10:
            print(micropython.mem_info())
            gc_ink = 0

        if tree.show_number > 2:
            tree.show_number = 0
        if tree.show_number == 0:
            test_ls1(tree)
        if tree.show_number == 1:
            test_ls2(tree)
        if tree.show_number == 2:
            cool_ls2(tree)


def main():

    tree = Tuct(14,1,0)
    light_main(tree)

    # Test led thread
    print("eeyo")
    tree = Tuct(14,1,0)
    #christmas1(tree)
    args = [tree]
    #args = (tree)
    _thread.start_new_thread(test_ls2,args)
    while True:
        time.sleep(5)
        print("wazup")


if __name__ == '__main__':
    main()

