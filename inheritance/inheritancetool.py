from goody import type_as_str

def pgetattr(an_object, attr,*default):
    # Try to locate attr in in object itself
    # Otherwise try to locate it in the classes in the __mro__ list
    #   based on the type of an_object (in order), which starts with
    #   type(an_object).
    # Finally return default[0] (if a third argument, and no more, was specified) or
    #   raise AttributeError if it was not

    if attr in an_object.__dict__:
        return an_object.__dict__[attr]
    else:
        for c in type(an_object).__mro__:
            if attr in c.__dict__:
                return c.__dict__[attr]
    
    if len(default) == 1:
        return default[0]

    raise AttributeError("'"+type_as_str(an_object)+"' object has no attribute '"+attr+"'")


# Search Constraints for mro
#   (1) Base classes must be searched in the order they appear in each derived
#         class definition.
#   (2) A derived class must be searched before any of the base class it was
#          derived from.

# bases is all the bases the new class is derived from
def compute_mro(*bases, debugging=False):
    # constraints is a list of lists; each inner list specifies the constraints
    #   for a base class or the new class (last, specified by *bases)
    # mro is the final order for searching all the base classes
    constraints = [list(c.__mro__) for c in bases] + [list(bases)]
    mro         = []
    
    # While there are constraints to satisfy
    while constraints:
        if debugging: print('\nConstraints =',constraints)
        
        # Find the first candidate in an inner constraint-list that does not appear anywhere
        #   but as the first in all other inner constraint-lists
        for const in constraints:
            candidate = const[0]
            if debugging: print('Trying candidate:',candidate)
            if not any([candidate in later[1:] for later in constraints]):
                if debugging: print('Selected candidate:',candidate)
                break
        else: # for finished without breaking; no candidate is possible!
            raise TypeError('Cannot create a consistent method resolution order (MRO) for bases ' +\
                               ', '.join(str(b)[8:-2] for b in bases))

        
        # That candidate is next in the mor
        mro.append(candidate)
        
        # Remove candidate from being the first in any inner constraint-list
        for const in constraints:
            if const[0] == candidate:
                if debugging: print('Removing candidate from:', const)
                del const[0]
                
        # If any innner constraint-list has been reduced to [], remove it
        constraints = [c for c in constraints if c != []]
        
    return tuple(mro)
            
def compute_mro_r(*bases, debugging=False):
    def merge(constraints):
        if constraints == []:
            return ()
        else:
            for const in constraints:
                candidate = const[0]
                if not any([candidate in later[1:] for later in constraints]):
                    break
            else: # for finished without breaking; no candidate is possible!
                raise TypeError('Cannot create a consistent method resolution order (MRO) for bases ' +\
                                   ', '.join(str(b)[8:-2] for b in bases))
            
            return (candidate,) + \
               merge([const[1:] if const[0] == candidate else const for const in constraints if const != [candidate]])
    return merge([list(c.__mro__) for c in bases] + [list(bases)])

# For each group, uncomment all but the last class declaration (and uncomment the print)

class B1a     : pass       # object is the base class of the derived class B1
class B1(B1a) : pass       # B1a is the base class of the derived class B1
class B2      : pass       # object is the base class of derived class B2
#class C(B1,B2): pass       # B1 and B2 (in that order) are the base classes of C
print('\nmro =',compute_mro(B1,B2,debugging=True))

# class A            : pass   # __mro__ is (A,object)
# class B            : pass   # __mro__ is (B,object)
# class C            : pass   # __mro__ is (C,object)
# class D            : pass   # __mro__ is (D,object)
# class E            : pass   # __mro__ is (E,object)
# class K1(A, B, C)  : pass   # __mro__ is (K1,A,B,C,object)
# class K2(D, B, E)  : pass   # __mro__ is (K2,D<B,E,object)
# class K3(D, A)     : pass   # __mro__ is (K3,D,A,object)
# #class Z(K1, K2, K3): pass   # __mro__ is (Z,K1,K2,K3,D,  A, B, C, E, object)
# print('\nmro =',compute_mro(K1,K2,K3,debugging=True))

# class A          : pass
# class B          : pass
# class C(A,object): pass
# class D          : pass
# class E(D,B)     : pass
# class F(B,C)     : pass
# #class G(E,F)     : pass
# print('\nmro =',compute_mro(E,F,debugging=True))

# class A     : pass    # __mro__ is [A, object]
# class B     : pass    # __mro__ is [B, object]
# class C(A,B): pass    # __mro__ is [C, A, B, object]
# class D(B,A): pass    # __mro__ is [D, B, A, object]
# #class E(C,D): pass    # __mro__ is not possible
# print('\nmro =',compute_mro(C,D,debugging=True))
