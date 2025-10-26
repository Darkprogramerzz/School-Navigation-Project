import customtkinter as ctk
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# GitHub Copilot
# Requires: pip install customtkinter
ROOMS = [
    "Entrance-1", "Entrance-2", "Entrance-4",
    "Entrance-3", "10-c", "11-c", "12-c", "Coodinator", "12-b", "12-a",
    "10-b", "Psychology Lab", "Home Sci.Lab", "10-a", "Lift-1", "Lift-2", "Room3",
    "Staircase-5", "Conserler", "Resource", "Restroom-1",  "Restroom-2", "Staffroom-2", "Staffroom", "11-b",
    "11-a", "9-b", "AV room", "Computer Lab", "Launguage Lab"
]

# sort case-insensitively
ROOMS_SORTED = sorted(ROOMS, key=lambda s: s.lower())

# color scheme
PURPLE = "#5B2C6F"
YELLOW = "#F7DC6F"
TEXT_ON_YELLOW = "#310531"  # dark purple for readability on yellow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BHIS Navigation")
        self.geometry("520x300")
        self.resizable(False, False)

        # overall purple background frame
        self.configure(fg_color=PURPLE)
        self.main_frame = ctk.CTkFrame(self, fg_color=PURPLE, corner_radius=5)
        self.main_frame.pack(expand=True, fill="both", padx=18, pady=18)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="School Navigation", text_color=YELLOW, font=ctk.CTkFont(size=25, weight="bold")
        )
        self.title_label.pack(pady=(6, 14))

        # Dropdowns container
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color=PURPLE, border_width=2, border_color=YELLOW)
        self.controls_frame.pack(pady=4, padx=8, fill="x")

        # Starting room
        self.start_label = ctk.CTkLabel(self.controls_frame, text="Starting Room", text_color=YELLOW, font=ctk.CTkFont(size=16))
        self.start_label.grid(row=0, column=0, sticky="w", padx=(6, 12), pady=6)
        self.start_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=ROOMS_SORTED,
            fg_color=YELLOW,
            button_color=PURPLE,
            text_color=TEXT_ON_YELLOW,
            dynamic_resizing=False,
            width=300,
            button_hover_color="#6B239D",
        )
        self.start_menu.set(ROOMS_SORTED[0])
        self.start_menu.grid(row=0, column=1, sticky="w", pady=6)

        # Destination room
        self.dest_label = ctk.CTkLabel(self.controls_frame, text="Destination Room", text_color=YELLOW, font=ctk.CTkFont(size=16))
        self.dest_label.grid(row=1, column=0, sticky="w", padx=(6, 12), pady=6)
        self.dest_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=ROOMS_SORTED,
            fg_color=YELLOW,
            button_color=PURPLE,
            text_color=TEXT_ON_YELLOW,
            dynamic_resizing=False,
            width=300,
            button_hover_color="#6B239D",
        )
        self.dest_menu.set(ROOMS_SORTED[1] if len(ROOMS_SORTED) > 1 else ROOMS_SORTED[0])
        self.dest_menu.grid(row=1, column=1, sticky="w", pady=6)

        # Submit button
        self.submit_btn = ctk.CTkButton(
            self.main_frame,
            text="SHOW PATH",
            fg_color=YELLOW,
            hover=False,
            text_color=PURPLE,
            command=self.save_selection,
            width=160,
            hover_color="#E6C200",
        )
        self.submit_btn.pack(pady=(14, 8))

        # Label to show saved value
        self.result_label = ctk.CTkLabel(self.main_frame, text="", text_color=YELLOW)
        self.result_label.pack(pady=6)

        # will hold the saved tuple (start, destination)
        self.selected_rooms = None

    def save_selection(self):
        start = self.start_menu.get()
        end = self.dest_menu.get()
        school_map = {
            "Entrance-1": {"Entrance-2": 10,"Entrance-4": 10},
            "Entrance-2": {"Entrance-1": 10,"Entrance-3": 10},
            "Entrance-3": {"Entrance-2": 10,"Entrance-4": 10},
            "Entrance-4": {"Entrance-1": 10,"Entrance-3": 10},


            "10-c":{"11-c": 4,"12-c":1},
            "12-c":{"10-c":1,"Coodinator":3},
            "12-b":{"12-a":1,"Entrance-2":3},
            "12-a":{"10-b": 4,"12-b":1},

            "Psychology Lab":{"11-c":1,},
            "Home Sci.Lab":{"Psychology Lab":1,"Entrance-1":3},
            "11-c":{"Psychology Lab":1,},
            "10-b":{"10-a":1,},
            "10-a":{"10-b":1,"Entrance-1":3},

            "Coodinator":{"Entrance-2":1},
            "Lift-1":{"Entrance-2":1},
            "Lift-2":{"Room3":1},
            "Staircase-5":{"Lift-2":1},
            "Conserler":{"Entrance-1":1},
            "Resource":{"Coodinator":2},
            "Restroom-1":{"Resource":2},
            "Room1":{"Restroom-1":2,"Entrance-3":3},
            "Room4":{"Entrance-3":3},
            "Room5":{"Room4":2},
            "Room6":{"Room5":2},
            "Room7":{"Room6":2,"Entrance-4":3},
            "Room2":{"Room1":2},
            "Room3":{"Room2":2},
            "Restroom-2":{"Home Sci.Lab":2},
            "Staffroom-2":{"Restroom-2":2,"Entrance-4":3,"Staircase-5":2},
            "Staffroom":{"11-b":2,"Entrance-2":3},
            "11-b":{"Staffroom":1},
            "11-a":{"11-b":1},
            "9-b":{"11-a":1,"Entrance-3":3},

            "AV room":{"Entrance-1":3},
            "Computer Lab":{"AV room":4},
            "Launguage Lab":{"Entrance-4":3,"Computer Lab":4},
            
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

        for room, connections in list(school_map.items()):
            for connected_room, distance in connections.items():
                if connected_room not in school_map:
                    school_map[connected_room] = {}
                if room not in school_map[connected_room]:
                    school_map[connected_room][room] = distance


        # STEP 4:input ---
        #print("Available rooms:", ", ".join(G.nodes))
        #start = input("Enter starting room: ")
        #end = input("Enter destination room: ")

        if start not in G.nodes or end not in G.nodes:
            print("❌ Invalid room name. Please enter names exactly as shown.")
            exit()

        #  STEP 5:shortest path ---
        path, total_distance = dijkstra(school_map, start, end)
        print(f"\n✅ Shortest path from {start} to {end}: {' → '.join(path)}")
        print(f"Total distance: {total_distance} units\n")

        # --- STEP 6: Draw visual map ---
        plt.figure(figsize=(30,30))
        img = mpimg.imread("map1.jpg")  # <-- change filename if needed
        plt.imshow(img, extent=[0, 16, 0, 10], alpha=0.8)  

        #  set positions 
        positions = {
            "Entrance-1": (3.7, 1.1),
            "Entrance-2":(14.7,1.5),
            "Entrance-3":(14,8.2),
            "Entrance-4":(1.2,8),

            "10-c":(9.2,3.3),
            "12-c":(7.7,3.3),
            "12-a":(8,0.9),
            "12-b":(9.2,0.9),

            "Psychology Lab":(5.4,3.3),
            "11-c":(6.6,3.3),
            "10-a":(5.5,0.9),
            "10-b":(6.6,0.9),
            "Home Sci.Lab":(4.1,4.1),

            "Coodinator":(11.6,3.2),
            "Conserler":(1.9,1.1),
            "Lift-1":(12.9,0.9),
            "Resource":(11.6,4.2),
            "Restroom-1":(11.6,5.1),
            "Room1":(11.6,8.2),
            "Room2":(11.6,6.2),
            "Room3":(9.1,6.2),
            "Room4":(7.7,8.2),
            "Room5":(5.8,8.2), 
            "Room6":(4.1,8.1),
            "Room7":(2.7,8.1),
            "Lift-2":(7.7,6.2),
            "Staircase-5":(6.2,6.2),
            "Restroom-2":(4.2,5),
            "Staffroom-2":(4.1,6.2),
            "Staffroom":(14.3,3.3),
            "11-b":(14.3,4.4),
            "11-a":(14.4,5.25),
            "9-b":(14.45,6.5),

            "AV room":(1,4.3),
            "Computer Lab":(1,5.9),
            "Launguage Lab":(1,6.8),

        }

        # Draw base map
        nx.draw_networkx_edges(G, pos=positions, width=2, alpha=0.3,edge_color='blue')
        nx.draw_networkx_nodes(G, pos=positions, node_color="Gold", node_size=1000)
        for node in G.nodes:
            if node == "Entrance-1" or node == "Entrance-2" or node == "Entrance-3" or node == "Entrance-4" or node == "Staircase-5":
                nx.draw_networkx_nodes(G, pos=positions, nodelist=[node], node_color="mediumpurple", node_size=1200)
            if node == "Restroom-1" or node == "Restroom-2" or node == "Lift-1" or node == "Lift-2":
                nx.draw_networkx_nodes(G, pos=positions, nodelist=[node], node_color="greenyellow", node_size=1000)
            if node == "Computer Lab" or node == "Launguage Lab" or node == "AV room" or node == "Home Sci.Lab" or node == "Psychology Lab" :
                nx.draw_networkx_nodes(G, pos=positions, nodelist=[node], node_color="skyblue", node_size=1000)
            if node == "Coodinator" or node == "Conserler" or node == "Resource" or node == "Staffroom" or node == "Staffroom-2":
                nx.draw_networkx_nodes(G, pos=positions, nodelist=[node], node_color="plum", node_size=1000)
        nx.draw_networkx_labels(G, pos=positions, font_size=8, font_weight='bold')

        # Highlight the shortest path in red
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos=positions, edgelist=path_edges, width=5, edge_color='Green',arrows=True,arrowstyle='-|>',arrowsize=30)

        # Add edge labels (distances)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels)

        plt.title(" BHIS Navigator",fontsize=25, fontweight='bold')
        plt.text(-1, 9, "Classrooms:Yellow", color="gold", fontsize=10, fontweight='bold')
        plt.text(-1, 9.2, "Enter Points:Purple", color="mediumpurple", fontsize=10, fontweight='bold')
        plt.text(-1, 9.4, "Labs:Blue", color="skyblue", fontsize=10, fontweight='bold')
        plt.text(-1, 9.6, "Utilities:Light pink", color="plum", fontsize=10, fontweight='bold')
        plt.text(5,0,f"\n Shortest path from {start} to {end}: {' → '.join(path)}", fontsize=15, fontweight='bold')
        plt.axis('off')
        plt.show()



if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # keeps native light/dark behavior
    app = App()
    app.mainloop()