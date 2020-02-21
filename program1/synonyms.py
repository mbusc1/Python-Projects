# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming


import re                               # used in my sentence_at_a_time generator function
import math                             # use in cosine_meteric
import prompt                           # for use in script
import goody                            # for use in script
from collections import defaultdict     #  dicts and defaultdictsare == when they have the same keys/associations


# For use in build_semantic_dictionary: see problem specifications
def sentence_at_a_time(open_file : open, ignore_words : {str}) -> [str]:
    end_punct    = re.compile('[.?\!;:]')
    remove_punct = re.compile(r'(,|\'|"|\*|\(|\)|--|'+chr(8220)+'|'+chr(8221)+')')
    prev   = []
    answer = []
    for l in open_file:
        l = remove_punct.sub(' ',l.lower())
        prev = prev + l.split()
        while prev:
            w = prev.pop(0)
            if end_punct.search(w):
                while end_punct.search(w):
                    w = w[0:-1]
                if w != '' and w not in ignore_words:
                    if end_punct.search(w):
                        print(w)
                    answer.append(w)
                    yield answer
                    answer = []
            else:
                if w != '' and w not in ignore_words:
                    answer.append(w)
                    
    # handle special case of last sentence missing final punctuation                
    if answer:
        yield answer


def build_semantic_dictionary(training_files : [open], ignore_file : open) -> {str:{str:int}}:
    pass


def dict_as_str(semantic : {str:{str:int}}) -> str:
    out_string = ""
    dict_lengths = []
    for k,v in semantic.items():
        item_count = 0
        new_line = "context for {} =".format(k)
        for w,c in v.items():
            new_line += " {}@{},".format(w,c)
            item_count += 1
        new_line += "\n"
        dict_lengths.append(item_count)
    out_string += "min/max context lenghts = {}/{}\n".format(min(dict_lengths),max(dict_lengths))
    return out_string

       
def cosine_metric(context1 : {str:int}, context2 : {str:int}) -> float:
    pass 


def most_similar(word : str, choices : [str], semantic : {str:{str:int}}, metric : callable) -> str:
    pass 


def similarity_test(test_file : open, semantic : {str:{str:int}}, metric : callable) -> str:
    pass 




# Script

if __name__ == '__main__':
    # Write script here
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
