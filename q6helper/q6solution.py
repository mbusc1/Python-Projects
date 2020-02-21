from functools import reduce         # can use for bases
from collections import defaultdict  # can use for popdict



# List Node class and helper functions (to set up problem)

class LN:
    def __init__(self,value,next=None):
        self.value = value
        self.next  = next

def list_to_ll(l):
    if l == []:
        return None
    front = rear = LN(l[0])
    for v in l[1:]:
        rear.next = LN(v)
        rear = rear.next
    return front

def str_ll(ll):
    answer = ''
    while ll != None:
        answer += str(ll.value)+'->'
        ll = ll.next
    return answer + 'None'




# Tree Node class and helper functions (to set up problem)

class TN:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left  = left
        self.right = right

def list_to_tree(alist):
    if alist == None:
        return None
    else:
        return TN(alist[0],list_to_tree(alist[1]),list_to_tree(alist[2])) 
    
def str_tree(atree,indent_char ='.',indent_delta=2):
    def str_tree_1(indent,atree):
        if atree == None:
            return ''
        else:
            answer = ''
            answer += str_tree_1(indent+indent_delta,atree.right)
            answer += indent*indent_char+str(atree.value)+'\n'
            answer += str_tree_1(indent+indent_delta,atree.left)
            return answer
    return str_tree_1(0,atree) 



# Define separate ITERATIVELY

def separate(ll,p):
    truelist = None
    falselist = None
    #print(str_ll(truelist),str_ll(falselist))
    while ll != None:       
        if p(ll.value):
            prepend = LN(ll.value)
            prepend.next = truelist
            truelist = prepend
            
            #print(str_ll(truelist),'true')            
        else:
            prepend = LN(ll.value)
            prepend.next = falselist
            falselist = prepend
            
            #print(str_ll(falselist),'false')
        
        ll = ll.next
    
    return truelist, falselist
    

# Define is_min_heap RECURSIVELY

def is_min_heap(t):
    #base case, reached end of tree limb
    if t == None:
        return True
       
    if t.right == None and t.left == None:
        return True
    
    #non-base cases
    if t.right == None:
        if t.value < t.left.value:
            return is_min_heap(t.left)
        else:
            return False
    
    if t.left == None:
        if t.value < t.right.value:
            return is_min_heap(t.right)
        else:
            return False
    
    
    # otherwise if no nodes are none....
    
    if (t.value < t.right.value) and (t.value < t.left.value):
        return is_min_heap(t.right) and is_min_heap(t.left)
    else:
        return False
        
    
# Define bases RECURSIVELY

def bases(c):
    #print(c.__bases__)
    ret = set()
    ret.add(c)
    #base case - no more to inherit
    if c.__bases__ == ():
        return set()
    
    #otherwise iter through the bases
    #and return their union 
    for base in c.__bases__:
        ret = ret.union(set(c.__bases__),bases(base))
    
    return ret   


# Define the derived popdict class

class popdict(dict):
    pass
            




# Testing Script

