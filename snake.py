import random
import pygame
import tkinter as tk
from tkinter import messagebox

width = 500
rows = 20

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("Snake")

class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, x_dir=1, y_dir=0, color=(0,255,0)):
        self.pos = start
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.color = color
        
    def move(self, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.pos = (self.pos[0] + self.x_dir, self.pos[1] + self.y_dir)
    
    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*distance+1, j*distance+1, distance-2, distance-2))
        if eyes:
            center = distance // 2
            radius = 3
            circleMiddle = (i*distance+center-radius, j*distance+8)
            circleMiddle2 = (i*distance+distance-radius*2, j*distance+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
    
class Snake(object):
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.x_dir = 0
        self.y_dir = 1
        
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed()
            
            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.x_dir = -1
                    self.y_dir = 0
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                    
                elif keys[pygame.K_RIGHT]:
                    self.x_dir = 1
                    self.y_dir = 0
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                    
                elif keys[pygame.K_UP]:
                    self.x_dir = 0
                    self.y_dir = -1
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                    
                elif keys[pygame.K_DOWN]:
                    self.x_dir = 0
                    self.y_dir = 1
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                    
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.x_dir == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.x_dir == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.y_dir == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.y_dir == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.x_dir, c.y_dir)
    
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x_dir = 0
        self.y_dir = 1
    
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.x_dir, tail.y_dir
        
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))
            
        self.body[-1].x_dir = dx
        self.body[-1].y_dir = dy
    
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
    
def drawGrid(width, rows, surface):
    sizeBetween = width // rows
    x = 0
    y = 0
    for _ in range(rows):
        x += sizeBetween
        y += sizeBetween
        pygame.draw.line(surface, (WHITE), (x,0), (x, width))
        pygame.draw.line(surface, (WHITE), (0,y), (width, y))

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def mainMenu():
    run = True
    while run:
        title = pygame.image.load("snake.png")
        win.blit(title, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

def maxScore():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
        
    return score 

def updateScore(newscore):
    score = maxScore()
        
    with open('scores.txt', 'w') as f:
        if int(score) > newscore:
            f.write(str(score))
        else:
            f.write(str(newscore))
            message_box("High Score", "NEW HIGH SCORE!!!")

def lossScreen(score):
    lossFont = pygame.font.SysFont('comicsans', 60)
    smallFont = pygame.font.SysFont('comicsans', 40)
    lostTxt = 'You Lost...'
    againTxt = "Press any key to play again!"
    sadSnake = pygame.image.load("sadSnake.png")
    pygame.time.delay(1000)
    win.fill(RED)
    
    label = lossFont.render(lostTxt, 1, BLACK)
    againLabel = smallFont.render(againTxt, 1, GREEN)
    scoreLabel = smallFont.render("Last Score: " + str(score), 1, WHITE)
    highScore = smallFont.render("High Score: " + maxScore(), 1, WHITE)
    
    win.blit(label, ((width/2 - label.get_width()/2), (100 - label.get_height()/2)))
    win.blit(sadSnake, (width/2 - sadSnake.get_width()/2, 150))
    win.blit(scoreLabel, (125 - scoreLabel.get_width()/2, 350))
    win.blit(highScore, (375 - highScore.get_width()/2, 350))
    win.blit(againLabel, (width/2 - againLabel.get_width()/2, 400))
    
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
                main()

def main():
    global s, snack, score
    s = Snake((0, 255, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(255, 0, 0))
    score = 0
    run = True
    clock = pygame.time.Clock()
    
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(255, 0, 0))
            score += 1
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                updateScore(score)
                lossScreen(score)
                #print('Score: ', len(s.body))
                #message_box('You lost!', 'Play again...')
                s.reset((10,10))
                break
            
        redrawWindow(win)

mainMenu()