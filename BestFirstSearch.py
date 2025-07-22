import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue

def best_first_search(graph, start, goal, heuristic):
    visited = set()  # Set to keep track of visited nodes
    pq = PriorityQueue()
    pq.put((heuristic[start], start))  # Push the start node with its heuristic value

    result = f"Starting Best First Search from '{start}' to '{goal}'\n"
    result += f"Heuristic values: {heuristic}\n"
    
    while not pq.empty():
        current_heuristic, current_node = pq.get()  # Get the node with the lowest heuristic value
        result += f"\nExploring node: {current_node} with heuristic: {current_heuristic}\n"

        if current_node in visited:
            result += f"Node '{current_node}' already visited. Skipping.\n"
            continue
        
        visited.add(current_node)
        result += f"Visited nodes: {visited}\n"

        if current_node == goal:
            result += "Goal reached!"
            return result
        
        # Explore neighbors
        if current_node not in graph:
            result += f"Node '{current_node}' has no neighbors.\n"
            continue
        
        for neighbor, cost in graph[current_node]:
            if neighbor not in visited:
                result += f"Adding neighbor '{neighbor}' to the priority queue with heuristic {heuristic[neighbor]}\n"
                pq.put((heuristic[neighbor], neighbor))
            else:
                result += f"Neighbor '{neighbor}' already visited.\n"

    result += "Goal not reachable."
    return result

def run_algorithm():
    # Get inputs from GUI
    try:
        graph_input = graph_entry.get("1.0", tk.END).strip()
        graph = eval(graph_input)
        heuristic_input = heuristic_entry.get("1.0", tk.END).strip()
        heuristic = eval(heuristic_input)
        start = start_entry.get().strip()
        goal = goal_entry.get().strip()

        # Validate inputs
        if not graph or not heuristic or not start or not goal:
            raise ValueError("All fields must be filled.")

        # Run the algorithm
        result = best_first_search(graph, start, goal, heuristic)

        # Update the result display
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, result)  # Insert new result

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Create the main GUI window
root = tk.Tk()
root.title("Best First Search GUI")

# Graph input
tk.Label(root, text="Graph (Adjacency List):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
graph_entry = tk.Text(root, height=5, width=50)
graph_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Heuristic input
tk.Label(root, text="Heuristic Values (Dictionary):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
heuristic_entry = tk.Text(root, height=5, width=50)
heuristic_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Start and goal nodes
tk.Label(root, text="Start Node:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
start_entry = tk.Entry(root, width=25)
start_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Goal Node:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
goal_entry = tk.Entry(root, width=25)
goal_entry.grid(row=5, column=1, padx=10, pady=5)

# Run button
run_button = tk.Button(root, text="Run Best First Search", command=run_algorithm)
run_button.grid(row=6, column=0, columnspan=2, pady=10)

# Result display (scrollable Text widget)
tk.Label(root, text="Result:").grid(row=7, column=0, sticky="nw", padx=10, pady=5)
result_text = tk.Text(root, width=50, height=10, bg="white", relief="sunken")
result_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.grid(row=8, column=2, sticky="ns", padx=5)
result_text.config(yscrollcommand=scrollbar.set)

# Run the GUI loop
root.mainloop()










# from queue import PriorityQueue

# # Best First Search Algorithm
# def best_first_search(graph, start, goal, heuristic):
#     print(f"Starting Best First Search from '{start}' to '{goal}'")
#     print(f"Heuristic values: {heuristic}")
    
#     visited = set()  # Set to keep track of visited nodes
#     pq = PriorityQueue()
#     pq.put((heuristic[start], start))  # Push the start node with its heuristic value

#     while not pq.empty():
#         # Debugging: Check what's in the priority queue
#         print("\nPriority Queue:", list(pq.queue))
        
#         current_heuristic, current_node = pq.get()  # Get the node with the lowest heuristic value
#         print(f"\nExploring node: {current_node} with heuristic: {current_heuristic}")
        
#         if current_node in visited:
#             print(f"Node '{current_node}' already visited. Skipping.")
#             continue
        
#         visited.add(current_node)
#         print(f"Visited nodes: {visited}")

#         if current_node == goal:
#             print("Goal reached!")
#             return
        
#         # Explore neighbors
#         if current_node not in graph:
#             print(f"Node '{current_node}' has no neighbors.")
#             continue
        
#         for neighbor, cost in graph[current_node]:
#             if neighbor not in visited:
#                 print(f"Adding neighbor '{neighbor}' to the priority queue with heuristic {heuristic[neighbor]}")
#                 pq.put((heuristic[neighbor], neighbor))
#             else:
#                 print(f"Neighbor '{neighbor}' already visited.")

#     print("Goal not reachable.")
#     return

# # Function to take user input
# def take_input():
#     # Number of nodes
#     n = int(input("Enter number of nodes: "))

#     # Graph input
#     graph = {}
#     for i in range(n):
#         node = input(f"Enter node {i+1}: ")
#         graph[node] = []
#         neighbors = int(input(f"Enter number of neighbors for {node}: "))
#         for j in range(neighbors):
#             neighbor = input(f"Enter neighbor {j+1} for {node}: ")
#             cost = int(input(f"Enter cost to reach {neighbor}: "))
#             graph[node].append((neighbor, cost))

#     print("\nGraph representation (adjacency list):")
#     print(graph)

#     # Heuristic values input
#     heuristic = {}
#     for i in range(n):
#         node = input(f"Enter node name for heuristic: ")
#         h_value = int(input(f"Enter heuristic value for {node}: "))
#         heuristic[node] = h_value

#     print("\nHeuristic values:")
#     print(heuristic)

#     start = input("Enter start node: ")
#     goal = input("Enter goal node: ")
    
#     return graph, start, goal, heuristic

# # Main function
# if __name__ == "__main__":
#     graph, start, goal, heuristic = take_input()
#     best_first_search(graph, start, goal, heuristic)