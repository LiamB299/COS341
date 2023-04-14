from graphviz import Digraph, dot


def render_graph(vertices: [], edges: []):
    graph = Digraph()
    for vertice in vertices:
        graph.node(vertice)

    for edge in edges:
        graph.edge(edge[0], edge[1])

    graph.render('graph', format='png')