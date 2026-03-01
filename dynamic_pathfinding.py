import pygame
import sys
import math
import random
import heapq
import time

# ===============================
# CONFIGURATION
# ===============================
WIDTH = 1000
HEIGHT = 700
GRID_SIZE = 25
ROWS = 20
COLS = 20

SIDEBAR_WIDTH = 300
GRID_WIDTH = WIDTH - SIDEBAR_WIDTH

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 200, 0)
PURPLE = (150, 0, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent - Modern UI")
font = pygame.font.SysFont("Arial", 18)

# ===============================
# NODE CLASS
# ===============================
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None
        self.obstacle = False

    def __lt__(self, other):
        return self.f < other.f

# ===============================
# GRID SETUP
# ===============================
def create_grid():
    return [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

grid = create_grid()
start = grid[0][0]
goal = grid[ROWS - 1][COLS - 1]

algorithm = "A*"
heuristic_type = "Manhattan"
dynamic_mode = False

visited_count = 0
path_cost = 0
exec_time = 0

# ===============================
# HEURISTICS
# ===============================
def heuristic(a, b):
    if heuristic_type == "Manhattan":
        return abs(a.row - b.row) + abs(a.col - b.col)
    else:
        return math.sqrt((a.row - b.row) ** 2 + (a.col - b.col) ** 2)

# ===============================
# DRAW FUNCTIONS
# ===============================
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            node = grid[r][c]
            x = c * GRID_SIZE
            y = r * GRID_SIZE
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

            if node.obstacle:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

def draw_sidebar():
    pygame.draw.rect(screen, BLACK, (GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))

    y = 30
    items = [
        f"Algorithm: {algorithm}",
        f"Heuristic: {heuristic_type}",
        f"Dynamic Mode: {'ON' if dynamic_mode else 'OFF'}",
        "",
        f"Visited Nodes: {visited_count}",
        f"Path Cost: {path_cost}",
        f"Execution Time: {exec_time:.4f}s",
        "",
        "Controls:",
        "A - Toggle A* / Greedy",
        "H - Toggle Heuristic",
        "D - Toggle Dynamic Mode",
        "R - Random Map",
        "C - Clear Grid",
        "SPACE - Start Search"
    ]

    for item in items:
        text = font.render(item, True, WHITE)
        screen.blit(text, (GRID_WIDTH + 20, y))
        y += 30

# ===============================
# SEARCH ALGORITHMS
# ===============================
def reconstruct_path(current):
    global path_cost
    path_cost = 0
    while current.parent:
        pygame.draw.rect(screen, GREEN,
                         (current.col * GRID_SIZE,
                          current.row * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE))
        current = current.parent
        path_cost += 1
        pygame.display.update()

def get_neighbors(node):
    neighbors = []
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for dr, dc in directions:
        r = node.row + dr
        c = node.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if not grid[r][c].obstacle:
                neighbors.append(grid[r][c])
    return neighbors

def search():
    global visited_count, exec_time
    visited_count = 0
    start_time = time.time()

    for row in grid:
        for node in row:
            node.g = float("inf")
            node.f = float("inf")
            node.parent = None

    open_list = []
    start.g = 0
    start.h = heuristic(start, goal)
    start.f = start.h if algorithm == "Greedy" else start.h
    heapq.heappush(open_list, start)

    closed_set = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current == goal:
            exec_time = time.time() - start_time
            reconstruct_path(current)
            return

        closed_set.add(current)
        visited_count += 1

        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g = current.g + 1

            if algorithm == "A*":
                if tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.h = heuristic(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current
                    heapq.heappush(open_list, neighbor)
            else:  # Greedy
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.h
                neighbor.parent = current
                heapq.heappush(open_list, neighbor)

        pygame.draw.rect(screen, BLUE,
                         (current.col * GRID_SIZE,
                          current.row * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE))
        pygame.display.update()

        if dynamic_mode and random.random() < 0.02:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if grid[r][c] != start and grid[r][c] != goal:
                grid[r][c].obstacle = True

    exec_time = time.time() - start_time

# ===============================
# MAP FUNCTIONS
# ===============================
def random_map():
    for r in range(ROWS):
        for c in range(COLS):
            if random.random() < 0.2:
                grid[r][c].obstacle = True
            else:
                grid[r][c].obstacle = False

def clear_map():
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c].obstacle = False

# ===============================
# MAIN LOOP
# ===============================
running = True
while running:
    screen.fill((40, 40, 40))
    draw_grid()
    draw_sidebar()

    pygame.draw.rect(screen, RED,
                     (start.col * GRID_SIZE,
                      start.row * GRID_SIZE,
                      GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, PURPLE,
                     (goal.col * GRID_SIZE,
                      goal.row * GRID_SIZE,
                      GRID_SIZE, GRID_SIZE))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                algorithm = "Greedy" if algorithm == "A*" else "A*"
            if event.key == pygame.K_h:
                heuristic_type = "Euclidean" if heuristic_type == "Manhattan" else "Manhattan"
            if event.key == pygame.K_d:
                dynamic_mode = not dynamic_mode
            if event.key == pygame.K_r:
                random_map()
            if event.key == pygame.K_c:
                clear_map()
            if event.key == pygame.K_SPACE:
                search()

pygame.quit()
sys.exit()