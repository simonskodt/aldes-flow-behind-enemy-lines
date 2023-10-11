import graph as gr

SOURCE, EG, SINK = 0, 53, 55
nodes_lookup = []

def main():
    global SOURCE, SINK
    graph = gr.Graph()
    
    # Setup graph
    nodes_lookup, edges = parse_file("data/rail.txt")
    for i, node in enumerate(nodes_lookup):
        if node == "ORIGINS":
            SOURCE = i
        elif node == "DESTINATIONS":
            SINK = i
        elif node == "EG":
            EG = i
        graph.add_node(i)
    for (fromN, toN, cap) in edges:
        if cap == -1:
            cap = float('inf')
        graph.add_edge(fromN, toN, cap)
    #graph.pretty_print()
    graph.add_edge(EG, SINK)

    # Find a path in the graph
    total_flow = 0
    path, flow = bfs(graph)
    
    while path:
        total_flow += flow
        augment(path, flow, graph)

        path, flow = bfs(graph)

def bfs(graph):
    queue = [(SOURCE, [SOURCE], float("inf"))]
    visited = [SOURCE]
    
    while queue:
        node, path, cur_flow = queue.pop(0)
        adj_nodes = graph.get_adjacent_nodes(node)

        for adj_node, capacity in adj_nodes:
            if adj_node not in visited and capacity > 0:
                flow = min(capacity, cur_flow)
                queue.append((adj_node, path + [adj_node], flow))
                visited.append(adj_node)

                if adj_node == SINK:
                    return path + [SINK], flow
    
    return [], 0

def augment(path, flow, graph):
    for i in range(len(path)-1):
        n1, n2 = path[i], path[i+1]
        forward_edge_new_cap  = graph.get_path_capacity(n1, n2) - flow
        backward_edge_new_cap = graph.get_path_capacity(n2, n1) + flow
        # TODO: Remove from graph if new cap is under 0
        graph.update_path_weight(n1, n2, forward_edge_new_cap)
        graph.update_path_weight(n2, n1, backward_edge_new_cap)

def parse_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    nodes, edges = [], []
    # Parse the number of nodes
    n = int(lines[0])
    # Parse node names
    nodes = [lines[i].strip() for i in range(1, n + 1)]
    
    # Parse the number of arcs
    m = int(lines[n + 1])

    # Parse arcs
    for i in range(n + 2, n + 2 + m):
        u, v, c = map(int, lines[i].split())
        edges.append((u, v, c))

    return nodes, edges

if __name__ == "__main__":
    main()
