import asyncio
import random
import pygame
import sys
from pygame import Color, Vector2

pygame.init()

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

GRIDSIZE = 50
space = 100
units = 12
board = Vector2(int(units), int(units))

screen = pygame.display.set_mode((space * 2 + board.x * GRIDSIZE, space * 2 + board.y * GRIDSIZE))
pygame.display.set_caption('sNakE gOnE WroOng')

FrameGarden = pygame.image.load("images/frame.png")
RedApple = pygame.image.load("images/redApple.png")
GreenApple = pygame.image.load("images/greenApple.png")
YellowApple = pygame.image.load("images/yellowApple.png")
HeadForward = pygame.image.load("images/headForward.png")
InfoThing = pygame.image.load("images/info.png")
frameGarden = pygame.transform.scale(FrameGarden, ((space * 3) + board.x * GRIDSIZE, (space * 3) + board.y * GRIDSIZE))
redApple = pygame.transform.scale(RedApple, (GRIDSIZE, GRIDSIZE))
infoThing = pygame.transform.scale(InfoThing, (100, 100))
greenApple = pygame.transform.scale(GreenApple, (GRIDSIZE, GRIDSIZE))
yellowApple = pygame.transform.scale(YellowApple, (GRIDSIZE, GRIDSIZE))
headForward = pygame.transform.scale(HeadForward, (GRIDSIZE, GRIDSIZE))
speed = pygame.mixer.Sound("whoosh.mp3")
pygame.mixer.music.load('whoosh.mp3')

def draw_board():
    for x in range(int(board.x)):
        for y in range(int(board.y)):
            color = (0, 0, 0) if (x + y) % 2 == 0 else (0, 0, 225)
            draw_box(color, (space + (x * GRIDSIZE), space + (y * GRIDSIZE)))

def draw_box(color, pos):
    rect = pygame.Rect(pos[0], pos[1], GRIDSIZE, GRIDSIZE)
    pygame.draw.rect(screen, color, rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(0, 0), Vector2(1, 0)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self):
        for index, block in enumerate(self.body):
            x_pos = space + (GRIDSIZE * block.x)
            y_pos = space + (GRIDSIZE * block.y)
            block_rect = pygame.Rect(x_pos, y_pos, GRIDSIZE, GRIDSIZE)
            
            if index == 0:
                screen.blit(headForward, (x_pos, y_pos))
            else:
                pygame.draw.rect(screen, (150, 100, 100), block_rect)
            
    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

        head = self.body[0]
        head.x = int(head.x)
        head.y = int(head.y)

        if head.x < -1 or head.x >= board.x + 1 or head.y < -1 or head.y >= board.y + 1:
            self.game.game_over()

    def reset(self):
        self.body = [Vector2(0, 0), Vector2(1, 0)]
        self.direction = Vector2(1, 0)
        self.new_block = False

class Apple:
    def __init__(self):
        self.randomize()

    def draw(self):
        x_pos = space + (GRIDSIZE * self.pos.x)
        y_pos = space + (GRIDSIZE * self.pos.y)
        if self.type == 'normal':
            screen.blit(redApple, (x_pos, y_pos))
        elif self.type == 'inverted':
            screen.blit(greenApple, (x_pos, y_pos))
        elif self.type == 'speed':
            screen.blit(yellowApple, (x_pos, y_pos))

    def randomize(self):
        self.pos = Vector2(random.randint(0, int(board.x) - 1), random.randint(0, int(board.y) - 1))
        self.type = random.choice(['normal', 'inverted', 'speed'])

class Game:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()
        self.currentGame = True
        self.inverted = False
        self.ticks = 6
        self.bricks = []

    def draw(self):
        draw_board()
        self.snake.draw()
        self.apple.draw()
        for brick in self.bricks:
            draw_box((150, 105, 25), Vector2(brick.x * GRIDSIZE + space, brick.y * GRIDSIZE + space))

    def check_collision(self):
        snake = self.snake
        apple = self.apple
        if snake.body[0] == apple.pos:
            if self.inverted or self.ticks != 6:
                self.inverted = False
                self.ticks = 6
            if apple.type == "normal":
                x_pos = random.randint(0, int(board.x) - 1)
                y_pos = random.randint(0, int(board.x) - 1)
                self.bricks.append(Vector2(x_pos, y_pos))
            if apple.type == "inverted":
                self.inverted = True
                self.ticks = 4
            if apple.type == "speed":
                pygame.mixer.music.play(1)
                self.ticks = 10
            apple.randomize()
            snake.new_block = True

    def check_game_over(self):
        head = self.snake.body[0]

        if head in self.snake.body[1:]:
            self.game_over()

        for brick in self.bricks:
            if brick == head:
                self.game_over()

    def end_round(self):
        self.currentGame = False
        self.snake.reset()

    def game_over(self):
        pygame.quit()
        sys.exit()

def game_loop():
    game = Game()
    snake = game.snake
    running = True
    while running:
        screen.fill((255, 255, 255))
        game.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game.game_over()
            if event.type == pygame.KEYDOWN:
                if game.inverted:
                    if event.key == pygame.K_UP:
                        snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_DOWN:
                        snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_RIGHT:
                        snake.direction = Vector2(-1, 0)
                else:
                    if event.key == pygame.K_UP:
                        snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_LEFT:
                        snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_DOWN:
                        snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_RIGHT:
                        snake.direction = Vector2(1, 0)
        
        screen.blit(frameGarden, (space - (GRIDSIZE * 2.75), space - (GRIDSIZE * 2.75)))
        screen.blit(infoThing, (0, 0))

        if game.currentGame:
            snake.move()
            game.check_collision()
            game.check_game_over()
        
        pygame.display.flip()
        clock.tick(game.ticks)

game_loop()
