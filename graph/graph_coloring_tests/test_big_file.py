"""Module to test graph with maximum size that supports coloring algorithm."""

import sys
import os
from time import time

sys.path.append(os.getcwd())
from graph.graph_coloring import Graph


graph = Graph()
graph.create_graph_from_file('graph/graph_coloring_tests/max_size_graph.txt')

start = time()
colored_vertices = graph.color_graph(995)
end = time()

expected = [f'V{num}:{num}' for num in range(1, 995)]
print(expected == colored_vertices)
print('Time taken: ', end - start)
