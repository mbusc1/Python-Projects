# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming



from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # To begin, by binding the class attribute to True means checking can occur
    #   (but only when self._checking_on is bound to True too)
    checking_on  = True
  
    # For checking the decorated function, bind self._checking_on as True too
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        def check_list_or_tuple(annot,param,value,check_history,t):
            if not isinstance(value, t):
                return AssertionError(f"{param} failed annotation check(wrong type): value = {value}\n was type {type(value)} ...should be type {t}\n{check_history}")
            if len(annot) == 1:
                if isinstance(annot[0],type):
                    for i,v in enumerate(value):
                        if not isinstance(v,annot[0]):
                            return AssertionError(f"{param} failed annotation check(wrong type): value = {value[i]}\n was type {type(value[i])} ...should be type {annot[0]}\n{check_history}")
                else:
                    for val in value:
                        check_history += f'{t}[0] check: {annot}\n'
                        error = Check_Annotation.check(self,param,annot[0],val)
                        if error != None:
                            return error
            else:
                if len(annot) != len(value):
                    return AssertionError(f"{param} failed annotation check(wrong number of elements): value = {value}\n  annotation had {len(annot)} elements{annot}\n{check_history}")

                for i,ann in enumerate(annot):
                    check_history += f'{t}[{i}] check: {annot}\n'
                    error = Check_Annotation.check(self,param,ann,value[i])
                    if error != None:
                        return error
            return
        
        
        def check_dict(annot,param,value,check_history,t):
            if not isinstance(value, t):
                return AssertionError(f"{param} failed annotation check(wrong type): value = {value}\n was type {type(value)} ...should be type {t}\n{check_history}")
            if len(annot) == 1:
                kAnn,vAnn = dict(annot).popitem()
                if isinstance(kAnn,type):
                    for kVal in value.keys():
                        if not isinstance(kVal,kAnn):
                            return AssertionError(f"{param} failed annotation check(wrong type): value = {kVal}\n was type {type(kVal)} ...should be type {kAnn}\n{check_history}")
                else:
                    for kVal in value.keys():
                        check_history += f'dict[keys] check: {annot}\n'
                        error = Check_Annotation.check(self,param,kAnn,kVal)
                        if error != None:
                            return error
                
                vAnn = annot[kAnn]
                if isinstance(vAnn,type):
                    for vVal in value.values():
                        if not isinstance(vVal,vAnn):
                            return AssertionError(f"{param} failed annotation check(wrong type): value = {vVal}\n was type {type(vVal)} ...should be type {vAnn}\n{check_history}")
                else:
                    for vVal in value.values():
                        check_history += f'dict[values] check: {annot}\n'
                        error = Check_Annotation.check(self,param,vAnn,vVal)
                        if error != None:
                            return error
            else:
                return AssertionError(f"AssertionError: {param} annotation inconsistency: dict should have 1 item but had {len(annot)}\n  annotation = {annot}")
            return
        
        def check_set_or_fset(annot,param,value,check_history,t):
            if not isinstance(value, t):
                return AssertionError(f"{param} failed annotation check(wrong type): value = {value}\n was type {type(value)} ...should be type {t}\n{check_history}")
            if len(annot) > 1:
                return AssertionError(f"{param} annotation inconsistency: set should have 1 value but had {len(annot)}\n annotation = {annot}\n{check_history}")
            for val in value:
                if not isinstance(val, set(annot).pop()):
                    return AssertionError(f"{param} failed annotation check(wrong type): value = {value}\n was type {type(value)} ...should be type {t}\n{check_history}")
            return    
        
        def check_lambda(annot,param,value,check_history):
            if len(annot.__code__.co_varnames) != 1:
                return AssertionError(f"{param} annotation inconsistency: prediocate should have 1 parameter but had {len(annot.__code__.co_varnames)}\n predicate = {annot}\n{check_history}")            
            try:
                if not annot(value):
                    return AssertionError(f"{param} failed annotation check: value = {value}\n predicate = {annot}\n{check_history}")
            except Exception as err:
                return AssertionError(f"{param} annotation predicate({annot}) raised exception\n exception = {err}\n{check_history}")
            return
        
        def check_other(annot,param,value,check_history):
            try:
                annot.__check_annotation__(self.check,param,value,check_history)
            except AttributeError:
                return AssertionError(f"{param} annotation undecipherable: {annot})")
            except Exception as err:
                return AssertionError(f"{param} annotation {annot} raised exception\n exception = {err}\n{check_history}")
        # To begin, get check's function annotation and compare it to its arguments
        if annot is None:
            pass #silent success
        elif isinstance(annot,type):
            assert isinstance(value,annot), f"{param} failed annotation check(wrong type): value = {value}\n was type {type(value)} ...should be type {annot}"
        elif isinstance(annot, list) or isinstance(annot, tuple):
            #check_list(param,annot,value,check_history)
            error = check_list_or_tuple(annot,param,value,check_history,type(annot))
            if error != None: raise error
        elif isinstance(annot, dict):
            error = check_dict(annot,param,value,check_history,type(annot))
            if error != None: raise error
        elif isinstance(annot, set):
            error = check_set_or_fset(annot,param,value,check_history,type(annot))
            if error != None: raise error
        elif isinstance(annot, frozenset):
            error = check_set_or_fset(annot,param,value,check_history,type(annot))
            if error != None: raise error
        elif inspect.isfunction(annot):
            error = check_lambda(annot,param,value,check_history)
            if error != None: raise error
        else:
            error = check_other(annot,param,value,check_history)
            if error != None: raise error
            
              
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return an ordereddict of the parameter/argument bindings: it's a special
        #   kind of dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not (Check_Annotation.checking_on and self._checking_on):
            return self._f(*args,**kargs)
                     
        
        try:
            pa_bindings = param_arg_bindings()
            # Check the annotation for each of the parameters that is annotated
            for param,arg in pa_bindings.items():
                if param in self._f.__annotations__.keys():
                    self.check(param, self._f.__annotations__[param], arg)
            # Compute/remember the value of the decorated function
            pa_bindings['_return'] = self._f(*args,**kargs)
            # If 'return' is in the annotation, check it
            if 'return' in self._f.__annotations__.keys():
                self.check('_return', self._f.__annotations__['return'], pa_bindings['_return'])
            # Return the decorated answer
            return pa_bindings['_return']
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #    print(l.rstrip())
            #print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    #def f(x:int): pass
    #f = Check_Annotation(f)
    #f(3)
    #f('a')
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4F19.txt'
    #driver.default_show_exception= True
    #driver.default_show_exception_message= True
    #driver.default_show_traceback= True
    driver.driver()
