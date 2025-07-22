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

def bfs_visualize(screen, font, adj, V, s, nodes):
    visited = [False] * V
    queue = deque([s])
    visited[s] = True
    result = []
    final_queue = []

    while queue:
        pygame.event.pump()  # Keep the window responsive
        v = queue.popleft()
        result.append(v)
        current_step = list(queue)  # Save current state of the queue
        draw(screen, font, nodes, current_step, result, v)
        pygame.time.delay(1000)  # Delay for visualization

        for i in adj[v]:
            if not visited[i]:
                visited[i] = True
                queue.append(i)
                current_step = list(queue)  # Save current state of the queue
                draw(screen, font, nodes, current_step, result, i)
                pygame.time.delay(1000)  # Delay for visualization

        final_queue = list(queue)  # Save the final state of the queue

    draw(screen, font, nodes, [], result, -1)  # Final state
    pygame.time.delay(2000)  # Longer delay at the end
    return result, final_queue

def draw(screen, font, nodes, queue, result, current_node):
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

    draw_queue(screen, font, queue, result)
    pygame.display.flip()

def draw_queue(screen, font, queue, result):
    queue_label = font.render("Queue: " + " ".join(map(str, queue)), True, (0, 0, 0))
    result_label = font.render("Result: " + " ".join(map(str, result)), True, (0, 0, 0))
    screen.blit(queue_label, (10, 10))
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
    bfs_result = []
    final_queue = []
    bfs_complete = False

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
                                bfs_result, final_queue = bfs_visualize(screen, font, g.adj, g.V, start, nodes)
                                bfs_complete = True
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
            color = (0, 0, 255) if i in bfs_result else (0, 0, 0)
            pygame.draw.ellipse(screen, color, node)
            label = font.render(str(i), True, (255, 255, 255))
            screen.blit(label, (node.x + 5, node.y + 5))

        if input_active:
            input_label = font.render("Enter starting node: " + input_text, True, (0, 0, 0))
            screen.blit(input_label, (10, 70))

        if bfs_complete:
            draw_queue(screen, font, final_queue, bfs_result)

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

def bfs(adj, V, s):
    visited = [False] * V
    queue = deque([s])
    visited[s] = True

    while queue:
        v = queue.popleft()
        print(v, end=" ")

        for i in adj[v]:
            if not visited[i]:
                visited[i] = True
                queue.append(i)
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
                start = int(input("Enter the starting node for BFS: "))
                if 0 <= start < g.V:
                    print(f"BFS traversal starting from node {start}: ", end="")
                    bfs(g.adj, g.V, start)
                else:
                    print("Invalid starting node. Node index out of bounds.")

        screen.fill((255, 255, 255))

        for edge in edges:
            pygame.draw.line(screen, (0, 0, 0), nodes[edge[0]].center, nodes[edge[1]].center, 2)

        for i, node in enumerate(nodes):
            pygame.draw.ellipse(screen, (0, 0, 0), node)
            label = font.render(str(i), True, (255, 255, 255))
            screen.blit(label, (node.x + node_radius // 2, node.y + node_radius // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
"""