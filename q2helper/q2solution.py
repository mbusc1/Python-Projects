import re
from goody import irange
from collections import defaultdict

# Before running the driver on the bsc.txt file, ensure you have put a regular
#   expression pattern in the files repattern1a.txt, repattern1b.txt, and
#   repattern2a.txt. The patterns must be all on the first line

def pages (page_spec : str, unique :  bool) -> [int]: #result in ascending order
    ret =[]
    pages = page_spec.split(",")
    for page_string in pages:
        mat =[]
        try:
            p2 = open('repattern2a.txt').read().rstrip() # Read pattern on first line
            m = re.match(p2,page_string)
            for mt in m.groups():
                if mt != None:
                    mat.append(mt)
                else:
                    mat.append(None)
        except:
            raise AssertionError('failed on regular expression matching')
                
        # if its a range...
        if mat[1] == '-':
            #make sure its a valid range
            if mat[0] and mat[2] != None:
                if int(mat[0]) > int(mat[2]):
                    raise AssertionError('failed range is smaller than starting page') 
            
            #check for a divisor
            if mat[3] != None:
             for p in irange(int(mat[0]), int(mat[2]), int(mat[3])):
                ret.append(p)
            # equal range
            elif int(mat[0]) == int(mat[2]):
                ret.append(mat[0])
            # if no divisor but range
            else:
                for p in irange(int(mat[0]), int(mat[2])):
                    ret.append(p)
                
        #if its a constructed range
        elif mat[1] == ':':
            #check for a divisor
            if mat[3] != None:
             for p in irange(int(mat[0]), int(mat[0])+int(mat[2]), int(mat[3])):
                ret.append(p)
            # otherwise
            # if no divisor but range
            else:
                for p in irange(int(mat[0]), int(mat[0])+int(mat[2])):
                    ret.append(p)
        # or no divisor and range   
        else:
            ret.append(int(mat[0]))
    
    if unique:
        s = {item for item in ret}
        return sorted(list(s))        
    else:
        return sorted(ret)        
        
        

def expand_re(pat_dict:{str:str}):
    for rule in pat_dict.keys():
        rep = re.compile("#"+str(rule)+"#")
        for r in pat_dict.keys():
            pat_dict[r] = re.sub(rep, "(?:"+str(rule)+")", pat_dict[r])
    return None




if __name__ == '__main__':
    
    p1a = open('repattern1a.txt').read().rstrip() # Read pattern on first line
    print('Testing the pattern p1a: ',p1a)
    for text in open('bm1.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1a,text)
        print(' ','Matched' if m != None else "Not matched")
        
    p1b = open('repattern1b.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p1b: ',p1b)
    for text in open('bm1.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1b,text)
        print('  ','Matched with groups ='+ str(m.groups()) if m != None else 'Not matched' )
        
        
    p2 = open('repattern2a.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p2: ',p2)
    for text in open('bm2a.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p2,text)
        print('  ','Matched with groups ='+ str(m.groups()) if m != None else 'Not matched' )
        
    print('\nTesting pages function')
    for text in open('bm2b.txt'):
        text = text.rstrip().split(';')
        text,unique = text[0], text[1]=='True'
        try:
            p = pages(text,unique)
            print('  ','pages('+text+','+str(unique)+') = ',p)
        except:
            print('  ','pages('+text+','+str(unique)+') = raised exception')
        
    
    print('\nTesting expand_re')
    pd = dict(digit = r'[0-9]', integer = r'[+-]?#digit##digit#*')
    print('  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary
    # {'digit': '[0-9]', 'integer': '[+-]?(?:[0-9])(?:[0-9])*'}
    
    pd = dict(integer       = r'[+-]?[0-9]+',
              integer_range = r'#integer#(..#integer#)?',
              integer_list  = r'#integer_range#(?,#integer_range#)*',
              integer_set   = r'{#integer_list#?}')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'integer': '[+-]?[0-9]+',
    #  'integer_range': '(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?',
    #  'integer_list': '(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*',
    #  'integer_set': '{(?:(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*)?}'
    # }
    
    pd = dict(a='correct',b='#a#',c='#b#',d='#c#',e='#d#',f='#e#',g='#f#')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'a': 'correct',
    #  'b': '(?:correct)',
    #  'c': '(?:(?:correct))',
    #  'd': '(?:(?:(?:correct)))',
    #  'e': '(?:(?:(?:(?:correct))))',
    #  'f': '(?:(?:(?:(?:(?:correct)))))',
    #  'g': '(?:(?:(?:(?:(?:(?:correct))))))'
    # }
    
    print()
    print()
    import driver
    driver.default_file_name = "bscq2F19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
