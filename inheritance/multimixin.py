class PrivacyError(Exception):
    pass # inherit __init__/constructor
        

class Privacy:
    def __setattr__(self,attr_name,new_value):
        if attr_name in self.__dict__ and attr_name in self.privates:
            raise PrivacyError('Privacy: attempt to set private: '+
                               attr_name+' to '+str(new_value))
        else:
            self.__dict__[attr_name] = new_value


class Str_All_Attributes:
    def __str__(self):
        from goody import type_as_str
        answer = 'Instance of ' +type_as_str(self)+'\n'
        for a in sorted(self.__dict__):
            answer += '  ' + a + ' -> ' + str(self.__dict__[a]) + '\n'
        return answer


class Test(Privacy,Str_All_Attributes):
    privates = {'y',} # y attribute of Test1 objects cannot be changed

    def __init__(self,x,y):
        self.x = x  
        self.y = y
        
t = Test(0,1)
print(isinstance(t,Str_All_Attributes))
print(t)
t.x = 'changed'
t.y = 'changed'

import prompt

while True:
    try:
        exec(prompt.for_string('Command'))
    except Exception as report:
        import traceback
        traceback.print_exc()
