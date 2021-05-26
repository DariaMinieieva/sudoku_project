"""Module with graph coloring with backtracking method implementation."""


class Vertex:
    """Class to represent a graph vertex."""

    def __init__(self, item: str, color: int = None):
        """Initialize vertex with its value and color data."""
        self._item = item
        if color:
            self._color = int(color)
        else:
            self._color = None

    def get_color(self) -> int:
        """Get color of the vertex."""
        return self._color

    def set_color(self, color: int):
        """Set vertex color to the new value."""
        self._color = color

    def clear_color(self):
        """Clear vertex color."""
        self.set_color(None)

    def is_colored(self) -> bool:
        """Check whether the vertex is colored."""
        return bool(self._color)

    def __str__(self) -> str:
        """
        Return vertex data as a string in format 'item:color'.
        Ignore the color data if it is not colored.
        """
        if self.is_colored():
            return f'{self._item}:{self._color}'
        return str(self._item)


class Edge:
    """Class to represent a graph edge."""

    def __init__(self, vertex_1: 'Vertex', vertex_2: 'Vertex'):
        """Initialize the edge with two vertices."""
        self._vertex_1 = vertex_1
        self._vertex_2 = vertex_2

    def get_edge_endpoints(self) -> tuple:
        """Return tuple with the edge vertices."""
        return (self._vertex_1, self._vertex_2)

    def __str__(self) -> str:
        """Return edge vertices tuple as a string."""
        return f'({str(self._vertex_1)}, {str(self._vertex_2)})'


class Graph:
    """Class to represent a non-oriented graph based on dictionary."""

    def __init__(self, edges_list=None):
        """
        Initialize the graph dictionary to contain its vertices
        as a key and its connected edges as a value.
        Fill the dictionary if there is a list of graph edges.
        """
        self._graph = {}
        if edges_list:
            self.create_graph_from_edges_list(edges_list)

    def _clear(self):
        """Clear the graph dictionary."""
        self._graph = {}

    def _insert_vertex(self, vertex: 'Vertex'):
        """Insert a single vertex to the graph dictionary."""
        self._graph[vertex] = set()

    def _append_graph_dict(self, vertex: 'Vertex', edge: 'Edge'):
        """Append graph dictionary with the vertex and the edge."""
        try:
            self._graph[vertex].add(edge)
        except KeyError:  # totally new vertex in the graph
            self._graph[vertex] = {edge}

    def _insert_edge(self, vertex_1: 'Vertex', vertex_2: 'Vertex'):
        """Insert the edge represented as two vertices to the graph dictionary."""
        edge = Edge(vertex_1, vertex_2)
        self._append_graph_dict(vertex_1, edge)
        self._append_graph_dict(vertex_2, edge)

    def create_graph_from_edges_list(self, edges_list: list):
        """
        Create the new graph dictionary from list of tuples,
        where each tuple represents the edge of the graph.
        """
        self._clear()
        all_vertices = set()

        for vertex_1, vertex_2 in edges_list:
            all_vertices.add(vertex_1)
            all_vertices.add(vertex_2)

        vertices_dict = {}
        for vertex in all_vertices:
            vertices_dict[vertex] = Vertex(vertex)

        for vertex_1, vertex_2 in edges_list:
            self._insert_edge(vertices_dict[vertex_1], vertices_dict[vertex_2])

    def create_graph_from_file(self, path: str):
        """
        Create the new graph dictionary from the file,
        where each line contains two graph vertices in the
        next format: Vertex_item_1: Vertex_item_2, e.g. A1: A2.
        """
        assert isinstance(path, str), 'File path should be a string.'

        self._clear()
        edges_list = list()

        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                try:
                    vertex_1 = line[:line.index(': ')]

                except ValueError as exception:
                    raise AssertionError(
                        'Vertices in the file should be represented as U: V') from exception

                connected_vertices = line[line.index(': ') + 2:].split(', ')
                for vertex in connected_vertices:
                    edges_list.append((vertex_1, vertex))

        self.create_graph_from_edges_list(edges_list)

    def _get_all_vertices(self) -> list:
        """Get the list of all vertices in the graph."""
        return list(self._graph.keys())

    def _get_connected_vertices(self, vertex: 'Vertex') -> set:
        """Get the set of all vertices connected to the particular one."""
        connected_vertices = set()

        for edge in self._graph[vertex]:
            for edge_vertex in edge.get_edge_endpoints():
                if edge_vertex != vertex:
                    connected_vertices.add(edge_vertex)

        return connected_vertices

    def _is_available(self, vertex: 'Vertex', color: int) -> bool:
        """
        Check whether the particular color can be set to the vertex,
        based on its connected vertices colors.
        """
        for connected_vert in self._get_connected_vertices(vertex):
            if connected_vert.get_color() == color:
                return False

        return True

    def _recurse(self, index: int, max_color: int):
        """
        Recursive function that implements the backtrack algorithm.
        Return True if graph can be colored with a limited number
        max_color of colors.
        """
        try:
            current_vertex = self._get_all_vertices()[index]
        except IndexError:
            return True

        for color in range(1, max_color + 1):
            if self._is_available(current_vertex, color):
                current_vertex.set_color(color)

                if self._recurse(index + 1, max_color):
                    return True

                current_vertex.clear_color()

    def color_graph(self, max_color: int) -> list:
        """
        Return list of the string-represented vertices of the graph if it
        can be colored with a limited number max_color of colors, else None.
        """
        assert isinstance(
            max_color, int), 'Colors number should be an integer.'
        assert max_color >= 1, 'Colors number should be greater than 1.'

        if self._recurse(0, max_color):
            return [str(vertex) for vertex in self._get_all_vertices()]

    def __str__(self) -> str:
        """
        Return graph dictionary with its elements represented as a strings.
        """
        string_repr = ''

        for key, value in self._graph.items():
            string_repr += f'{key} : {", ".join([str(vertex) for vertex in value])}' + '\n'

        return string_repr[:-1]


if __name__ == '__main__':
    pass
