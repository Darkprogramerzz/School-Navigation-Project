import heapq
import networkx as nx
import matplotlib.pyplot as plt

#STEP 1: Define your school layout ---
school_map = {
    "Entrance-1": {"Hallway-1": 5,"Hallway-2": 5,"Entrance-2": 10,"Entrance-4": 10},
    "Entrance-2": {"Hallway-1": 5,"Hallway-3": 5,"Entrance-1": 10,"Entrance-3": 10},
    "Entrance-3": {"Hallway-3": 5,"Hallway-4": 5,"Entrance-2": 10,"Entrance-4": 10},
    "Entrance-4": {"Hallway-2": 5,"Hallway-4": 5,"Entrance-1": 10,"Entrance-3": 10},
    "Hallway-1": {"Entrance-1": 5,"Entrance-2": 5,},
    "Hallway-2": {"Entrance-1": 3,"Entrance-4": 3,},
    "Hallway-3": {"Entrance-3": 3,"Entrance-2": 3,},
    "Hallway-4": {"Entrance-3": 5,"Entrance-4": 5,},

    "10-c":{"Hallway-1": 2,"12-c":1},
    "12-c":{"10-c":1},
    "12-b":{"12-a":1},
    "12-a":{"Hallway-1": 2,"12-b":1},

    "Psychology Lab":{"11-c":1},
    "11-c":{"Psychology Lab":1,"Hallway-1":2},
    "10-b":{"10-a":1,"Hallway-1":2},
    "10-a":{"10-b":1}


}


# STEP 2: Dijkstra’s Algorithm (Shortest Path) ---
def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    node = end
    while node is not None:
        path.insert(0, node)
        node = previous[node]
    return path, distances[end]


# STEP 3: Create the Graph for Visualization ---
G = nx.Graph()
for room, connections in school_map.items():
    for connected_room, distance in connections.items():
        G.add_edge(room, connected_room, weight=distance)


# STEP 4:input ---
print("Available rooms:", ", ".join(G.nodes))
start = input("Enter starting room: ")
end = input("Enter destination room: ")

if start not in G.nodes or end not in G.nodes:
    print("❌ Invalid room name. Please enter names exactly as shown.")
    exit()

#  STEP 5:shortest path ---
path, total_distance = dijkstra(school_map, start, end)
print(f"\n✅ Shortest path from {start} to {end}: {' → '.join(path)}")
print(f"Total distance: {total_distance} units\n")

# --- STEP 6: Draw visual map ---
plt.figure(figsize=(10,15))

#  set positions 
positions = {
    "Entrance-1": (0, 0),
    "Entrance-2":(4,0),
    "Entrance-3":(4,4),
    "Entrance-4":(0,4),
    "Hallway-1": (2, 0),
    "Hallway-2": (0,2),
    "Hallway-3": (4, 2),
    "Hallway-4": (2,4),

    "10-c":(3,0.4),
    "12-c":(3.5,0.4),
    "12-a":(3,-0.4),
    "12-b":(3.5,-0.4),

    "Psychology Lab":(1,0.4),
    "11-c":(1.5,0.4),
    "10-a":(1,-0.4),
    "10-b":(1.5,-0.4)
    
}

# Draw base map
nx.draw_networkx_edges(G, pos=positions, width=2, alpha=0.3,edge_color='blue')
nx.draw_networkx_nodes(G, pos=positions, node_color='skyblue', node_size=1000)
nx.draw_networkx_labels(G, pos=positions, font_size=8, font_weight='bold')

# Highlight the shortest path in red
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos=positions, edgelist=path_edges, width=5, edge_color='red')

# Add edge labels (distances)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels)

plt.title(" School Floor Navigation System")
plt.text(1, -1, f"\n✅ Shortest path from {start} to {end}: {' → '.join(path)}", fontdict=None)
plt.axis('off')
plt.show()
