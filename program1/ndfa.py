# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
import prompt


def read_ndfa(file : open) -> {str:{str:{str}}}:
    ndfa = {}
    for line in file:
        break_down = line.strip("\n").split(";")
        transitions = {}
        for i in range(1,len(break_down),2):
            if break_down[i] in transitions.keys():
                transitions[break_down[i]].add(break_down[i+1])
            else:
                transitions[break_down[i]] = set()
                transitions[break_down[i]].add(break_down[i+1])
        ndfa[break_down[0]] = transitions
    return ndfa


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    return "\n".join(sorted(["  "+k+" transitions: " + str(sorted([(x,sorted(list(y))) for x,y in v.items()])) for k,v in ndfa.items()])) + "\n"

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    process_steps = [state]
    current_states = {state}
    for cmd in inputs:
        new_states = set()
        for s in current_states:
            if cmd in ndfa[s].keys():
                new_states.update(ndfa[s][cmd])
            else:
                pass
        process_steps.append((cmd,new_states))
        if new_states == set():
            break
        current_states = set(new_states)
    return process_steps


def interpret(result : [None]) -> str:
    out_string = "Start state = " + str(result[0]) + "\n"
    for i in range(1,len(result)):
            out_string += "  Input = {}; new possible states = {}\n".format(result[i][0],sorted(list(result[i][1])))
    out_string += "Stop state(s) = "+str(sorted(list(result[-1][1])))+"\n"
    return out_string





if __name__ == '__main__':
    # Write script here
    ndfa_file_name = prompt.for_string("Enter the file name describing this Non-Deterministic Finite Automaton", is_legal=(lambda f: open(f)), error_message="Please enter a valid file name")
    with open(ndfa_file_name) as f:
        ndfa = read_ndfa(f)
        print("\nThe Description of the file entered for this Non-Deterministic Finite Automaton")
        print(ndfa_as_str(ndfa))
    input_file_name = prompt.for_string("Enter the file name describing a sequence of start-states and all their inputs", is_legal=(lambda f: open(f)), error_message="Please enter a valid file name")
    print()
    with open(input_file_name) as f:
        for line in f:
            line_list = line.strip("\n").split(";")
            process_steps = process(ndfa, line_list[0], line_list[1:len(line_list)])
            print("Start tracing this NDFA in its start-state")
            print(interpret(process_steps)) 
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
