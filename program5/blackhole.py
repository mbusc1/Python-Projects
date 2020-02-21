# Black_Hole is singly derived from Simulton, updating by finding+removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey
import model



class Black_Hole(Simulton):
    def __init__(self,x,y):
        self._width = 5
        self._height = 5
        self._color = '#000000'
        self._radius = 10
        
        self.set_location(x,y)
    
    def update(self):
        checks = model.find(lambda ob: self.contains(ob.get_location()))
        destroys = set()
        foundPrey = False
        for ch in checks:
            if isinstance(ch, Prey):
                destroys.add(ch)
                foundPrey = True
        #print(destroys)
        if foundPrey:
            #print('returned')
            return destroys
            
        
    
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-self._radius      ,self.get_location()[1]-self._radius,
                                self.get_location()[0]+self._radius, self.get_location()[1]+self._radius,
                                fill=self._color)
        
    def contains(self,xy):
        if self.distance(xy) < self._radius:
            return True
        else:
            return False
