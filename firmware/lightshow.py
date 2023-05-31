
import time
import tuct_leds


class LightshowRunner:

    self.tree:tuct_leds.Tree

    def __init__(self,tree:tuct_leds.Tree):
        self.tree = tree
        self.ls_nr = 0

        self.t0 = self._get_tick()

        self.custom_ls = {    
            'time':[0.0,1.0,2.0],
            'leds':[
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED],
                [RED,GREEN,RED]
                ]}

    
    def _get_tick(self):
        return time.ticks_cpu()*1/1e6



    def lightshow_step(self):
        current_lightshow = self.get_current_ls()
        
        t = self._get_tick() - self.t0 

        # If internal clock has overflow:n
        if t < 0 or t >= current_lightshow['time'][-1]:
            self.t0 = self._get_tick()
            t = 0

            # Interpolate each led's shedule
        for i in range(self.tree.nr_leds):

            rgb = self._interp_leds(t,current_lightshow['time'],current_lightshow['leds'][i])
            self.tree.leds[i].set_rgb(rgb)

        self.tree.update_tree()

    def switch_ls(self):
        if self.ls_nr >= 4:
            self.ls_nr = 0
        else:
            self.ls_nr += 1  
        
        self.t0 = self._get_tick()

    def get_current_ls(self):

        if self.ls_nr == 0:
            return LS0
        elif self.ls_nr == 1:
            return LS1 
        elif self.ls_nr == 2:
            return LS2
        elif self.ls_nr == 3:
            return LS3
        elif self.ls_nr == 4:
            return self.custom_ls
        else:
            return {}

    def get_custom_ls(self):
        return self.custom_ls 

    def set_custom_ls(self, ls):
        ls_ok = self.light_show_dict_valid(ls)
        if ls_ok:
            self.custom_ls = ls 
            self.ls_nr = 4
        return ls_ok 

    def light_show_dict_valid(self,ls:dict):

        ls_valid = True

        nr_time_steps = len(ls['time'])
        nr_leds_in_ls = len(ls['leds'])

        ls_valid &= self.tree.nr_leds == nr_leds_in_ls

        for i in range(len(ls['leds'])):

            if not ls_valid:
                break

            led_i = ls['leds'][i]
            ls_valid &= len(led_i) == nr_time_steps

        return ls_valid

    def _interp_leds(self,t, time_vec, leds:list):
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




RED = (250,0,0)
GREEN = (0,250,0)
BLUE = (0,0,250)
PURPLE = (250,0,250)
YELLOW = (0,250,250)

LS0 = {
'time':[0.0,1.0,1.1,2.1,2.2],
'leds':[
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED],
    [RED,RED,GREEN,GREEN,RED]
    ]
}

LS1 = {
    'time':[0.0,1.0,1.1,2.1,2.2,3.2,3.3],
    'leds':[
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED]
        ]
}

LS2 =  {
    'time':[0.0, 1.0, 1.01, 2.1, 2.11, 3.2, 3.21],
    'leds':[
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#1
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#2
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#2
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#1
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#1
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#2
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#2
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#1
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#1
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#2
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#2
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#1
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#1
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED]#2
        ]
}

LS3 = {
    'time':[0.0, 1.0, 1.01, 2.1, 2.11, 3.2, 3.21],
    'leds':[
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#1
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#2
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#2
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#1
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#1
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#2
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#2
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#1
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#1
        [BLUE,BLUE,RED,RED,GREEN,GREEN,BLUE],#2
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#2
        [GREEN,GREEN,BLUE,BLUE,RED,RED,GREEN],#1
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED],#1
        [RED,RED,GREEN,GREEN,BLUE,BLUE,RED]#2
        ]
}


