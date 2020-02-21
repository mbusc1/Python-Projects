# Wormhole acts lieka black hole but instead of destroying an object it moves it, it does this 
# by editing the simulton instead of returning it to be destroyed.
# It also can teleport any simulton type. to any random point on the canvas

from simulton import Simulton
from random import random
import model



class Special(Simulton):
    def __init__(self,x,y):
        self._width = 5
        self._height = 5
        self._color = '#ff3399'
        self._radius = 15
        self.set_location(x,y)
    
    def update(self):
        checks = model.find(lambda ob: self.contains(ob.get_location()))
        for ch in checks:
            if not isinstance(ch, Special):
                ch.set_location(random()*model.world()[0],random()*model.world()[1])
            
        
    
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-self._radius      ,self.get_location()[1]-self._radius,
                                self.get_location()[0]+self._radius, self.get_location()[1]+self._radius,
                                fill=self._color)
        
    def contains(self,xy):
        if self.distance(xy) < self._radius:
            return True
        else:
            return False
