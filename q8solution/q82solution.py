import cProfile
from graph_goody import random_graph, spanning_tree
import pstats

# Put script here to generate data for Problem #2

g = random_graph (15000, lambda n : 10*n)

cProfile.run('spanning_tree(g)','profile15K')
p = pstats.Stats('profile15K')
p.strip_dirs().sort_stats('ncalls').print_stats(10)
p.strip_dirs().sort_stats('time').print_stats(10)
