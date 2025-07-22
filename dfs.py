import pygame
import sys
from collections import deque

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)

def dfs_visualize(screen, font, adj, V, s, nodes):
    visited = [False] * V
    result = []
    stack = [s]
    visited[s] = True

    while stack:
        pygame.event.pump()  # Keep the window responsive
        v = stack.pop()
        result.append(v)
        draw(screen, font, nodes, stack, result, v)
        pygame.time.delay(1000)  # Delay for visualization

        for i in reversed(adj[v]):
            if not visited[i]:
                stack.append(i)
                visited[i] = True
                draw(screen, font, nodes, stack, result, i)
                pygame.time.delay(1000)  # Delay for visualization

    draw(screen, font, nodes, [], result, -1)  # Final state
    pygame.time.delay(2000)  # Longer delay at the end
    return result

def draw(screen, font, nodes, stack, result, current_node):
    screen.fill((255, 255, 255))

    for edge in edges:
        pygame.draw.line(screen, (0, 0, 0), nodes[edge[0]].center, nodes[edge[1]].center, 2)

    for i, node in enumerate(nodes):
        color = (0, 0, 255) if i in result else (0, 0, 0)
        pygame.draw.ellipse(screen, color, node)
        label = font.render(str(i), True, (255, 255, 255))
        screen.blit(label, (node.x + 5, node.y + 5))

    if current_node >= 0:
        pygame.draw.ellipse(screen, (255, 0, 0), nodes[current_node], 3)

    draw_stack(screen, font, stack, result)
    pygame.display.flip()

def draw_stack(screen, font, stack, result):
    stack_label = font.render("Stack: " + " ".join(map(str, stack)), True, (0, 0, 0))
    result_label = font.render("Result: " + " ".join(map(str, result)), True, (0, 0, 0))
    screen.blit(stack_label, (10, 10))
    screen.blit(result_label, (10, 40))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Graph Editor")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    nodes = []
    global edges
    edges = []
    g = Graph(0)
    is_creating_edge = False
    first_node = -1
    node_radius = 15
    input_active = False
    input_text = ""
    dfs_result = []
    dfs_complete = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                clicked_on_node = False
                for i, node in enumerate(nodes):
                    if node.collidepoint(mouse_pos):
                        clicked_on_node = True
                        if is_creating_edge:
                            g.add_edge(first_node, i)
                            edges.append((first_node, i))
                            is_creating_edge = False
                        else:
                            first_node = i
                            is_creating_edge = True
                        break

                if not clicked_on_node:
                    node = pygame.Rect(mouse_pos[0] - node_radius, mouse_pos[1] - node_radius, node_radius * 2, node_radius * 2)
                    nodes.append(node)
                    g.V += 1
                    g.adj.append([])

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            start = int(input_text)
                            if 0 <= start < g.V:
                                dfs_result = dfs_visualize(screen, font, g.adj, g.V, start, nodes)
                                dfs_complete = True
                            else:
                                print("Invalid starting node. Node index out of bounds.")
                        except ValueError:
                            print("Invalid input. Please enter a valid node index.")
                        input_active = False
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                elif event.key == pygame.K_SPACE:
                    input_active = True

        screen.fill((255, 255, 255))

        for edge in edges:
            pygame.draw.line(screen, (0, 0, 0), nodes[edge[0]].center, nodes[edge[1]].center, 2)

        for i, node in enumerate(nodes):
            color = (0, 0, 255) if i in dfs_result else (0, 0, 0)
            pygame.draw.ellipse(screen, color, node)
            label = font.render(str(i), True, (255, 255, 255))
            screen.blit(label, (node.x + 5, node.y + 5))

        if input_active:
            input_label = font.render("Enter starting node: " + input_text, True, (0, 0, 0))
            screen.blit(input_label, (10, 70))

        if dfs_complete:
            draw_stack(screen, font, [], dfs_result)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



"""import pygame
import sys
from collections import deque

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)

def dfs_util(adj, v, visited):
    visited[v] = True
    print(v, end=" ")
    for i in adj[v]:
        if not visited[i]:
            dfs_util(adj, i, visited)

def dfs(adj, V, s):
    visited = [False] * V
    dfs_util(adj, s, visited)
    print()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Graph Editor")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    nodes = []
    edges = []
    g = Graph(0)
    is_creating_edge = False
    first_node = -1
    node_radius = 15  # Adjust the radius for smaller nodes

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                clicked_on_node = False
                for i, node in enumerate(nodes):
                    if node.collidepoint(mouse_pos):
                        clicked_on_node = True
                        if is_creating_edge:
                            g.add_edge(first_node, i)
                            edges.append((first_node, i))
                            is_creating_edge = False
                        else:
                            first_node = i
                            is_creating_edge = True
                        break

                if not clicked_on_node:
                    node = pygame.Rect(mouse_pos[0] - node_radius, mouse_pos[1] - node_radius, node_radius * 2, node_radius * 2)
                    nodes.append(node)
                    g.V += 1
                    g.adj.append([])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start = int(input("Enter the starting node for DFS: "))
                if 0 <= start < g.V:
                    print(f"DFS traversal starting from node {start}: ", end="")
                    dfs(g.adj, g.V, start)
                else:
                    print("Invalid starting node. Node index out of bounds.")

        screen.fill((255, 255, 255))

        for edge in edges:
            pygame.draw.line(screen, (0, 0, 0), nodes[edge[0]].center, nodes[edge[1]].center, 2)

        for i, node in enumerate(nodes):
            pygame.draw.ellipse(screen, (0, 0, 0), node)  # Black nodes
            label = font.render(str(i), True, (255, 255, 255))  # White labels
            screen.blit(label, (node.x + node_radius - label.get_width() // 2, node.y + node_radius - label.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()"""