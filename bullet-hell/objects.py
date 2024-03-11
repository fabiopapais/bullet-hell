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

class Player(pygame.sprite.Sprite):
    def __init__(self, HP: int):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
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

        # keeps player on the screen
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
        # spawns the enemy anywhere 200 blocks far from the edge
        self.rect = self.surf.get_rect(
            center=position
        )
        self.speed = 1

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
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

def vector2d(endP: list, startP: list, speed: int) -> list:
    """
    recives two points and the value that you want the resulting vector to be scaled to 
    """
    Norm = sqrt((endP[0] - startP[0])**2+(endP[1] - startP[1])**2)
    K = speed/Norm
    return [(endP[0] - startP[0])*K, -(endP[1] - startP[1])*K]

def strategy_reset(grid):
        for i in range(SCREEN_HEIGHT//10):
            for j in range(SCREEN_WIDTH//10):
                spawner_atual = grid[i][j]
                spawner_atual.active = False
                spawner_atual.set_speed((0,0))


def strategy_updown(grid):
        base = [2,27,52,77,98]
        velocidade_base = (0,1)
        for j in base:
            spawner_atual = grid[0][j]
            spawner_atual.active = True
            spawner_atual.set_speed(velocidade_base)

def strategy_leftright(grid):
        base = [2,22,42,62,78]
        velocidade_base = (1,0)
        for j in base:
            spawner_atual = grid[j][0]
            spawner_atual.active = True
            spawner_atual.set_speed(velocidade_base)


def strategy_fast(grid, player):
    print(len(grid),len(grid[0]))
    basee = [0,99]
    bas = [50]
    for a in basee:
        for b in bas:
            spawner_atual = grid[b][a]
            spawner_atual.active = True
            spawner_atual.set_speed(vector2d([player.rect.centerx,player.rect.centery],[b*10,a*10],1))
    

        