# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from math import sqrt
from copy import deepcopy

class Interval:
    def __init__(self,minim,maxim):
        self.min = minim
        self.max = maxim
    
    @staticmethod
    def min_max(minim,maxim=None):
        if type(minim) not in (float,int): raise AssertionError('min and max must be float or int')
        if type(maxim) not in (float, int, type(None)): raise AssertionError('min and max must be float or int')
        if maxim == None:
            return Interval(minim,minim)
        if minim > maxim:
            raise AssertionError('min cannot be greater than max')
        return Interval(minim,maxim)

    
    @staticmethod     
    def mid_err(mid,err=0):
        if type(mid) not in (float,int): raise AssertionError('mid must be float or int')
        if type(err) not in (float,int,complex): raise AssertionError('err must be float or int or complex')
        if err < 0:
            raise AssertionError('err cannot be negative')
        return Interval(mid-err,mid+err)

    
    def best(self):
        return (self.max + self.min)/2

    
    def error(self):
        return (self.max - self.min)/2


    def relative_error(self):
        return (self.error()/self.best()) * 100

    
    def __repr__(self):
        return "Interval("+str(self.min)+","+str(self.max)+")"

    
    def __str__(self):
        return str(self.best())+"(+/-"+str(self.error())+")"

    
    def __bool__(self):
        return self.max != self.min

            
    def __pos__(self):
        return self


    def __neg__(self):
        return Interval.min_max(-self.max,-self.min)
    
    
    def __add__(self,other):
        if type(other) not in (int, float, Interval): return NotImplemented
        if type(other) is not Interval: other = Interval.min_max(other)
        return Interval.min_max(self.min + other.min, self.max + other.max)
    
    
    def __radd__(self,other):
        if type(other) not in (int, float, Interval): return NotImplemented
        if type(other) is not Interval: other = Interval.min_max(other)
        return Interval.__add__(self,other)
    
    
    def __sub__(self,right):
        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        right = -right
        return Interval.min_max(self.min + right.min, self.max + right.max)
     
        
    def __rsub__(self,left):
        if type(left) not in (int, float, Interval): return NotImplemented
        if type(left) is not Interval: left = Interval.min_max(left)
        return Interval.__sub__(left,self)
    
    
    def __mul__(self,other):
        if type(other) not in (int, float, Interval): return NotImplemented
        if type(other) is not Interval: other = Interval.min_max(other)
        extr = [self.min * other.min, self.max * other.max, self.min * other.max, self.max * other.min]
        return Interval.min_max(min(extr), max(extr))
    
    
    def __rmul__(self,other):
        if type(other) not in (int, float, Interval): return NotImplemented
        if type(other) is not Interval: other = Interval.min_max(other)
        return Interval.__mul__(self, other)
    
    
    def __truediv__(self,right):
        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        if right.min <= 0 and right.max >= 0: raise ZeroDivisionError
        
        extr = [self.min / right.min, self.max / right.max, self.min / right.max, self.max / right.min]
        return Interval.min_max(min(extr), max(extr))
    
    
    def __rtruediv__(self,left):
        if type(left) not in (int, float, Interval): return NotImplemented
        if type(left) is not Interval: left = Interval.min_max(left)
        return Interval.__truediv__(left,self)
    
    def __pow__(self,right):
        if type(right) is not int: return NotImplemented
        if type(self) is not Interval: return NotImplemented
        new = deepcopy(self)
        if right == 0:
            new = Interval.min_max(1.0)
        elif right > 0:
            for _ in range(right-1):
                new *= self
        else:
            new = Interval.min_max(1.0)
            for _ in range(abs(right)):
                new /= self
        return new
    
    def __eq__(self,right):
        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        return self.max == right.max and self.min == right.min
    
    def __gt__(self,right):
        assert hasattr(self, 'compare_mode') and self.compare_mode in ('liberal','conservative'), 'Error: define compare mode with <Interval>.compare_mode = \'liberal\' , \'conservative\''

        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        
        if self.compare_mode == 'liberal':
            return self.best() > right.best()
        if self.compare_mode == 'conservative':
            return self.min > right.max           

    def __lt__(self,right):
        assert hasattr(Interval, 'compare_mode') and Interval.compare_mode in ('liberal','conservative'), 'Error: define compare mode with Interval.compare_mode = \'liberal\' , \'conservative\''

        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        
        if self.compare_mode == 'liberal':
            return self.best() < right.best()
        if self.compare_mode == 'conservative':
            return self.max < right.min
    
    def __ge__(self,right):
        assert hasattr(self, 'compare_mode') and self.compare_mode in ('liberal','conservative'), 'Error: define compare mode with <Interval>.compare_mode = \'liberal\' , \'conservative\''

        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        
        if self.compare_mode == 'liberal':
            return self.best() >= right.best()
        if self.compare_mode == 'conservative':
            return self.min >= right.max
    
    def __le__(self,right):
        assert hasattr(Interval, 'compare_mode') and Interval.compare_mode in ('liberal','conservative'), 'Error: define compare mode with Interval.compare_mode = \'liberal\' , \'conservative\''

        if type(right) not in (int, float, Interval): return NotImplemented
        if type(right) is not Interval: right = Interval.min_max(right)
        
        if self.compare_mode == 'liberal':
            return self.best() < right.best()
        if self.compare_mode == 'conservative':
            return self.max < right.min

        
    def __abs__(self):
        extr = [abs(self.min), abs(self.max)]
        if self.min <0 and self.max > 0: extr.append(0.0)
        return Interval.min_max(min(extr),max(extr))
    
    
    def sqrt(self):
        extr = [sqrt(self.min), sqrt(self.max)]
        if self.min <0 and self.max > 0: raise ValueError
        return Interval.min_max(min(extr),max(extr))
    
    
if __name__ == '__main__':
    g = Interval.mid_err(9.8,.05)
#     print(repr(g))
#     g = Interval.min_max(9.75,9.85)
#     print(repr(g))
    d = Interval.mid_err(100,1)
#     t = (d/(2*g)).sqrt()
#     print(t,repr(t),t.relative_error())

    import driver    
    driver.default_file_name = 'bscp22F19.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
