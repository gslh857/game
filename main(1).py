import pygame
import random as rn
from pygame import mixer

colours = [[0, 255, 255], [190, 83, 120], [0, 255, 0], [190, 190, 190],
           [238, 130, 238], [255, 165, 0], [184, 94, 0], [250, 235, 0],
           [189, 190, 57], [160, 32, 240]]
mixer.init()
mixer.music.load("music.mp3")
mixer.music.play()


class Shape:
    x = 0
    y = 0
    shapes = [[[2, 6, 10, 14], [8, 9, 10, 11]],
              [[5, 6, 10, 11], [2, 6, 5, 9]],
              [[2, 3, 5, 6], [1, 5, 6, 10]],
              [[2, 3, 6, 10], [1, 5, 6, 7], [3, 7, 11, 10], [5, 6, 7, 11]],
              [[5, 6, 10, 14], [1, 2, 3, 5], [1, 5, 9, 10], [9, 10, 11, 7]],
              [[2, 5, 6, 7], [2, 5, 6, 10], [5, 6, 7, 10], [2, 6, 7, 10]],
              [[0, 1, 5, 4]]
              ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figure = rn.randint(0, len(self.shapes) - 1)
        self.color = rn.randint(0, len(colours) - 1)
        self.rot = 0

    def image(self):
        return self.shapes[self.figure][self.rot]

    def rotate(self):
        self.rot = (self.rot + 1) if self.rot < len(
            self.shapes[self.figure]) - 1 else 0


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    h = 0
    w = 0
    x = 50
    y = 50
    zoom = 30
    shape = None

    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(h):
            new_line = []
            for j in range(w):
                new_line.append(0)
            self.field.append(new_line)

    def new_shape(self):
        self.shape = Shape(5, 0)

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.shape.image():
                    if (
                            i + self.shape.y > self.h - 1
                            or j + self.shape.x > self.w - 1
                            or j + self.shape.x < 0
                            or self.field[i + self.shape.y][
                            j + self.shape.x] > 0
                    ):
                        return True
        return False

    def break_lines(self):
        full_rows = []
        for i in range(1, self.h):
            if all(self.field[i]):
                full_rows.append(i)

        for row in full_rows:
            self.field.pop(row)
            self.field.insert(0, [0] * self.w)

        self.score += len(full_rows) ** 2

    def go_space(self):
        distance = 0
        while not self.intersects():
            distance += 1
            self.shape.y += 1
        self.shape.y -= distance - 1
        self.freeze()

    def go_down(self):
        self.shape.y += 1
        if self.intersects():
            self.shape.y -= 1
            self.freeze()

    def freeze(self):
        shape_image = self.shape.image()
        shape_y, shape_x = self.shape.y, self.shape.x
        for i in range(4):
            for j in range(4):
                if i * 4 + j in shape_image:
                    y, x = shape_y + i, shape_x + j
                    self.field[y][x] = self.shape.color
        self.break_lines()
        self.new_shape()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.shape.x
        self.shape.x += dx
        if self.intersects():
            self.shape.x = old_x

    def rotate(self):
        old_rot = self.shape.rot
        self.shape.rotate()
        if self.intersects():
            self.shape.rot = old_rot


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

size = (700, 750)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris Game")
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False
screen.fill(BLACK)
pygame.display.set_caption("Tetris Game")

while not done:
    if game.shape is None:
        game.new_shape()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_ESCAPE:
                done = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)
    pygame.display.set_caption("Tetris Game")

    for i in range(game.h):
        for j in range(game.w):
            pygame.draw.rect(screen, GRAY,
                             [game.x + game.zoom * j, game.y + game.zoom * i,
                              game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colours[game.field[i][j]],
                                 [game.x + game.zoom * j + 1,
                                  game.y + game.zoom * i + 1, game.zoom - 2,
                                  game.zoom - 1])
    font1 = pygame.font.SysFont('Calibre', 25, True, False)
    font2 = pygame.font.SysFont('Calibre', 65, True, False)
    if game.shape is not None:
        shape_image = game.shape.image()
        shape_x, shape_y = game.shape.x, game.shape.y
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in shape_image:
                    x, y = game.x + game.zoom * (
                            shape_x + j) + 1, game.y + game.zoom * (
                                   shape_y + i) + 1
                    pygame.draw.rect(screen, colours[game.shape.color],
                                     [x, y, game.zoom - 2, game.zoom - 2])
    text = font2.render("Score: " + str(game.score), True, GREEN)
    text_game_over = font2.render("!!GAME OVER!!", True, (255, 0, 0))
    text_game_over1 = font1.render("Press esc", True, (255, 215, 0))
    screen.blit(text, (0, 0))
    if game.state == "game over":
        screen.blit(text_game_over, (20, 200))
        screen.blit(text_game_over1, (25, 265))
        pygame.mixer.music.pause()
    pygame.display.flip()
    clock.tick(fps)
    pygame.mixer.music.unpause()
pygame.quit()
