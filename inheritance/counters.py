class Counter:                      # implicitly use object as base class
    hierarchy_depth = 1
    counter_base = 0
    def __init__(self,init_value=0):
        assert init_value >= 0,\
            'Counter.__init__ init_value('+str(init_value)+') < 0'
        self._value = init_value
        Counter.counter_base += 1    
    def __str__(self):
        return str(self._value)
    
    def reset(self):
        self._value = 0
        
    def inc(self):
        self._value += 1
        
    def value_of(self):
        return self._value
    
    
    
class Modular_Counter(Counter):     # explicitly use Counter as base class
    hierarchy_depth = Counter.hierarchy_depth + 1
    counter_derived = 0
    def __init__(self,init_value,modulus):
        assert modulus >= 1,\
            'Modular_Counter.__init__ modulus('+str(init_value)+') < 1'
        assert 0 <= init_value < modulus,\
            'Modular_Counter.__init__ init_value('+str(init_value)+') not in [0,'+str(modulus)+')'
        Counter.__init__(self,init_value)
        self._modulus = modulus
        Modular_Counter.counter_derived += 1    
    
    def __str__(self):
        return Counter.__str__(self)+' mod '+str(self._modulus)
        
    def inc(self):
        if self.value_of() == self._modulus - 1:    # Counter.value_of(self)
            self.reset() # or Counter.reset(self)
        else:
            Counter.inc(self)
        
    def modulus_of(self):
        return self._modulus


if __name__ == '__main__':

    import prompt

    c = Counter(0)
    mc = Modular_Counter(0,3)
    
    while True:
        try:
            exec(prompt.for_string('Command'))
        except Exception as report:
            import traceback
            traceback.print_exc()
     
    