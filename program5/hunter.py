# Hunter is doubly-derived from the Mobile_Simulton and Pulsator classes:
#   updating/displaying like its Pulsator base, but also moving (either in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2
import model

starvation = 30

class Hunter(Pulsator, Mobile_Simulton):
    def __init__(self,x,y):
        self._width = 5
        self._height = 5
        self._color = '#000000'
        self._radius = 10
        
        self.set_location(x,y)
        self.set_speed(5)
        self.randomize_angle()
    
    def update(self):
        #New Movement
        seeks = model.find(lambda ob: self.distance(ob.get_location()) < 200)
        #print(seeks)
        min = 200,None
        for sim in seeks:
            if self.distance(sim.get_location()) < min[0] and isinstance(sim, Prey):
                min = self.distance(sim.get_location()),sim
        
        if min != (200,None):
            seek = min[1]
            self.set_angle(atan2(seek.get_location()[1]-self.get_location()[1],seek.get_location()[0]-self.get_location()[0]))
        self.move()
        self.wall_bounce()  
            
        global starvation
        checks = model.find(lambda ob: self.contains(ob.get_location()))
        destroys = set()
        foundPrey = False
        for ch in checks:
            if isinstance(ch, Prey):
                destroys.add(ch)
                foundPrey = True
        
        #pulsator code
        global starvation
        checks = model.find(lambda ob: self.contains(ob.get_location()))
        destroys = set()
        foundPrey = False
        for ch in checks:
            if isinstance(ch, Prey):
                destroys.add(ch)
                foundPrey = True
        #print(destroys)
        starvation -= 1
        #check if shrunk
        if starvation == 0:
            self._radius -= 0.5
            starvation = 30
        #check if dead
        if self._radius == 0:
            return({self})
        
        if foundPrey:
            starvation = 30
            self._radius += 0.5
            #print('returned')
            return destroys