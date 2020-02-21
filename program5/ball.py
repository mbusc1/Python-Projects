# A Ball is Prey; it updates by moving in a straight
#   line and displays as blue circle with a radius
#   of 5 (width/height 10).
from prey import Prey

class Ball(Prey): 
    def __init__(self,x,y):
        self._width = 5
        self._height = 5
        self._color = '#000099'
        self._radius = 5
        
        self.randomize_angle()
        self.set_speed(5)
        self.set_location(x,y)
    
    def update(self):
        self.move()
        self.wall_bounce()
    
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0]-self._radius      ,self.get_location()[1]-self._radius,
                                self.get_location()[0]+self._radius, self.get_location()[1]+self._radius,
                                fill=self._color)
    
