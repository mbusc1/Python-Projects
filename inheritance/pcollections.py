class pdefaultdict(dict):
    def __init__(self,default_factory=None,initial_dict=[],**kargs):
        dict.__init__(self,initial_dict,**kargs)  # use to initialize base-class
        self._default_factory = default_factory   # use in overridden methods
        
    def __repr__(self):
        return 'pdefaultdict('+str(self._default_factory)+','+dict.__repr__(self)+')'

    # When accessing d[key] the inherited method __getitem__ is
    #   called; if it finds key is not in the dictionary, it calls
    #   self.__missing__(key), returns the result of executing this
    #   method, which uses default_factory, if present, to create a
    #   value assocaited with d[key] and return that value
    def __missing__(self,key):
        if self.default_factory == None:
            raise KeyError(str(key))
        result    = self._default_factory()
        self[key] = result
        return result
  
if __name__ == '__main__':  
    import prompt 
#     uncomment code below for a simple test of defaultdict  
    d = pdefaultdict(int,[('a',1)],b=2)   
    d['a'] += 1
    d['b'] += 1
    d['c'] += 1
    print(d)

    # general driver
    while True:
        try:
            exec(prompt.for_string('Command'))
        except Exception as report:
            import traceback
            traceback.print_exc()