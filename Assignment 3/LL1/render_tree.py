from graphviz import Digraph, dot


def render_graph(vertices: [], edges: []):
    graph = Digraph()
    for vertice in vertices:
        if vertice in ':=':
            graph.node('/=')
            continue
        graph.node(vertice)

    for edge in edges:
        if edge[0] in ':=':
            graph.edge('/=', edge[1])
        elif edge[1] in ':=':
            graph.edge(edge[0], '/=')
        else:
            graph.edge(edge[0], edge[1])

    graph.render('graph', format='png')