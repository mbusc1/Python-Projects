# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
import prompt
from Tools.demo.sortvisu import steps


def read_fa(file : open) -> {str:{str:str}}:
    fa = {}
    for line in file:
        break_down = [x for x in line.strip("\n").split(";")]
        fa[break_down[0]] = {break_down[x]:break_down[x+1] for x in range(1,len(break_down),2)}
    return fa


def fa_as_str(fa : {str:{str:str}}) -> str:
    return "\n".join(sorted(["  "+k+" transitions: " + str(sorted([(x,y) for x,y in v.items()])) for k,v in fa.items()])) + "\n"

    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    process_steps = [state]
    current_state = str(state)
    for cmd in inputs:
        if cmd not in fa[current_state].keys(): 
            process_steps.append(('x',None))
            break
        process_steps.append((cmd,fa[current_state][cmd]))
        current_state = fa[current_state][cmd]
    return process_steps


def interpret(fa_result : [None]) -> str:
    out_string = "Start state = " + str(fa_result[0]) + "\n"
    for i in range(1,len(fa_result)):
        if fa_result[i][0] != 'x':
            out_string += "  Input = {}; new state = {}\n".format(fa_result[i][0],fa_result[i][1])
        else:
            out_string += "  Input = x; illegal input: simulation terminated\n"
    out_string += "Stop state = "+str(fa_result[-1][1])+"\n"
    return out_string


if __name__ == '__main__':
    # Write script here
    fa_file_name = prompt.for_string("Enter the file name describing this Finite Automaton", is_legal=(lambda f: open(f)), error_message="Please enter a valid file name")
    with open(fa_file_name) as f:
        fa = read_fa(f)
        print("The Description of the file entered for this Finite Automaton")
        print(fa_as_str(fa))
    input_file_name = prompt.for_string("Enter the file name describing a sequence of start-states and all their inputs", is_legal=(lambda f: open(f)), error_message="Please enter a valid file name")
    print()
    with open(input_file_name) as f:
        for line in f:
            line_list = line.strip("\n").split(";")
            process_steps = process(fa, line_list[0], line_list[1:len(line_list)])
            print("Start tracing this FA in its start-state")
            print(interpret(process_steps))  
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
