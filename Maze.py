import tkinter
import random
import pygame
import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_GREEN = (33, 158, 188)
HONEY_YELLOW = (255, 183, 3)
GREY = (108, 117, 125)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == HONEY_YELLOW

    def is_end(self):
        return self.color == BLUE_GREEN

    def reset_node(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = BLUE_GREEN

    def make_start(self):
        self.color = HONEY_YELLOW

    def draw(self, scr):
        pygame.draw.rect(
            scr, self.color, (self.x, self.y, self.width, self.width))


class Maze:

    def __init__(self, width, rows):
        pygame.init()
        self.WIDTH = width
        self.ROWS = rows
        self.BOX_WIDTH = self.WIDTH // self.ROWS
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        pygame.display.set_caption("Maze Solver")
        self.GRID = self.make_grid()
        self.reset_board()
        clock = pygame.time.Clock()
        is_running = True
        self.FPS = 20
        while is_running:
            clock.tick(self.FPS)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if pygame.mouse.get_pressed()[0]:
                    row, col = self.get_mouse_pos()
                    self.GRID[row][col].make_wall()

                if pygame.mouse.get_pressed()[2]:
                    row, col = self.get_mouse_pos()
                    self.GRID[row][col].reset_node()

                if keys[pygame.K_r]:
                    self.reset_board()

            if keys[pygame.K_UP]:
                self.move_up()

            if keys[pygame.K_DOWN]:
                self.move_down()

            if keys[pygame.K_LEFT]:
                self.move_left()

            if keys[pygame.K_RIGHT]:
                self.move_right()

            self.draw()
        pygame.quit()

    def reset_board(self):
        for row in self.GRID:
            for node in row:
                node.reset_node()
        self.make_boundary()
        self._player = [0, random.randint(1, self.ROWS-1)]
        self.getPlayerNode().make_start()

    def make_grid(self):
        return [[Node(i, j, self.BOX_WIDTH, self.ROWS)
                 for j in range(self.ROWS)]
                for i in range(self.ROWS)]

    def make_boundary(self):
        for i in range(self.ROWS):
            self.GRID[0][i].make_wall()
            self.GRID[-1][i].make_wall()
            self.GRID[i][0].make_wall()
            self.GRID[i][-1].make_wall()
            # self.draw()  # FOR REALTIME DRAWING WALLS

    def draw_grid_lines(self):
        for i in range(self.ROWS):  # FOR X AXIS
            pygame.draw.line(
                self.SCREEN,  # DISPLAY SCREEN
                GREY,  # COLOR
                            (0, i*self.BOX_WIDTH),  # X - STARTING POINT
                            (self.WIDTH, i*self.BOX_WIDTH))  # X - ENDING POINT
            for j in range(self.ROWS):  # FOR Y AXIS
                pygame.draw.line(
                    self.SCREEN,  # DISPLAY SCREEN
                    GREY,  # COLOR
                                (j*self.BOX_WIDTH, 0),  # Y - STARTING POINT
                                (j*self.BOX_WIDTH, self.WIDTH))  # Y - ENDING POINT

    def draw(self):
        self.SCREEN.fill(WHITE)
        for row in self.GRID:
            for node in row:
                node.draw(self.SCREEN)
        self.draw_grid_lines()
        pygame.display.update()

    def get_mouse_pos(self):
        y, x = pygame.mouse.get_pos()
        row = y // self.BOX_WIDTH
        col = x // self.BOX_WIDTH
        return row, col

    def getPlayerNode(self):
        return self.GRID[self._player[0]][self._player[1]]

    def is_valid_move(self, node):
        if node.is_wall() or node.is_start():
            return False
        return True

    def move_node(self, node):
        node.make_closed() if node.is_open() else node.make_open()

    def move_up(self):
        if self._player[1] <= 0:
            return
        if not self.is_valid_move(self.GRID[self._player[0]][self._player[1] - 1]):
            return
        self._player[1] -= 1
        self.move_node(self.getPlayerNode())

    def move_down(self):
        if self._player[1] >= self.ROWS - 1:
            return
        if not self.is_valid_move(self.GRID[self._player[0]][self._player[1] + 1]):
            return
        self._player[1] += 1
        self.move_node(self.getPlayerNode())

    def move_left(self):
        if self._player[0] <= 0:
            return
        if not self.is_valid_move(self.GRID[self._player[0] - 1][self._player[1]]):
            return
        self._player[0] -= 1
        self.move_node(self.getPlayerNode())

    def move_right(self):
        if self._player[0] >= self.ROWS - 1:
            return
        if not self.is_valid_move(self.GRID[self._player[0] + 1][self._player[1]]):
            return
        self._player[0] += 1
        self.move_node(self.getPlayerNode())

    def build_maze(self, visited):
        pass


if __name__ == "__main__":
    Maze = Maze(800, 50)
