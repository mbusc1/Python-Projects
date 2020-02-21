# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole
from prey import Prey
import model

starvation = 30

class Pulsator(Black_Hole): 
    def update(self):
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