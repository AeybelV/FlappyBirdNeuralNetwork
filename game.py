import pygame
import numpy as np
import random
FLAPPING = -50
GRAVITY = 9

class Bird(pygame.sprite.Sprite):
    def __init__(self,startPos,size,windowDimensions):
        pygame.sprite.Sprite.__init__(self)
        self.windowDimensions = windowDimensions
        self.image = pygame.image.load('bird.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.jump = 0
        self.rect.x = windowDimensions[0]/8
        self.alive = True
        self.pipes = [self.createPipe()]
        self.score = 0

        # self.guiObject = pygame.Rect(startPos,(size,size))
    def createPipe(self):
        gap = 200
        topPipeY = 0
        topPipeHeight = random.randint(10,self.windowDimensions[1]-gap)

        bottomPipeY = topPipeHeight+gap

        topPipe = pygame.Rect((self.windowDimensions[0]+100,topPipeY),(100,topPipeHeight))
        bottomPipe = pygame.Rect((self.windowDimensions[0]+100,bottomPipeY),(100,self.windowDimensions[1]))
        return [topPipe,bottomPipe]
        
    def jumped(self,state):
        self.jump = state
    def update(self):
        if(self.alive):
            self.acceleration = 9
            self.velocity = 0
            # print(self.guiObject.center)
            if(self.jump >= 0.5):
                # print(self.rect.center)
                self.acceleration -= 15
      
            self.velocity += self.acceleration
            dY = self.velocity+0.5*self.acceleration

            if(self.rect.top+dY <= 0):
                dY = 0 - self.rect.top
            if(self.rect.bottom+dY >= self.windowDimensions[1]):
                dY = self.windowDimensions[1] - self.rect.bottom

            self.rect.y += dY

            for p in self.pipes:
                if(p[0].center[0] < 0):
                    self.pipes.remove(p)
                p[0].move_ip(-5,0)
                p[1].move_ip(-5,0)

                if(p[0].center[0] == self.rect.center[0]+3):
                    self.score += 1
               

                if(p[0].center[0] == self.rect.center[0]+3+(0.5*self.windowDimensions[0])):
                    self.pipes.append(self.createPipe())
           
            if(len(self.pipes) < 1):
                self.pipes.append(self.createPipe())

 
                
