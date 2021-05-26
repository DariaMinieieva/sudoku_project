class Vertex:

    def __init__(self, item: str, color=None):
        self._item = item
        if color:
            self._color = int(color)
        else:
            self._color = None

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def clear_color(self):
        self.set_color(None)

    def is_colored(self):
        return bool(self._color)

    def __str__(self):
        if self.is_colored():
            return f'{self._item}:{self._color}'
        return str(self._item)


class Edge:

    def __init__(self, u, v):
        self._origin_vertex = u
        self._destination_vertex = v

    def get_edge_endpoints(self):
        """Return (u,v) tuple for vertices u and v."""
        return (self._origin_vertex, self._destination_vertex)

    def __str__(self):
        return f'({str(self._origin_vertex)}, {str(self._destination_vertex)})'


class Graph:

    def __init__(self, edges_list=None):
        self._graph = {}
        if edges_list:
            self.create_graph_from_edges_list(edges_list)

    def _clear(self):
        self._graph = {}

    def _insert_vertex(self, vertex):
        self._graph[vertex] = set()

    def _append_graph_dict(self, vertex, edge):
        try:
            self._graph[vertex].add(edge)
        except KeyError:  # totally new vertex in the graph
            self._graph[vertex] = {edge}

    def _insert_edge(self, u, v):
        edge = Edge(u, v)
        self._append_graph_dict(u, edge)
        self._append_graph_dict(v, edge)

    def create_graph_from_edges_list(self, edges_list):
        self._clear()
        all_vertices = set()

        for vertex_1, vertex_2 in edges_list:
            all_vertices.add(vertex_1)
            all_vertices.add(vertex_2)

        # print(all_vertices)
        vertices_dict = {}
        for vertex in all_vertices:
            try:
                vert, color = vertex.split(':')
                vertices_dict[vertex] = Vertex(vert, color)
                continue
            except ValueError:
                pass

            vertices_dict[vertex] = Vertex(vertex)

        for vertex_1, vertex_2 in edges_list:
            self._insert_edge(vertices_dict[vertex_1], vertices_dict[vertex_2])

    def create_graph_from_file(self, path):
        self._clear()
        edges_list = list()
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                edges_list.append(
                    (line[:line.index(':')], line[line.index(':') + 2:]))
        self.create_graph_from_edges_list(edges_list)

    def _get_all_vertices(self):
        return list(self._graph.keys())

    def _get_connected_vertices(self, vertex):
        connected_vertices = set()
        for edge in self._graph[vertex]:
            vertex_1, vertex_2 = edge.get_edge_endpoints()
            if vertex_1 != vertex:
                connected_vertices.add(vertex_1)
            elif vertex_2 != vertex:
                connected_vertices.add(vertex_2)
        return connected_vertices

    def _is_available(self, v, color):
        for vertex in self._get_connected_vertices(v):
            if vertex.get_color() == color:
                return False
        return True

    def _recurse(self, index, max_color):
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

    def color_graph(self, max_color):
        if self._recurse(0, max_color):
            return [str(vertex) for vertex in self._get_all_vertices()]

    def __str__(self):
        string_repr = ''
        for key, value in self._graph.items():
            string_repr += f'{key} : {", ".join([str(vertex) for vertex in value])}' + '\n'
        return string_repr[:-1]
