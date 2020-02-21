# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
import prompt
from collections import defaultdict
from test.test_email import openfile


def read_graph(file : open) -> {str:{str}}:
    graph = {}
    for line in file:
        k,v = line.strip("\n").split(";")
        if k in graph.keys():
            graph[k].add(v)
        else:
            graph[k] = set(v)
    return(graph)


def graph_as_str(graph : {str:{str}}) -> str:
    return "".join(sorted(["  {0} -> ['{1}']\n".format(k,"', '".join(sorted(list(v)))) for k,v in graph.items()]))
    

        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set = set()
    exploring_list = [start]
    while exploring_list != []:
        popped = exploring_list.pop(0)
        if trace:
            print("removing node "+str(popped)+" from the exploring list; adding it to reached list")
        if popped in graph.keys():
            for node in graph[popped]:
                if node not in reached_set:
                    exploring_list.insert(0,node)
            
        reached_set.add(popped)
        if trace:
            print("after adding all nodes reachable directly from" + str(popped) + "but not already in reached, exploring = " + str(exploring_list) + "\n")
            print("reached set    = " + str(reached_set))
            print("exploring list = " + str(exploring_list))
             
    return(reached_set)

if __name__ == '__main__':
    # Write script here
    graph_file = prompt.for_string("Enter the file name describing this graph", is_legal=(lambda f: open(f)), error_message="Please enter a valid file name")
    with open(graph_file) as f:
        graph = read_graph(f)
        
    print("Graph: a node -> [showing all its destination nodes]")
    print(graph_as_str(graph))
    while(True):
        start_node = prompt.for_string("Enter the starting node (or enter quit)", is_legal=(lambda s: s in graph.keys() or s == 'quit'), error_message="Please enter a legal String")
        if start_node == 'quit': break
        trace = prompt.for_bool("Enter whether to trace this algorithm (True/False)", error_message='Please enter "True" or "False"')
        print("From node a its reachable nodes:", reachable(graph,start_node,trace))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
