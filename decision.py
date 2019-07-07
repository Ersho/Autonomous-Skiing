import numpy as np
import time

from key_dict import key_dict
from get_input import PressKey, ReleaseKey

class Decision(object):
    
    def __init__(self):
    
        self.vel = 0
        self.acc = 0
        
        self.tuck = 0
        self.forward_time = 0
    
    def next_move(self, angle):
 
        if self.tuck == 1:
            self.tuck = 2
            self.enter_tuck_state()
        
        if angle >= -0.2 and angle <= 0.2:
            
            if self.tuck != 2:
                self.accelerate(angle)           
            
            if self.forward_time > 20:
                self.tuck = 1
            self.forward_time += 1 
        else:   
            self.steer(angle)
            
            if self.tuck == 2:
                self.tuck = 0
                self.forward_time = 0
                self.end_tuck_state()
                self.stop()
            
        if self.vel > 5:
            self.stop()
            self.vel -= 2
            self.acc = 0
            
    def steer(self, angle):
        
        if angle > 7:
            self.go_faster_right(angle)
        elif angle < -7:
            self.go_faster_left(angle)
        elif angle > 0.5:
            self.go_right(angle)
        elif angle < -0.5:
            self.go_left(angle)
            
    def accelerate(self, angle):
    
        self.go_forward()
        self.vel += 1
        self.acc += 1
    
    def enter_tuck_state(self):
        self.run_faster()
        
    def end_tuck_state(self):
        self.end_faster()
    
    def go_faster_right(self, angle):
        self.go_right(angle * 2)

    def go_faster_left(self, angle):
        self.go_left(angle * 2)

    def go_right(self, angle):
        PressKey(key_dict['D'])
        time.sleep(angle * 0.03)
        ReleaseKey(key_dict['D'])
        
    def go_left(self, angle):
        PressKey(key_dict['A'])
        time.sleep(np.abs(angle * 0.03))
        ReleaseKey(key_dict['A'])
        
    def go_forward(self):
        PressKey(key_dict['W'])
        time.sleep(0.1)
        ReleaseKey(key_dict['W'])
        
    def stop(self): 
        PressKey(key_dict['S'])
        time.sleep(0.5)
        ReleaseKey(key_dict['S'])
        
    def run_faster(self):
        PressKey(key_dict['LSHIFT'])
        
    def end_faster(self):
        ReleaseKey(key_dict['LSHIFT'])