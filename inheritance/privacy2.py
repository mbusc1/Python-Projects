class PrivacyError(Exception):
    pass # inherit __init__/constructor
        

class Privacy:
    def __setattr__(self,attr_name,new_value):
        print('__setattr__:',attr_name,self.privates) # for illustration
        if attr_name in self.__dict__ and attr_name in self.privates:
            raise PrivacyError('Privacy: attempt to set private: '+
                               attr_name+' to '+str(new_value))
        else:
            self.__dict__[attr_name] = new_value


class Test(Privacy):
    privates = {'y',} # y attribute of Test1 objects cannot be changed

    def __init__(self,x,y):
        self.x = x  
        self.y = y

        
t = Test(0,1)
t.x = 'changed'
t.y = 'changed'

import prompt

while True:
    try:
        exec(prompt.for_string('Command'))
    except Exception as report:
        import traceback
        traceback.print_exc()
