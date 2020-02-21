from goody import irange
from goody import type_as_str

import math

class Fraction:
    @staticmethod
    # Call as Fraction._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    def _gcd(x : int, y : int) -> int:
        assert x >= 0 and y >= 0, 'Fraction._gcd: x('+str(x)+') and y('+str(y)+') must be >= 0'
        while y != 0:
            x, y = y, x % y
        return x

    # Returns a string that is the decimal representation of a Fraction, with
    #   decimal_places digits appearing after the decimal points.
    # For example: if x = Fraction(23,8), then x(5) returns '2.75000'
    def __call__(self, decimal_places):
        answer = ''
        num = self.num
        denom = self.denom
    
        # handle negative values
        if num < 0:
            num, answer = -num, '-'
    
        # handle integer part
        if num >= denom:
            answer += str(num//denom)
            num     = num - num//denom*denom
            
        # handle decimal part
        answer += '.'+str(num*10**decimal_places//denom)
        return answer
    
    @staticmethod
    # Call as Fraction._validate_arithmetic(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Fraction or int is...
    # Fraction._validate_arithmetic(right, {Fraction,int},'+','Fraction',type_as_str(right))
    def _validate_arithmetic(v, t : set, op : str, lt : str, rt : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+lt+'\' and \''+rt+'\'')        

    @staticmethod
    # Call as Fraction._validate_relational(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v, t : set, op : str, rt : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Fraction() '+op+' '+rt+'()')        


    def __init__(self,num=0,denom=1):
        assert type(num)   is int, 'Fraction.__init__ numerator is not int: '+str(num)
        assert type(denom) is int, 'Fraction.__init__ denominator is not int: '+str(denom)
        assert denom != 0,'Fraction.__init__ denominator is 0'
        if denom < 0:
            num, denom = -num, -denom
        if num == 0:
            denom = 1
        gcd = Fraction._gcd(abs(num), denom)
        self.num = num // gcd
        self.denom = denom // gcd
        

    def __repr__(self):
        return 'Fraction('+str(self.num)+','+str(self.denom)+')'
    
    def __str__(self):
        return str(self.num)+'/'+str(self.denom)
   

    def __bool__(self):
        return self.num != 0
    

    def __getitem__(self,i):
        if i == 0 or i == 1:
            return self.num if i == 0 else self.denom
        if i == '':
            raise TypeError('Fraction.__getitem: index('+str(i)+') not, 0, 1 or (non-empty) prefix')
        if 'numerator'.find(str(i)) == 0:
            return self.num
        elif 'denominator'.find(str(i)) == 0:
            return self.denom
        else:
            raise TypeError('Fraction.__getitem: index('+str(i)+') not, 0, 1 or prefix')
    
 
    def __pos__(self):
        return Fraction(self.num,self.denom)
    
    def __neg__(self):
        return Fraction(-self.num,self.denom)
    
    def __abs__(self):
        return Fraction(abs(self.num),self.denom)
    

    def __add__(self,right):
        Fraction._validate_arithmetic(right, [Fraction,int],'+','Fraction',type_as_str(right))
        if type(right) is int:
            right = Fraction(right)
        return Fraction(self.num*right.denom+right.num*self.denom,self.denom*right.denom)
    
    def __radd__(self,left):
        Fraction._validate_arithmetic(left, [Fraction,int],'+',type_as_str(left),'Fraction')
        return self + left

    def __sub__(self,right):
        Fraction._validate_arithmetic(right, [Fraction,int],'-','Fraction',type_as_str(right))
        return self + -right
     
    def __rsub__(self,left):
        Fraction._validate_arithmetic(left, [Fraction,int],'-',type_as_str(left),'Fraction')
        return left + -self 
     
    def __mul__(self,right):
        Fraction._validate_arithmetic(right, [Fraction,int],'*','Fraction',type_as_str(right))
        if type(right) is int:
            right = Fraction(right)
        return Fraction(self.num*right.num,self.denom*right.denom)

    def __rmul__(self,left):
        Fraction._validate_arithmetic(left, [Fraction,int],'*',type_as_str(left),'Fraction')
        return self * left
    
    def __truediv__(self,right):
        Fraction._validate_arithmetic(right, [Fraction,int],'/','Fraction',type_as_str(right))
        if type(right) is int:
            right = Fraction(right)
        return Fraction(self.num*right.denom,self.denom*right.num)
 
    def __rtruediv__(self,left):
        Fraction._validate_arithmetic(left, [Fraction,int],'/',type_as_str(left),'Fraction')
        if type(left) is int:
            left = Fraction(left)
        return left / self

    def __pow__(self,right):
        Fraction._validate_arithmetic(right, [int],'**','Fraction',type_as_str(right))
        if right >= 0:
            return Fraction(self.num**right,self.denom**right)
        else:
            return Fraction(self.denom**-right,self.num**-right)

    def __eq__(self,right):
        Fraction._validate_relational(right,[Fraction,int],'==',type_as_str(right))
        if type(right) is int:
            right = Fraction(right)
        return self.num==right.num and self.denom==right.denom
    
    
    def __lt__(self,right):
        Fraction._validate_relational(right,[Fraction,int],'<',type_as_str(right))
        if type(right) is int:
            right = Fraction(right)
        return self.num*right.denom < right.num*self.denom

    
    def __gt__(self,right):
        Fraction._validate_relational(right,[Fraction,int],'>',type_as_str(right))
        if type(right) is int:
            right = Fraction(right)
        return right < self

    
    def __setattr__(self,name,value):
        if name in self.__dict__:
            raise NameError('Fraction is immutable; attempted to change instance variable: '+name)
        self.__dict__[name] = value
 


# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer
    
    answer = Fraction(1,2)
    x      = Fraction(1,2)
    for i in irange(1,n):
        big = 2*i+1
        answer += Fraction(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer





if __name__ == '__main__':
    # Put in simple tests for Fraction before allowing driver to run
    
 
    print()
    import driver
    
    driver.default_file_name = 'bscq31F19.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
