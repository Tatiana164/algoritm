import pygame
import random
from queue import PriorityQueue

pygame.init()

# настройки
WIDTH = 600
GRID_SIZE = 10   # теперь карта 10×10
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding (hardcoded map)")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.type = 'empty'
        self.color = WHITE
        self.neighbors = []
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None

    def draw(self, win):
        pygame.draw.rect(win, self.color,
                         (self.col * CELL_SIZE,
                          self.row * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))

    def reset(self):
        if self.type not in ['start', 'end']:
            self.type = 'empty'; self.color = WHITE
        self.g = float('inf'); self.h = 0; self.f = float('inf')
        self.parent = None; self.neighbors = []

    def make_start(self):
        self.type = 'start'; self.color = ORANGE; self.g = 0

    def make_end(self):
        self.type = 'end'; self.color = TURQUOISE

    def make_barrier(self):
        if self.type not in ['start', 'end']:
            self.type = 'obstacle'; self.color = BLACK

    def make_open(self):
        if self.type not in ['start', 'end', 'obstacle']:
            self.type = 'open'; self.color = GREEN

    def make_closed(self):
        if self.type not in ['start', 'end', 'obstacle']:
            self.type = 'closed'; self.color = RED

    def make_path(self):
        if self.type not in ['start', 'end', 'obstacle']:
            self.type = 'path'; self.color = PURPLE

    def is_barrier(self):
        return self.type == 'obstacle'

    def update_neighbors(self, grid):
        self.neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = self.row+dx, self.col+dy
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                nei = grid[nr][nc]
                if not nei.is_barrier():
                    self.neighbors.append(nei)


def make_grid():
    return [[Cell(r, c) for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]


def draw_grid(win, grid):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE))
        pygame.draw.line(win, GREY, (i*CELL_SIZE, 0), (i*CELL_SIZE, WIDTH))
    pygame.display.update()

# S — старт
# E — финиш
# # — препятствие
# . — пустая клетка

# карта 10×10
MAP = [
    ".#...##.#.",
    "###.#...#.",
    "S.....###.",
    "...##.....",
    "..........",
    "#...#.....",
    "#.........",
    "....#...#.",
    "..####.##.",
    "#.#......E"
]

def load_map(grid):
    start = end = None
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            ch = MAP[r][c]
            cell = grid[r][c]
            if ch == '#':
                cell.make_barrier()
            elif ch == 'S':
                cell.make_start(); start = cell
            elif ch == 'E':
                cell.make_end(); end = cell
            # '.' — оставляем пустым
    
    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)
    return start, end


def h(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


def a_star_algorithm(grid, start, end):
    open_list = PriorityQueue()
    count = 0
    start.g = 0
    start.h = h(start, end)
    start.f = start.h
    open_list.put((start.f, count, start))
    open_set = {start}
    came_from = {}

    while not open_list.empty():
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return False

        _, _, current = open_list.get()
        open_set.remove(current)
        current.make_closed()

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw_grid(WIN, grid)
                pygame.time.delay(50)
            return True

        for nei in current.neighbors:
            if nei.is_barrier() or nei.type == 'closed':
                continue
            tentative_g = current.g + 1  # все рёбра веса 1
            if tentative_g < nei.g:
                came_from[nei] = current
                nei.g = tentative_g
                nei.h = h(nei, end)
                nei.f = nei.g + nei.h
                if nei not in open_set:
                    count += 1
                    open_list.put((nei.f, count, nei))
                    open_set.add(nei)
                    nei.make_open()

        draw_grid(WIN, grid)
        pygame.time.delay(20)

    return False


def main():
    grid = make_grid()
    start, end = load_map(grid)

    run = True
    solved = False
    while run:
        draw_grid(WIN, grid)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE and not solved:
                    solved = a_star_algorithm(grid, start, end)
    pygame.quit()


if __name__ == "__main__":
    main()
