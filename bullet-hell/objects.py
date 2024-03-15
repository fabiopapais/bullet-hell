import pygame
import random

from math import sqrt
from settings import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
gsd = 10 #instead of creating a grid of 1000x800 we creat a grid of 100x80
class Player(pygame.sprite.Sprite):
    def __init__(self, HP: int):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (500, 400))
        self.hp = HP

    # Moves the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, HP: int, speed: tuple, position: tuple):
        """
        The velocity and position are defined as (x, y)
        """
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 20)) #tamanho do quadrado
        self.surf.fill((255, 0, 0))
        self.hp = HP
        self.xvelocity = speed[0]
        self.yvelocity = speed[1]
        self.rect = self.surf.get_rect(
            center=position
        )

    def update(self):
        self.rect.move_ip(self.xvelocity, self.yvelocity)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > SCREEN_WIDTH:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.top > SCREEN_HEIGHT:
            self.kill()
        

class Spawner(pygame.sprite.Sprite): 
    """
    spawner invisiveis sem colisao
    """
    def __init__(self,x:int , y:int, active= False) -> None:
        super(Spawner, self).__init__()
        self.x = x
        self.y = y
        self.active = active

    def set_speed(self, speed: tuple):
        self.speed = speed

    def update(self) -> Enemy: #vai ser o bagulho que escolhe o padrao de inimigos que vai dar essa velocidade, fixa ou relativa ao player
        if self.active:
            return Enemy(HP=1, speed=self.speed, position=(self.x, self.y))

def strategy_reset(grid):
        for i in range(SCREEN_HEIGHT//gsd):
            for j in range(SCREEN_WIDTH//gsd):
                spawner_atual = grid[i][j]
                spawner_atual.active = False
                spawner_atual.set_speed((0,0))

def strategy_updown(grid):
        base = [2,(SCREEN_WIDTH//(5*gsd)),(2*SCREEN_WIDTH//(5*gsd)),(3*SCREEN_WIDTH//(5*gsd)),(4*SCREEN_WIDTH//(5*gsd)),(SCREEN_WIDTH//gsd -2)]
        velocidade_base = (0,1)
        for j in base:
            spawner_atual = grid[0][j]
            spawner_atual.active = True
            spawner_atual.set_speed(velocidade_base)

def strategy_leftright(grid):
        base = [2,(SCREEN_HEIGHT//(5*gsd)),(2*SCREEN_HEIGHT//(5*gsd)),(3*SCREEN_HEIGHT//(5*gsd)),(4*SCREEN_HEIGHT//(5*gsd)),(SCREEN_HEIGHT//gsd -2)]
        velocidade_base = (1,0)
        for j in base:
            spawner_atual = grid[j][0]
            spawner_atual.active = True
            spawner_atual.set_speed(velocidade_base)


cord = ((20,20),(20,70),(60,20),(60,70))
vel = ((0,1),(-1,0),(1,0),(0,-1))
def strategy_square(grid, cordenadas: tuple,velocidades: tuple):
    for a in cordenadas:
        for b in velocidades:
            spawner_atual = grid[a[0]][a[1]]
            spawner_atual.active = True
            spawner_atual.set_speed((b[0],b[1]))
            print(spawner_atual.__dict__)

# class Colectable(pygame.sprite.Sprite):
#     def speed 
            
class Shoot_player(pygame.sprite.Sprite):
    def __init__(self, position : tuple , speed : tuple, direction : tuple):
        super(Shoot_player, self).__init__()
        self.positionx = position[0]
        self.positiony = position[1]
        self.speed = speed
        self.direction = direction
        self.surf = pygame.surface((20, 15))
        self.surf.fill((102, 0, 0))
        self.rect = self.surf.get_rect(center=position)

        