# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming


class Bag:
    def __init__(self,it=[]):
        self.dict = {}
        for item in it:
            if item not in self.dict.keys():
                self.dict[item] = 1
            else:
                self.dict[item] += 1
        
    def __repr__(self):
        baglist = []
        for k,v in self.dict.items():
            for _ in range(v):
                baglist.append(k)
                
        return "Bag({})".format(str(baglist))
    
    def __str__(self):
        ret = ""
        for k,v in self.dict.items():
            ret += str(k)+"["+str(v)+"],"
            
        return "Bag("+ ret[:-1] +")"
    
    def __len__(self):
        count = 0
        for v in self.dict.values():
            count += v
            
        return count
    
    def unique(self):
        return len(self.dict.keys())
    
    def add(self,value):
        if value in self.dict.keys():
            self.dict[value] += 1
        else:
            self.dict[value] = 1
            
    
    def __contains__(self,arg):
        return arg in self.dict.keys()
    
    
    def count(self,arg):
        if arg in self.dict.keys():
            return self.dict[arg]
        else:
            return 0
        
        
    def __add__(self,right):
        if type(right) != Bag: raise TypeError('bags must be added with bags, use .add() to add value')
        newBag = Bag()
        for b in (self,right):
            for k,v in b.dict.items():
                if k in newBag.dict.keys():
                    newBag.dict[k] += v
                else:
                    newBag.dict[k] = v
        return newBag
    
    
    def __radd__(self,left):
        return Bag.__add__(self,left)
    
    def remove(self,arg):
        if arg not in self.dict.keys(): raise ValueError('could not find {} in bag'.format(arg))
        self.dict[arg] -= 1
        if self.dict[arg] <= 0: del self.dict[arg]
        pass
    
    def __eq__(self,other):
        if type(other) != Bag: return False
        return self.dict == other.dict
    
    def __ne__(self,other):
        if type(other) != Bag: return True
        return self.dict != other.dict
    
    def __iter__(self):
        def gen(contents):
            for k,v in contents.items():
                for _ in range(v):
                    yield k
        return gen(dict(self.dict))
        
        
if __name__ == '__main__':
    #Put your own test code here to test Bag before doing bsc tests

    print('Start simple testing')
    import driver
    driver.default_file_name = 'bscp21F19.txt'
#     driver.default_show_exception =True
#     driver.default_show_exception_message =True
#     driver.default_show_traceback =True
    driver.driver()
