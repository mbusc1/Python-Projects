import re
from goody import irange
from collections import defaultdict

# Before running the driver on the bsc.txt file, ensure you have put a regular
#   expression pattern in the files repattern1a.txt, repattern1b.txt, and
#   repattern2a.txt. The patterns must be all on the first line

def pages (page_spec : str, unique :  bool) -> [int]: #result in ascending order
    answer = []
    for ps in page_spec.split(','):
        m = re.match('^([1-9]\d*)(?:([:-])([1-9]\d*)(?:/([1-9]\d*))?)?$', ps)
        assert m != None, 'pages: Illegal specification: '+ps
        p1, sep, p2, n = m.group(1,2,3,4)
        if sep == None:
            answer.append(int(p1))
        else:
            p1, p2, n = int(p1), int(p2), (1 if n == None else int(n))
            if sep == '-':
                assert p1 <= p2,'pages: in page sequence {p1}-{p2}, {p1} > {p2}'.format(p1=p1,p2=p2)
                answer += [i for i in irange(p1,p2,n)]
            else:
                answer += [i for i in irange(p1,p1+p2-1,n)]

    return sorted(set(answer) if unique else answer)


def expand_re(pat_dict:{str:str}):
    for lhs_to_exp,rhs_to_sub in pat_dict.items():
        lhs_comp = re.compile('#'+lhs_to_exp+'#')
        for lhs,rhs in pat_dict.items():
            pat_dict[lhs] = lhs_comp.sub('(?:'+rhs_to_sub+')',rhs)





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
