# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:40:39 2019

@author: Philip
"""

import time
from aiy.leds import Leds, Color, Pattern, RgbLeds


def rainbow():
    with Leds() as leds:
        for i in range(16):
            leds.update(Leds.blend(Color.RED,Color.GREEN, i/16))
            time.sleep(0.1)
        for i in range(16):
            leds.update(Leds.blend(Color.BLUE,Color.RED, i/16))
            time.sleep(0.1)
        for i in range(16):
            leds.update(Leds.blend(Color.GREEN,Color.BLUE, i/16))
            time.sleep(0.1)
            
def color(R,G,B):
    c = (R,G,B)
    with Leds() as leds:
        leds.update(Leds.rgb_on(c))
        time.sleep(.1)
#        time.sleep(1)
        
color(255,0,0)