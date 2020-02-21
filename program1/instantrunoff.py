# Submitter: mbuscemi(Buscemi, Matthew)
# Partner  : wbuscemi(Buscemi, William)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
import prompt


def read_voter_preferences(file : open):
    voter_prefs = {} #create dictionary to return
    for line in file: #for each lien in the file which represents a single voter
        pref = line.strip("\n").split(";") #remove the newline char and split along semicolons
        voter_prefs[pref[0]] = pref[1:len(pref)] #use first index as key and the rest as list of preferences
    return(voter_prefs) #return the compelte dictionary


def dict_as_str(d : {None:None}, key : callable=None, reverse : bool=False) -> str:
    sorted_keys = sorted([k for k in d.keys()],key=key,reverse=reverse)
    out_string = ""
    for k in sorted_keys:
        out_string += "  {0} -> {1}\n".format(k,d[k]) 
    return(out_string)


def evaluate_ballot(vp : {str:[str]}, cie : {str}) -> {str:int}:
    ballot = {can:0 for can in cie} #construct initial dictionary of all remaning candidates and 0 votes
    for voter in vp.keys():
        for pref in vp[voter]:
            if pref in cie:
                ballot[pref] += 1
                break
    return(ballot)            


def remaining_candidates(vd : {str:int}) -> {str}:
    return {can for can in vd.keys() if vd[can] != min(vd.values())}



def run_election(vp_file : open) -> {str}:
    vp = read_voter_preferences(vp_file) # create initial dict
    print("Preferences: voter -> [candidates in order]")
    print(dict_as_str(vp))
    cie = set() # intiialize candidate set
    for voter in vp.keys(): # for each voter 
        cie.update(set(vp[voter])) #gather their candidates into a set
    count = 1
    while True:
        vd = evaluate_ballot(vp,cie) #for each ballot, evaluate
        print("Vote count on ballot #"+str(count)+": candidates (sorted alphabetically) using only candidates in set", cie)
        print(dict_as_str(vd))
        print("Vote count on ballot #"+str(count)+": candidates (sorted numerically) using only candidates in set", cie)
        print(dict_as_str(vd,lambda x:vd[x],True))
        cie = remaining_candidates(vd) #get the remaining candidates formt eh evaluated ballot
        count+=1
        if len(cie) <= 1: #if there are 1 or less candidates remaining, returnt he winner or none signifyign tie.
            break
    if cie == set():
        print("Tie among final candidates: cannot choose one unique winner")
    else:
        print("Election winner is",str(cie))
    return cie
if __name__ == '__main__':
    # Write script here
    with open(prompt.for_string("Enter the file name describing all the voter preferences",is_legal=lambda f:open(f),error_message="Please enter a valid filename")) as vp_file:
        run_election(vp_file)              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