if __name__ == '__main__':
    print('Testing separate')
    ll = list_to_ll([i for i in range(20)])
    even,odd = separate(ll,lambda x : x%2 == 0) 
    print(str_ll(even)+' and '+str_ll(odd))
    
    import predicate
    prime,composite = separate(ll,predicate.is_prime) 
    print(str_ll(prime)+' and '+str_ll(composite))
    
    small,big = separate(ll,lambda x : x <= 10) 
    print(str_ll(small)+' and '+str_ll(big))
    
    

    print('\nTesting is_min_heap')
    t = None
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
          
    t = list_to_tree([1,[2,None,None],[3,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([2,[1,None,None],[3,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
          
    t = list_to_tree([3,[2,None,None],[1,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([1,None,[3,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
           
    t = list_to_tree([1,[2,None,None],None]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([3,None,[1,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
           
    t = list_to_tree([2,[1,None,None],None]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree(
            [5,
              [8,
                [16,
                   [32,None,None],
                   [46,
                      [70,None,None],
                      [82,None,None]
                   ]
                ],
                None],
              [12,
                 [24,
                    None,
                    [30,
                       [40,None,None],
                       [70,None,None]
                    ]
                 ],
                 None
              ]
            ])
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
  
    t = list_to_tree(
            [5,
              [8,
                [16,
                   [32,None,None],
                   [32,
                      [70,None,None],
                      [82,None,None]
                   ]
                ],
                None],
              [12,
                 [30,
                    None,
                    [30,
                       [40,None,None],
                       [70,None,None]
                    ]
                 ],
                 None
              ]
            ])
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  

    t = list_to_tree(
            [5,
              [8,
                [16,
                   [32,None,None],
                   [46,
                      [70,None,None],
                      [82,None,None]
                   ]
                ],
                None],
              [12,
                 [30,
                    None,
                    [30,
                       [40,None,None],
                       [70,None,None]
                    ]
                 ],
                 None
              ]
            ])
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
      
    
    
    print('\nTesting bases')
    
    class F:pass
    class C:pass
    class G:pass
    class B(F):pass
    class D(G):pass
    class A(B,C,D):pass
    print(bases(A))
    
    class A          : pass    
    class B          : pass
    class C(A)       : pass    
    class D(A,B)     : pass
    class E(A)       : pass
    class F(C,D)     : pass    
    class G(B)       : pass
    class H(E,F,G)   : pass
    print(bases(H))
          
  

    print('\nTesting popdict')
    d = popdict([('a',100)],b=200,c=300)
    print('initial')
    print(d)
    print([(k,d(k)) for k in 'abcx'])
    
    d['a']
    d['b']
    d['b']
    d['a'] = 103
    d['a'] += 1  # accesses d['a'] 2 times: to get value and store value
    d['c'] += 5  # accesses d['c'] 2 times: to get value and store value
    d['c'] += 1  # accesses d['c'] 2 times: to get value and store value
    d['c'] += 1  # accesses d['c'] 2 times: to get value and store value
    try:
        d['x'] # should raise exception: 
        print('Did not raise exception')
    except:
        pass
    
    print('\nafter some updates')
    print(d)
    print([(k,d(k)) for k in 'abcx'])
    
    print('\niteration order =',[k for k in d])
    
    del d['a']
    
    print('\nafter delete')
    print(d)
    print([(k,d(k)) for k in 'abcx'])

    d.clear()
    
    print('\nafter clear')
    print(d)
    print([(k,d(k)) for k in 'abcx'])
    
     
    
# Result from running driver

# Testing separate
# 18->16->14->12->10->8->6->4->2->0->None and 19->17->15->13->11->9->7->5->3->1->None
# 19->17->13->11->7->5->3->2->None and 18->16->15->14->12->10->9->8->6->4->1->0->None
# 10->9->8->7->6->5->4->3->2->1->0->None and 19->18->17->16->15->14->13->12->11->None
# 
# Testing is_min_heap
# 
# Tree is
#  is_min_heap = True
# 
# Tree is
#  ..3
# 1
# ..2
# is_min_heap = True
# 
# Tree is
#  ..3
# 2
# ..1
# is_min_heap = False
# 
# Tree is
#  ..1
# 3
# ..2
# is_min_heap = False
# 
# Tree is
#  ..3
# 1
# is_min_heap = True
# 
# Tree is
#  1
# ..2
# is_min_heap = True
# 
# Tree is
#  ..1
# 3
# is_min_heap = False
# 
# Tree is
#  2
# ..1
# is_min_heap = False
# 
# Tree is
#  ..12
# ........70
# ......30
# ........40
# ....24
# 5
# ..8
# ........82
# ......46
# ........70
# ....16
# ......32
# is_min_heap = True
# 
# Tree is
#  ..12
# ........70
# ......30
# ........40
# ....30
# 5
# ..8
# ........82
# ......32
# ........70
# ....16
# ......32
# is_min_heap = False
# 
# Tree is
#  ..12
# ........70
# ......30
# ........40
# ....30
# 5
# ..8
# ........82
# ......46
# ........70
# ....16
# ......32
# is_min_heap = False
# 
# Testing bases
# {<class '__main__.D'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.G'>, <class 'object'>, <class '__main__.C'>, <class '__main__.F'>}
# {<class '__main__.A'>, <class '__main__.E'>, <class 'object'>, <class '__main__.H'>, <class '__main__.D'>, <class '__main__.G'>, <class '__main__.F'>, <class '__main__.C'>, <class '__main__.B'>}
# 
# Testing popdict
# initial
# {'a': 100, 'b': 200, 'c': 300}
# [('a', 1), ('b', 1), ('c', 1), ('x', 0)]
# 
# after some updates
# {'a': 104, 'b': 200, 'c': 307}
# [('a', 5), ('b', 3), ('c', 7), ('x', 0)]
# 
# iteration order = ['c', 'a', 'b']
# 
# after delete
# {'b': 200, 'c': 307}
# [('a', 0), ('b', 3), ('c', 7), ('x', 0)]
# 
# after clear
# {}
# [('a', 0), ('b', 0), ('c', 0), ('x', 0)]
    
