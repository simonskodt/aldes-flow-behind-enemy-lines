class Graph:
    def __init__(self):
        self.graph = {}
        self.SOURCE = 'ORIGINS'
        self.SINK = 'DESTINATIONS'
        self.add_node(self.SOURCE)
        self.add_node(self.SINK)

    def add_node(self, node):
        if node in self.graph:
            return
        
        self.graph[node] = []

    def add_edge(self, n1, n2, capacity=float('inf')):
        if n1 in self.graph and n2 in self.graph:
            self.graph[n1].append((n2, capacity))
            if n1 not in self.graph[n2]:
                self.graph[n2].append((n1, capacity))

    def get_path_capacity(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            self.add_edge(n1, n2, capacity)
        
        for neighbor, capacity in self.graph[n1]:
            if neighbor == n2:
                return capacity
            
    def update_path_weight(self, n1, n2, new_weight):
        if n2 not in self.graph:
            raise ValueError("Node(s) not in graph")
        
        if n1 not in self.graph:
            return self.add_edge(n1, n2, new_weight)

        adjacent_nodes = self.graph[n1]
        for i, edge in enumerate(adjacent_nodes):
            if n2 == edge[0]:
                adjacent_nodes[i] = (n2, new_weight)
                break 

    def get_adjacent_nodes(self, node):
        return self.graph[node]
    
    def node_has_no_adjacent_nodes(self, node):
        if node not in self.graph:
            return False
        
        return not self.graph[node]
    
    def print_graph(self):
        for node in self.graph:
            print(f"Node: {node}")
            adjacent_nodes = self.graph[node]
            if adjacent_nodes:
                for neighbor, capacity in adjacent_nodes:
                    print(f"  -> Neighbour: {neighbor}, Capacity: {capacity}")
            else:
                print("  (No adjacent nodes)")
