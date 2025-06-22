# Сделано в автогенераций карты
import pygame
import random
from queue import PriorityQueue

pygame.init()

# настройки
WIDTH = 600
GRID_SIZE = 20  # 10x10 сетка
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding with Dynamic Obstacles")

# Цвета
RED = (255, 0, 0)  # Посещённые ячейки
GREEN = (0, 255, 0)  # Ячейки в очереди
WHITE = (255, 255, 255)  # Пустая ячейка
BLACK = (0, 0, 0)  # Препятствие
PURPLE = (128, 0, 128)  # Путь
ORANGE = (255, 165, 0)  # Начало
GREY = (128, 128, 128)  # Линии сетки
TURQUOISE = (64, 224, 208)  # Конец


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.type = 'empty'  # empty, obstacle, start, end, open, closed, path
        self.color = WHITE
        self.neighbors = []
        self.g = float('inf')  # Расстояние от старта
        self.h = 0
        self.f = float('inf')  # f = g + h
        self.parent = None

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.col * CELL_SIZE, self.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def reset(self):
        if self.type not in ['start', 'end']:
            self.type = 'empty'
            self.color = WHITE
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.neighbors = []

    def make_start(self):
        self.type = 'start'
        self.color = ORANGE
        self.g = 0

    def make_end(self):
        self.type = 'end'
        self.color = TURQUOISE

    def make_barrier(self):
        if self.type not in ['start', 'end']:
            self.type = 'obstacle'
            self.color = BLACK

    def make_open(self):
        if self.type not in ['start', 'end', 'obstacle']:
            self.type = 'open'
            self.color = GREEN

    def make_closed(self):
        if self.type not in ['start', 'end', 'obstacle']:
            self.type = 'closed'
            self.color = RED

    def make_path(self):
        if self.type not in ['start', 'end', 'obstacle']:
            self.type = 'path'
            self.color = PURPLE

    def is_barrier(self):
        return self.type == 'obstacle'

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
        for dx, dy in directions:
            new_row, new_col = self.row + dx, self.col + dy
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                neighbor = grid[new_row][new_col]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)


def make_grid():
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid


def draw_grid(win, grid):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))
    pygame.display.update()


def generate_dynamic_grid(grid):
    for row in grid:
        for cell in row:
            cell.reset()

    start_row, start_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]
    start.make_start()
    end.make_end()

    # Генерация препятствий (не более 25% от 100 клеток = 25)
    max_obstacles = int(GRID_SIZE * GRID_SIZE * 0.25)  # 25 клеток
    obstacle_count = random.randint(0, max_obstacles)
    obstacle_positions = set()

    while len(obstacle_positions) < obstacle_count:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (row, col) not in [(start_row, start_col), (end_row, end_col)] and (row, col) not in obstacle_positions:
            obstacle_positions.add((row, col))

    for row, col in obstacle_positions:
        grid[row][col].make_barrier()

    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)

    return start, end


def h(cell1, cell2):
    return abs(cell1.row - cell2.row) + abs(cell1.col - cell2.col)


# Алгоритм A*
def a_star_algorithm(grid, start, end):
    open_list = PriorityQueue()
    count = 0
    open_list.put((0, count, start))
    open_set_hash = {start}
    came_from = {}
    start.g = 0
    start.h = h(start, end)
    start.f = start.g + start.h

    while not open_list.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        f_score, _, current = open_list.get()
        open_set_hash.remove(current)
        current.make_closed()
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw_grid(WIN, grid)
                pygame.time.delay(50)
            return True

        for neighbor in current.neighbors:
            if neighbor.is_barrier() or neighbor.type == 'closed':
                continue

            tentative_g = current.g + 1
            if tentative_g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = tentative_g
                neighbor.h = h(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set_hash:
                    count += 1
                    open_list.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw_grid(WIN, grid)
        pygame.time.delay(50)

    return False


def main():
    grid = make_grid()
    start, end = generate_dynamic_grid(grid)
    run = True

    while run:
        draw_grid(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    a_star_algorithm(grid, start, end)
                if event.key == pygame.K_r:
                    start, end = generate_dynamic_grid(grid)

    pygame.quit()


if __name__ == "__main__":
    main()
