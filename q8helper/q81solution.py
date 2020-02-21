from performance import Performance
from goody import irange
from graph_goody import random_graph,spanning_tree
from graph import Graph

# Put script below to generate data for Problem #1
# In case you fail, the data appears in sample8.pdf in the helper folder
global nodes
global graph
if __name__ == '__main__':
    nodes = 1000
    while nodes <= 128000:
        graph = random_graph(nodes,lambda n : 10*n)
        perf = Performance(lambda: spanning_tree(graph),setup=lambda:None,times_to_measure=5,title='Spanning Tree Timings for '+str(nodes)+' nodes')
        perf.evaluate()
        perf.analyze()
        nodes *= 2