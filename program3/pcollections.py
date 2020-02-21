# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import re, traceback, keyword


def pnamedtuple(type_name, field_names, mutable=False, defaults={}):
    def show_listing(s):
        for line_number, line_text in enumerate( s.split('\n'),1 ):
            print(f' {line_number: >3} {line_text.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    
    #check that type_name is vaild
    def _is_legal(name):
        if type(name) != str:
            raise SyntaxError("Name is not valid string. Use a charachter followed by any number of alphanumerics, which are not python keywords")
        if name in keyword.kwlist:
            raise SyntaxError("Name is not valid string. Use a charachter followed by any number of alphanumerics, which are not python keywords")
        
        checked_name = re.search(r'^[a-zA-Z]\w*$',name)
        if checked_name == None:
            raise SyntaxError("Name is not valid string. Use a charachter followed by any number of alphanumerics, which are not python keywords")
        else:
            return(checked_name.group(0))
     
    def _is_legal_list(names):
        if type(names) == str:
            checked_names = re.split(r'[, ]+',names)
            for checked_name in checked_names:
                #group 1 in a match
                _is_legal(checked_name)
            return checked_names
        elif type(names) == list:
            for name in names:
                cn = re.search(r'^[a-zA-Z]\w*$',name)
                if cn == None:
                    raise SyntaxError("Name is not valid string. Use a charachter followed by any number of alphanumerics, which are not python keywords")
            return names
        else:
            raise SyntaxError("Name is not valid string. Use a charachter followed by any number of alphanumerics, which are not python keywords")

        
    
    class_name = _is_legal(type_name)
    class_fields = _is_legal_list(field_names)
        
        
    #begin building class string    
    class_definition = f'''class {class_name}:
    _fields = {class_fields}
    _mutable = {mutable}
    
    '''
    #INIT
    class_init = 'def __init__(self, {}):\n'.format(', '.join([f if f not in defaults.keys() else f'{f}={defaults[f]}' for f in class_fields]))
    for f in class_fields:
        class_init += f'        self.{f} = {f}\n'
    class_definition += class_init + '\n'
    
    #REPR
    arg_str = ','.join([f'{f}={{{f}}}' for f in class_fields])
    f_str = ','.join([f'{f}=self.{f}' for f in class_fields])
    class_repr=f"    def __repr__(self):\n        return '{class_name}({arg_str})'.format({f_str})\n\n"
    class_definition += class_repr
    
    #Simple Query
    for f in class_fields:
        class_definition += f'''    def get_{f}(self):
        return self.{f}
\n'''
    #GET ITEM
    class_definition += f'''    def __getitem__(self,arg):
        indexes = {class_fields} 
        if type(arg) == int and arg in range(len(indexes)):
            cmd = f'self.get_{{indexes[arg]}}()'
            return eval(cmd)
        elif type(arg) == str and arg in indexes:
            cmd = f'self.get_{{arg}}()'
            return eval(cmd)
        else:
            raise IndexError('Argument is not a feild or is out of range')
\n'''

    #equals
    class_definition += f'''    def __eq__(self,right):
        if type(self) !=  type(right):
            return False
            
        if self.__dict__ != right.__dict__:
            return False
            
        return True
\n'''

    #_asdict
    class_definition += f'''    def _asdict(self):
        return dict(self.__dict__)
\n'''
 
    #_make
    class_definition += f'''    def _make(iterable):
        args = ','.join([str(x) for x in iterable])
        cmd = f'{class_name}({{args}})'
        return eval(cmd)
\n'''

    #_replace
    class_definition += f'''    def _replace(self,**kargs):
        for arg in kargs:
            if arg not in {class_fields}:
                raise TypeError("_replace arguments must match keyword arguments of class.")
    
    
        if self._mutable:
            for arg,val in kargs.items():
                self.__dict__[arg] = val
        else:
            class_list = []
            for key in {class_fields}:
                if key in kargs:
                    class_list.append(kargs[key])
                else:
                    class_list.append(self.__dict__[key])
            return {class_name}._make(class_list)
\n'''
    
    
    
    # When debugging, uncomment following line to show source code for the class
    #show_listing(class_definition)
    
    # Execute this class_definition, a str, in a local name space; then bind the
    #   the source_code attribute to class_definition; after try/except return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )    
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):        
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test pnamedtuple below in script with Point = pnamedtuple('Point','x,y')
    Point = pnamedtuple('Point','x,y')
    #driver tests
    import driver
    driver.default_file_name = 'bscp3F19.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
