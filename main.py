FPS = 60
BIRD_SIZE = 25
WIN_DIMENSIONS = (1000,700)
START_POINT = (100,500/2)
FREQ = 5
import pygame
from pygame.locals import *
import game
import neuralnetwork
import numpy as np


WHITE = (255, 255, 255)
GREEN = (118, 194, 44)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
BACKGROUND = (123, 197, 205)
# BIRD_COLOR = (249, 241, 36)

pygame.init()
mainClock = pygame.time.Clock()

screen = pygame.display.set_mode((WIN_DIMENSIONS[0],WIN_DIMENSIONS[1]),0,32)
canvas = pygame.Surface((WIN_DIMENSIONS[0],WIN_DIMENSIONS[1]))
# screen = pygame.display.set_mode((WIN_DIMENSIONS[0]+500,WIN_DIMENSIONS[1]),0,32)
# canvas = pygame.Surface((WIN_DIMENSIONS[0]+500,WIN_DIMENSIONS[1]))

font = pygame.font.Font(None, 24)
gameCamera = pygame.Rect((0,0,WIN_DIMENSIONS[0],WIN_DIMENSIONS[1]))
# dataCamera = pygame.Rect((WIN_DIMENSIONS[0],0,500,WIN_DIMENSIONS[1]))
gameSurface = canvas.subsurface(gameCamera)
# dataSurface = canvas.subsurface(dataCamera)

pygame.display.set_caption("Flappy Bird Neural Network")

gameActive = True


bird = game.Bird(START_POINT,BIRD_SIZE,WIN_DIMENSIONS)


sprites = pygame.sprite.Group()
sprites.add(bird)

pipeIndex = 0
topPipeY = bird.pipes[pipeIndex][0].bottom
bottomPipeY = bird.pipes[pipeIndex][1].top



n = neuralnetwork.NeuralNetwork(3)
n.addLayer(1)

cycle = 1
highScore = 0
ticks = 0
while gameActive:
    # jump = 0
    ticks += 1
    if(bird.alive == False):
        cycle += 1
        if(bird.rect.bottom >= WIN_DIMENSIONS[1]):
            t = 1
        else:
            if(bird.rect.center[1] >= bottomPipeY+10):
                t = 1
            elif(bird.rect.center[1] <= topPipeY+10):
                t = 0
            else: 
                t = 0

        n.adjust(t)

        bird = game.Bird(START_POINT,BIRD_SIZE,WIN_DIMENSIONS)
        sprites = pygame.sprite.Group()
        sprites.add(bird)
        bird.alive = True

        topPipeY = bird.pipes[pipeIndex][0].bottom
        bottomPipeY = bird.pipes[pipeIndex][1].top
        distanceToGround = WIN_DIMENSIONS[1] - bird.rect.bottom

    gameSurface.fill(BACKGROUND)
    # dataSurface.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            gameActive = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                gameActive = False
    
    if(bird.alive):
        jump = n.predict(np.array([topPipeY/100,bottomPipeY/100,bird.rect.center[1]/100]))[0]
        if(ticks % FREQ == 0):
            bird.jumped(jump)
        sprites.update()

    if(gameActive == False):
        break
    
    for p in bird.pipes:
        pygame.draw.rect(gameSurface,GREEN,p[0])
        pygame.draw.rect(gameSurface,GREEN,p[1])

        if(bird.rect.colliderect(p[0]) or bird.rect.colliderect(p[1])):
            bird.alive = False

    pygame.draw.line(gameSurface,RED,bird.rect.center,(bird.pipes[pipeIndex][0].center[0],bird.pipes[pipeIndex][0].bottom))
    pygame.draw.line(gameSurface,RED,bird.rect.center,(bird.pipes[pipeIndex][1].center[0],bird.pipes[pipeIndex][1].top))
    
    sprites.draw(gameSurface)


    topPipeY = bird.pipes[pipeIndex][0].bottom
    bottomPipeY = bird.pipes[pipeIndex][1].top
    distanceToGround = WIN_DIMENSIONS[1] - bird.rect.bottom 
    

    if(bird.rect.bottom >= WIN_DIMENSIONS[1]):
        bird.alive = False
        
    if(bird.score > highScore):
        highScore = bird.score

    FPS_monitor = font.render(str(round(mainClock.get_fps(),2))+"FPS",False, BLACK)
    cycleText = font.render("Cycle: "+str(cycle),False, BLACK)
    scoreText = font.render("Score: "+str(bird.score),False, BLACK)
    highScoreText = font.render("High Score: "+str(highScore),False, BLACK)

    topPipeText = font.render("Top: "+str(topPipeY),False, BLACK)
    bottomPipeText = font.render("Bottom: "+str(bottomPipeY),False, BLACK)
    birdText = font.render("Bird: "+str(bird.rect.center[1]),False, BLACK)
    jumpText = font.render("Jump: "+str(round(jump,3)),False, BLACK)

    screen.blit(gameSurface,(0,0))
    # screen.blit(dataSurface,(WIN_DIMENSIONS[0],0))
    screen.blit(FPS_monitor,(10,10))
    screen.blit(topPipeText,(10,30))
    screen.blit(bottomPipeText,(10,50))
    screen.blit(birdText,(10,70))
    screen.blit(jumpText,(10,90))
    screen.blit(cycleText,(WIN_DIMENSIONS[0]-100,10))
    screen.blit(highScoreText,(WIN_DIMENSIONS[0]-125,30))
    screen.blit(scoreText,(WIN_DIMENSIONS[0]-100,50))
    # screen.blit(bird.image, bird.rect)

    if(bird.alive == False):
        game_over = font.render("GAME OVER",False, BLACK)
        screen.blit(game_over,(int(WIN_DIMENSIONS[0]/2)-50,int(WIN_DIMENSIONS[1]/2)))

    pygame.display.update()
    mainClock.tick(FPS)
