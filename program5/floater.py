# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


#from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


class Floater(Prey): 
    def __init__(self,x,y):
        self._width = 5
        self._height = 5
        self._color = '#ff0000'
        self._radius = 5
        
        self.randomize_angle()
        self.set_speed(5)
        self.set_location(x,y)
    
    def update(self):
        
        option = random()
        if option > 0.3:
            pass
        else:
            #set new random angle
            self.set_angle(self.get_angle() + random()-0.5)
            #set new speed
            newspeed = random()-0.5
            if self.get_speed() + newspeed < 7 and self.get_speed() + newspeed > 3:
                self.set_speed(self.get_speed() + newspeed)
            else:
                self.set_speed(self.get_speed() - newspeed)
            
        self.move()
        self.wall_bounce()
    
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-self._radius      ,self.get_location()[1]-self._radius,
                                self.get_location()[0]+self._radius, self.get_location()[1]+self._radius,
                                fill=self._color)
