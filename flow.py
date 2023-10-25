import graph as gr

SOURCE, EG, SINK = 0, 53, 55

def main():
    """
    Main finds the maximum flow in a graph using the Ford-Fulkerson algorithm.
    It first builds a graph, then finds a path in the graph using bfs, and then 
    augments the path with the maximum possible flow, and repeats until no more 
    paths can be found. Finally, it finds the minimum cut of the graph and prints 
    the endpoints and their capacities, as well as the total flow.
    """
    graph = build_graph()

    # Find a path in the graph using bfs
    total_flow = 0
    path, flow = bfs(graph)
    
    while path:
        total_flow += flow
        augment(path, flow, graph)

        path, flow = bfs(graph)

    visited, endpoints = bfs(graph, min_cut=True)
    for u, v, c in sorted(endpoints, key=lambda x: x[0]):
        if v not in visited:
            print(u, v, c)

    print(total_flow)

def build_graph():
    """
    Builds a graph object from a file containing node and edge information.
    The file should be in the format specified in the project description.

    Returns:
        the graph object.
    """
    global SOURCE, SINK
    graph = gr.Graph()
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

    graph.add_edge(EG, SINK)

    # To check if reducing the capacities on the lines from division 4W to
    # divisions 48 and 49, set the formel argument of run to true.
    graph = decrease_capacities(graph, run=True)
    
    return graph

def decrease_capacities(graph, run=False):
    """
    Decrease the capacities on the lines from division 4W to divisions 48 and
    49. This allows for analyzing the effects of this change in capacities.

    Args:
        graph: a Graph object representing the graph to search
        if run is False: simply return the graph object unchanged
        if min_cut is True: update the capacities for the two lines

    Returns:
        the graph object.
    """
    if run:
        MINSK, N48, N49 = 20, 21, 23
        MINSK_TO_N48, MINSK_TO_N49 = 20, 20

        graph.update_path_weight(MINSK, N48, MINSK_TO_N48)
        graph.update_path_weight(MINSK, N49, MINSK_TO_N49)
    
    return graph


def bfs(graph, min_cut=False):
    """
    Perform a breadth-first search on a graph to find the shortest path from 
    SOURCE to SINK. If min_cut is True, return the minimum cut of the graph 
    instead.
    
    Args:
        graph: a Graph object representing the graph to search
        min_cut: a boolean indicating whether to return the minimum cut of the 
                 graph
    
    Returns:
        if min_cut is False: a tuple containing the shortest path from SOURCE 
            to SINK and its flow
        if min_cut is True: a tuple containing the visited nodes and the 
            endpoints of the minimum cut
    """
    queue = [(SOURCE, [SOURCE], float("inf"))]
    visited, endpoints = [SOURCE], []
    
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
            elif capacity == 0 and adj_node not in visited:
                original_capacity = graph.get_path_capacity(adj_node, node)
                endpoints.append((node, adj_node, original_capacity//2))
    
    return (visited, endpoints) if min_cut else ([], 0)

def augment(path, flow, graph):
    """
    Augments the flow along a given path in a graph.

    Args:
        path (list): A list of nodes representing the path.
        flow (int): The amount of flow to augment.
        graph (Graph): The graph object.

    Returns:
        None
    """
    for i in range(len(path)-1):
        n1, n2 = path[i], path[i+1]
        forward_edge_new_cap  = graph.get_path_capacity(n1, n2) - flow
        backward_edge_new_cap = graph.get_path_capacity(n2, n1) + flow
        graph.update_path_weight(n1, n2, forward_edge_new_cap)
        graph.update_path_weight(n2, n1, backward_edge_new_cap)

def parse_file(filename):
    """
    Parses a file containing information about nodes and edges in a graph.

    Args:
        filename (str): The path to the file to be parsed.

    Returns:
        tuple: A tuple containing two lists. The first list contains the 
        names of the nodes in the graph, and the second list contains tuples 
        representing the edges in the graph. Each edge tuple contains three 
        integers: the source node, the destination node, and the capacity of 
        the edge.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    nodes, edges = [], []
    n = int(lines[0]) # parse the number of nodes
    nodes = [lines[i].strip() for i in range(1, n + 1)] # parse node names
    m = int(lines[n + 1]) # parse the number of arcs/edges

    for i in range(n + 2, n + 2 + m): # parse arcs
        u, v, c = map(int, lines[i].split())
        edges.append((u, v, c))

    return nodes, edges

if __name__ == "__main__":
    main()
