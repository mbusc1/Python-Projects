# Generators must be able to iterate through any iterable.
# hide is present and called to ensure that your generator code works on
#   general iterable parameters (not just a string, list, etc.)
# For example, although we can call len(string) we cannot call
#   len(hide(string)), so the generator functions you write should not
#   call len on their parameters (nor indexing/slicing)
# Leave hide in this file and add code for the other generators.

def hide(iterable):
    for v in iterable:
        yield v



def sequence(*iterables):
    for iterable in iterables:
        for v in iterable:
            yield v


            
def group_when(iterable,p):
    answer = []
    for i in iterable:
        answer.append(i)
        if p(answer[-1]):
            yield answer
            answer = []
    if answer != []:
        yield answer


    
                
def drop_last(iterable,n):
    i = iter(iterable)
    try:
        window = [next(i) for _ in range(n)]
        while True:
            window.append(next(i))
            yield window.pop(0)
    except StopIteration:
        return


        
def yield_and_skip(iterable,skip):
    i = iter(iterable)
    try:
        while True:
            v = next(i)
            yield v
            for _ in range(skip(v)):
                next(i)
    except StopIteration:
        return
        


        
def alternate_all(*args):
#     args = [iter(a) for a in args]
#     while args != []:
#         remaining = []
#         for a in args:
#             try:
#                 yield next(a)
#                 remaining.append(a)
#             except StopIteration:
#                 pass
#         args = remaining
    args = [iter(a) for a in args]
    while True:
        yielded = False
        for a in args:
            try:
                yield next(a)
                yielded = True
            except StopIteration:
                pass
        if not yielded:
            return



def min_key_order(adict):
    if not adict:
        return
    min_value = min(adict)
    yield min_value,adict[min_value]
    while True:
        # Scan dict keys, finding min_bigger: the smallest one > min_value
        min_bigger = None
        for k in adict:
            if k>min_value and (min_bigger == None or k<min_bigger):
                min_bigger = k
        if min_bigger == None:
            return
        else:
            min_value = min_bigger
            yield min_value,adict[min_value]

#         #simpler code for loop body, but declaring list (maybe as big as dict)
#         bigger_values = [k for k in adict if k>min_value]
#         if not bigger_values:
#             return
#         else:
#             min_value = min(bigger_values)
#             yield min_value,adict[min_value]

 
           
         
if __name__ == '__main__':
    from goody import irange
    
    # Test sequence; you can add your own test cases
    print('Testing sequence')
    for i in sequence('abc', 'd', 'ef', 'ghi'):
        print(i,end='')
    print('\n')

    print('Testing sequence on hidden')
    for i in sequence(hide('abc'), hide('d'), hide('ef'), hide('ghi')):
        print(i,end='')
    print('\n')


    # Test group_when; you can add your own test cases
    print('Testing group_when')
    for i in group_when('combustibles', lambda x : x in 'aeiou'):
        print(i,end='')
    print('\n')

    print('Testing group_when on hidden')
    for i in group_when(hide('combustibles'), lambda x : x in 'aeiou'):
        print(i,end='')
    print('\n')


    # Test drop_last; you can add your own test cases
    print('Testing drop_last')
    for i in drop_last('combustible', 5):
        print(i,end='')
    print('\n')

    print('Testing drop_last on hidden')
    for i in drop_last(hide('combustible'), 5):
        print(i,end='')
    print('\n')


    # Test sequence; you can add your own test cases
    print('Testing yield_and_skip')
    for i in yield_and_skip('abbabxcabbcaccabb',lambda x : {'a':1,'b':2,'c':3}.get(x,0)):
        print(i,end='')
    print('\n')

    print('Testing yield_and_skip on hidden')
    for i in yield_and_skip(hide('abbabxcabbcaccabb'),lambda x : {'a':1,'b':2,'c':3}.get(x,0)):
        print(i,end='')
    print('\n')


    # Test alternate_all; you can add your own test cases
    print('Testing alternate_all')
    for i in alternate_all('abcde','fg','hijk'):
        print(i,end='')
    print('\n')
    
    print('Testing alternate_all on hidden')
    for i in alternate_all(hide('abcde'), hide('fg'),hide('hijk')):
        print(i,end='')
    print('\n\n')
       
         
    # Test min_key_order; add your own test cases
    print('\nTesting Ordered')
    d = {1:'a', 2:'x', 4:'m', 8:'d', 16:'f'}
    i = min_key_order(d)
    print(next(i))
    print(next(i))
    del d[8]
    print(next(i))
    d[32] = 'z'
    print(next(i))
    print(next(i))
    


         
         
    import driver
    driver.default_file_name = "bscq4F19.txt"
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
    
