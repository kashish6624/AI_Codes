import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
NODE_RADIUS = 20
WHITE = (255, 255, 255)
BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
FPS = 30
FONT = pygame.font.Font(None, 24)

# Define Button Class
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = text
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Define Node Class
class Node:
    def __init__(self, x, y, name=None, value=None):
        self.x = x
        self.y = y
        self.name = name  # Max or Min
        self.value = value  # Leaf node value
        self.children = []  # Child nodes
        self.selected = False  # For dragging
        self.color = BLUE
        self.pruned = False  # Added to mark pruned nodes

    def draw(self, screen):
        color = RED if self.pruned else self.color  # Change color if pruned
        pygame.draw.circle(screen, color, (self.x, self.y), NODE_RADIUS)
        label = f"{self.name}" if self.value is None else f"{self.value}"
        text = FONT.render(label, True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        
    def is_hovered(self, pos):
        return (self.x - pos[0])**2 + (self.y - pos[1])**2 <= NODE_RADIUS**2

# Check if the node is a leaf (terminal node)
def is_terminal(node):
    return len(node.children) == 0

# Minimax function with Alpha-Beta Pruning
def minimax(node, depth, alpha, beta, maximizingPlayer):
    print(f"\n{'Max' if maximizingPlayer else 'Min'} Node at Depth {depth}: (Alpha={alpha}, Beta={beta})")

    if depth == 0 or is_terminal(node):
        print(f"Leaf Node Value: {node.value}")
        return node.value  # Return value at leaf node

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in node.children:
            eval = minimax(child, depth - 1, alpha, beta, False)  # Minimizer's turn next
            maxEval = max(maxEval, eval)
            alpha = max(alpha, maxEval)
            print(f"Max Node Updated: Value={maxEval}, Alpha={alpha}, Beta={beta}")
            if beta <= alpha:
                node.pruned = True  # Mark node as pruned
                print("Pruning occurs at Max Node")
                break  # Beta cut-off (Pruning)
        node.value = maxEval  # Set node value for Max
        return maxEval
    else:
        minEval = float('inf')
        for child in node.children:
            eval = minimax(child, depth - 1, alpha, beta, True)  # Maximizer's turn next
            minEval = min(minEval, eval)
            beta = min(beta, minEval)
            print(f"Min Node Updated: Value={minEval}, Alpha={alpha}, Beta={beta}")
            if beta <= alpha:
                node.pruned = True  # Mark node as pruned
                print("Pruning occurs at Min Node")
                break  # Alpha cut-off (Pruning)
        node.value = minEval  # Set node value for Min
        return minEval

# Define Minimax GUI Class
class MinimaxPygame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minimax Tree GUI")
        self.clock = pygame.time.Clock()

        self.nodes = []
        self.edges = []  # List of tuples (parent, child)
        self.selected_node = None
        self.mode = None  # Modes: 'create_node', 'create_edge', 'run_minimax'
        self.edge_start_node = None
        self.node_type = "Max"  # Default type for new nodes

        # Create buttons
        self.buttons = [
            Button(10, 10, 120, 40, "Create Max Node", self.set_create_max_node_mode),
            Button(140, 10, 120, 40, "Create Min Node", self.set_create_min_node_mode),
            Button(270, 10, 120, 40, "Create Edge", self.set_create_edge_mode),
            Button(400, 10, 120, 40, "Run Minimax", self.run_minimax)
        ]

    def set_create_max_node_mode(self):
        self.mode = 'create_node'
        self.node_type = "Max"
        self.edge_start_node = None
        print("Mode set to Create Max Node")

    def set_create_min_node_mode(self):
        self.mode = 'create_node'
        self.node_type = "Min"
        self.edge_start_node = None
        print("Mode set to Create Min Node")

    def set_create_edge_mode(self):
        self.mode = 'create_edge'
        self.edge_start_node = None
        print("Mode set to Create Edge")

    def create_node(self, pos):
        node = Node(pos[0], pos[1], name=self.node_type)
        self.nodes.append(node)
        print(f"Created {node.name} node at {pos}")

    def create_edge(self, parent, child):
        if child not in parent.children:
            parent.children.append(child)
            self.edges.append((parent, child))
            print(f"Created edge from {parent.name} to {child.name}")

    def run_minimax(self):
        if not self.nodes:
            print("No nodes to run Minimax on.")
            return
        try:
            depth = int(input("Enter the depth for Minimax: "))
        except ValueError:
            print("Invalid depth input.")
            return

        # Input values for leaf nodes
        for node in self.nodes:
            if not node.children:
                while True:
                    try:
                        value = int(input(f"Enter value for leaf node at ({node.x}, {node.y}): "))
                        node.value = value
                        break
                    except ValueError:
                        print("Invalid input. Please enter an integer.")

        # Assuming the first node is the root
        root_node = self.nodes[0]
        minimax(root_node, depth, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True)
        print(f"Minimax value for root node ({root_node.name}): {root_node.value}")

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def draw_edges(self):
        for parent, child in self.edges:
            pygame.draw.line(self.screen, BLACK, (parent.x, parent.y), (child.x, child.y), 2)

    def draw_nodes(self):
        for node in self.nodes:
            node.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if a button was clicked
                for button in self.buttons:
                    if button.is_clicked(pos):
                        button.callback()
                        return  # Prevent further processing

                if self.mode == 'create_node':
                    self.create_node(pos)

                elif self.mode == 'create_edge':
                    # Check if a node was clicked
                    for node in self.nodes:
                        if node.is_hovered(pos):
                            if not self.edge_start_node:
                                self.edge_start_node = node
                                print(f"Selected parent node: {node.name} at ({node.x}, {node.y})")
                            else:
                                child_node = node
                                if child_node != self.edge_start_node:
                                    self.create_edge(self.edge_start_node, child_node)
                                self.edge_start_node = None
                            break

            elif event.type == MOUSEBUTTONUP:
                pass  # Future enhancements (e.g., dragging nodes)

    def run(self):
        while True:
            self.handle_events()

            self.screen.fill(WHITE)

            # Draw buttons
            self.draw_buttons()

            # Draw edges
            self.draw_edges()

            # Draw nodes
            self.draw_nodes()

            pygame.display.flip()
            self.clock.tick(FPS)

# Run the GUI
if __name__ == "__main__":
    minimax_gui = MinimaxPygame()
    minimax_gui.run()









# class Node:
#     def __init__(self, value=None, name=None):
#         self.value = value  # Holds the node's value
#         self.name = name  # Holds the node's label (Max or Min)
#         self.children = []  # List to hold child nodes

# # Check if the node is a leaf (terminal node)
# def is_terminal(node):
#     return len(node.children) == 0

# # Minimax function with Alpha-Beta Pruning
# def minimax(node, depth, alpha, beta, maximizingPlayer):
#     if depth == 0 or is_terminal(node):
#         return node.value  # Return value at leaf node

#     if maximizingPlayer:
#         maxEval = float('-inf')
#         for child in node.children:
#             eval = minimax(child, depth - 1, alpha, beta, False)  # Minimizer's turn next
#             maxEval = max(maxEval, eval)
#             alpha = max(alpha, maxEval)
#             if beta <= alpha:
#                 break  # Beta cut-off
#         node.value = maxEval  # Set node value for Max
#         return maxEval
#     else:
#         minEval = float('inf')
#         for child in node.children:
#             eval = minimax(child, depth - 1, alpha, beta, True)  # Maximizer's turn next
#             minEval = min(minEval, eval)
#             beta = min(beta, minEval)
#             if beta <= alpha:
#                 break  # Alpha cut-off
#         node.value = minEval  # Set node value for Min
#         return minEval

# # Function to create a tree based on user input
# def create_tree():
#     depth = int(input("Enter the depth of the tree: "))
#     root = Node(name="Max")  # Root is always a Max node

#     def build_tree(node, current_depth):
#         if current_depth == depth:
#             # Leaf node, ask for value
#             node.value = int(input(f"Enter value for leaf node at depth {current_depth}: "))
#             node.name = str(node.value)  # Leaf node name is the value itself
#         else:
#             num_children = int(input(f"Enter number of children for node at depth {current_depth}: "))
#             for i in range(num_children):
#                 if current_depth % 2 == 0:
#                     child = Node(name="Min")  # Alternate between Max and Min
#                 else:
#                     child = Node(name="Max")
#                 node.children.append(child)
#                 build_tree(child, current_depth + 1)

#     build_tree(root, 0)
#     return root

# # Function to print the tree structure
# def print_tree(node, level=0):
#     indent = " " * (8 * level)  # Indent based on the level of the node
#     if node.name in ["Max", "Min"]:
#         print(f"{indent}{node.name} ({node.value if node.value is not None else ''})")
#     else:
#         print(f"{indent}{node.name}")
#     for child in node.children:
#         print_tree(child, level + 1)

# # Example usage
# if __name__ == "__main__":
#     print("Minimax with Alpha-Beta Pruning Tree Input")

#     # Create a tree from user input
#     root = create_tree()

#     # Run the minimax algorithm with alpha-beta pruning
#     depth = int(input("Enter depth to compute Minimax: "))
#     minimax(root, depth=depth, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True)

#     # Print the tree structure
#     print("\nTree Structure:\n")
#     print_tree(root)


# # Function to perform Alpha-Beta pruning
# def alpha_beta(node, depth, alpha, beta, maximizing_player):
#     # Base case: if we've reached a leaf node or max depth
#     if depth == 0 or isinstance(node, int):
#         return node

#     if maximizing_player:
#         max_eval = float('-inf')
#         for child in node:
#             eval = alpha_beta(child, depth - 1, alpha, beta, False)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break  # Beta cut-off
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for child in node:
#             eval = alpha_beta(child, depth - 1, alpha, beta, True)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break  # Alpha cut-off
#         return min_eval

# # Main part of the program
# if __name__ == "__main__":
#     # Example game tree where leaf nodes are scores, and each level alternates between Min and Max
#     tree = [
#         [[3, 5], [6, 9]],  # Sub-tree 1
#         [[1, 2], [0, -1]]  # Sub-tree 2
#     ]

#     # Depth of the tree
#     depth = 3

#     # Call the alpha_beta function
#     best_value = alpha_beta(tree, depth, float('-inf'), float('inf'), True)
    
#     # Output the result
#     print(f"The best possible value for the maximizing player is: {best_value}")
