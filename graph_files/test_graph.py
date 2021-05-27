"""Module to test graph coloring from module graph.py with unittests."""

import unittest
import sys
import os

sys.path.append(os.getcwd())
from graph import Graph


class TestGraphColoring(unittest.TestCase):
    """Class to unit test class Graph from graph.py."""

    def setUp(self):
        """Build initial graphs from edges lists."""
        self.graph_1 = Graph(
            [('A', 'B'), ('B', 'C'), ('A', 'C'), ('C', 'D'), ('A', 'D')])
        self.graph_2 = Graph([('A', 'B'), ('C', 'D')])
        self.graph_3 = Graph([('A', 'A')])
        self.graph_4 = Graph([])
        self.graph_5 = Graph(set())
        self.graph_6 = Graph({('A', 'B'), ('A', 'C')})

    def test_assertion_errors(self):
        """
        Test exeptions (AssertionError) caught in function color_graph
        with unsupported function arguments.
        """
        with self.assertRaises(AssertionError) as err:
            self.graph_1.color_graph(0)
        self.assertEqual(str(err.exception),
                         'Colors number should be greater than 1.')

        with self.assertRaises(AssertionError) as err:
            self.graph_1.color_graph(-1)
        self.assertEqual(str(err.exception),
                         'Colors number should be greater than 1.')

        with self.assertRaises(AssertionError) as err:
            self.graph_1.color_graph([])
        self.assertEqual(str(err.exception),
                         'Colors number should be an integer.')

    def test_incorrect_graph_file_representation(self):
        """
        Test function create_graph_from_file if the graph
        representation format in the file is incorrect.
        """
        graph = Graph()

        with self.assertRaises(AssertionError) as err:
            graph.create_graph_from_file('graph_files/incorrect_file.txt')
        self.assertEqual(str(err.exception),
                         'Vertices in the file should be represented as U: V')

    def test_connected_graph_and_read_from_file(self):
        """Test connected graph."""
        self.assertEqual(self.graph_1.color_graph(2), None)
        self.assertEqual(self.graph_1.color_graph(3),
                         ['A:1', 'B:2', 'C:3', 'D:2'])

        graph_1 = Graph()
        graph_1.create_graph_from_file('graph_files/graph_1.txt')
        self.assertEqual(graph_1.color_graph(2), None)
        self.assertEqual(graph_1.color_graph(3),
                         ['A:1', 'B:2', 'C:3', 'D:2'])

        graph_2 = Graph()
        graph_2.create_graph_from_file('graph_files/graph_2.txt')
        self.assertEqual(graph_2.color_graph(2), None)
        self.assertEqual(graph_2.color_graph(3),
                         ['A:1', 'B:2', 'C:3', 'D:2'])

    def test_disconnected_graph(self):
        """Test disconnected graph."""
        self.assertEqual(self.graph_2.color_graph(1), None)
        self.assertEqual(self.graph_2.color_graph(2),
                         ['A:1', 'B:2', 'C:1', 'D:2'])

    def test_recursion_error(self):
        """
        Test graph with too much vertices, when
        maximum recursion depth is exceeded.
        """
        graph = Graph()
        edges = []

        for num in range(1, 996):
            edges.append(('V' + str(num), 'V' + str(num + 1)))
        graph.create_graph_from_edges_list(edges)

        with self.assertRaises(RecursionError):
            graph.color_graph(2)

    def test_single_vertex_graph(self):
        """Test graph with only one vertex."""
        self.assertEqual(self.graph_3.color_graph(1), ['A:1'])

    def test_empty_vertices_list_and_read_file(self):
        """Test graph built from an empty list and empty file."""
        self.assertEqual(self.graph_4.color_graph(1), [])

        graph = Graph()
        graph.create_graph_from_file('graph_files/empty_graph.txt')
        self.assertEqual(graph.color_graph(1), [])

        self.assertEqual(self.graph_4.color_graph(1),
                         graph.color_graph(1))

    def test_graph_built_from_set(self):
        """Test graph built from a set of edges."""
        self.assertEqual(self.graph_5.color_graph(1), [])
        self.assertTrue(set(self.graph_6.color_graph(2)) in (
            {'A:1', 'B:2', 'C:2'}, {'A:2', 'B:1', 'C:1'}))


if __name__ == '__main__':
    unittest.main()
