from goody import irange
from goody import type_as_str

import math

class Fraction:
    # Call as Fraction._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    @staticmethod
    def _gcd(x : int, y : int) -> int:
        assert x >= 0 and y >= 0, 'Fraction._gcd: x('+str(x)+') and y('+str(y)+') must be >= 0'
        while y != 0:
            x, y = y, x % y
        return x

    # Returns a string that is the decimal representation of a Fraction, with
    #   decimal_places digitst appearing after the decimal points.
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
    # Call as Fraction._validate_arithmetic(..); with no self parameter
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
    # Call as Fraction._validate_relational(..); with no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v, t : set, op : str, rt : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Fraction() '+op+' '+rt+'()')        


    def __init__(self,num=0,denom=1):
        #check for 0
        if num == 0 and denom != 1:
            self.num = num
            self.denom = 1
            return None
        
        if denom == 0:
            raise AssertionError('Cannot divide by 0 for a fraction')
        
        # verify input data type is integer
        if (type(num) is not int) or (type(denom) is not int):
            raise AssertionError('Arguments must be 1-2 integers')
            return None
        
        #verify postivie numerator
        if denom > 0 and num < 0:
            gcd = self._gcd(-num,denom)
            self.num = int(num/gcd)
            self.denom = int(denom/gcd)
            return None
        if denom < 0 and num < 0:
            num = -num
            denom = -denom
            gcd = self._gcd(num,denom)
            self.num = int(num/gcd)
            self.denom = int(denom/gcd)
            return None
        #fix negative denom
        if num > 0 and denom < 0:
            num = -num
            denom = -denom
            gcd = self._gcd(-num,denom)
            self.num = int(num/gcd)
            self.denom = int(denom/gcd)
            return None
        
        # assign regular variables            
        gcd = self._gcd(num,denom)
        self.num = int(num/gcd)
        self.denom = int(denom/gcd)
        return None 

    def __repr__(self):
        return 'Fraction('+str(self.num)+','+str(self.denom)+')'
    
    def __str__(self):
        return str(self.num)+'/'+str(self.denom)
   

    def __bool__(self):
        if self.num == 0 and self.denom == 1:
            return False
        else:
            return True
    

    def __getitem__(self,i):
        if type(i) is int:
            if i == 0:
                return self.num
            elif i == 1:
                return self.denom
            else:
                raise TypeError('Indavild index integer')
        elif type(i) is  str:
            if i == '':
                raise TypeError('Index must be a number or non-empty string representing numerator or denominator')

            elif str.find(i,'numerator'[0:len(i)]) >= 0:
                return self.num
            elif str.find(i,'denominator'[0:len(i)]) >= 0:
                return self.denom
            else:
                raise TypeError('Indavild index string')
        else:
            raise TypeError('Index must be a number or non-empty string representing numerator or denominator')
    
 
    def __pos__(self):
        return Fraction(self.num,self.denom)

    
    def __neg__(self):
        return Fraction(-self.num,self.denom)
        
    def __abs__(self):
        return Fraction(abs(self.num),(self.denom))
    

    def __add__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'+','Fraction',type_as_str(right))
        if type(right) is int:
            return Fraction(self.num+(right*self.denom),self.denom)
        if type(right) is Fraction:
            gcd = min(self.denom,right.denom)
            return Fraction(self.num*right.denom+right.num*self.denom,int((self.denom*right.denom+right.denom*self.denom)/ gcd))

    def __radd__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'+','Fraction',type_as_str(left))
        if type(left) is int:
            return Fraction(self.num+(left*self.denom),self.denom)
        if type(left) is Fraction:
            gcd = min(self.denom,left.denom)
            return Fraction(self.num*left.denom+left.num*self.denom,int((self.denom*left.denom+left.denom*self.denom)/ gcd))


    def __sub__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'-','Fraction',type_as_str(right))
        if type(right) is int:
            return Fraction(self.num-(right*self.denom),self.denom)
        if type(right) is Fraction:
            gcd = min(self.denom,right.denom)
            return Fraction(self.num*right.denom-right.num*self.denom,int((self.denom*right.denom+right.denom*self.denom)/ gcd))
     
    def __rsub__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'-','Fraction',type_as_str(left))
        if type(left) is int:
            return Fraction(-self.num+(left*self.denom),self.denom)
        if type(left) is Fraction:
            gcd = min(self.denom,left.denom)
            return Fraction(-self.num*left.denom+left.num*self.denom,int((self.denom*left.denom+left.denom*self.denom)/ gcd))

     
    def __mul__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'*','Fraction',type_as_str(right))
        if type(right) is Fraction:
            return Fraction(self.num*right.num,self.denom*right.denom)
        elif type(right) is int:
            return Fraction(self.num*right,self.denom)


    def __rmul__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'*','Fraction',type_as_str(left))
        if type(left) is Fraction:
            return Fraction(self.num*left.num,self.denom*left.denom)
        elif type(left) is int:
            return Fraction(self.num*left,self.denom)

    
    def __truediv__(self,right):
        pass

    def __rtruediv__(self,left):
        pass


    def __pow__(self,right):
        pass


    def __eq__(self,right):
        pass
    

    def __lt__(self,right):
        pass

    
    def __gt__(self,right):
        pass

    # Uncomment this method when you are ready to write/test it
    # If this is pass, then no attributes will be set!
    #def __setattr__(self,name,value):
    #    pass
 


##############################


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
        big    = 2*i+1
        answer += Fraction(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer





if __name__ == '__main__':
    # Put in simple tests for Fraction before allowing driver to run
 
    print()
    import driver
    
    driver.default_file_name = 'bscq31F19.txt'
#     driver.default_show_traceback= True
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
    driver.driver()
