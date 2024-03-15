import pygame

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
        

# essa função facilita a criação de divisões e coordenadas pelo mapa, substituindo a lógica de grid
# cria 'divide_by' divisões no intervalo [0 a 'interval'] especificado, 
# adicionando um 'padding' aos lados
# exemplo: interval = SCREEN_WIDTH = 1000, divide_by = 5, padding = 60
# retorna [60, 280, 500, 720, 940]
def base_coords_generator(interval:int, divide_by:int, padding:int=60):
    division_size = (interval - padding*2) / (divide_by - 1)
    base_coords = []
    for division in range(0, divide_by):
        base_coords.append(int(division_size*division + padding))
    return base_coords

# cria a quantidade de inimigos desejada dispostos horizontalmente na parte de cima do mapa
def strategy_updown(enemies_quantity, enemies_sprite_group, all_sprite_group):
    base_coords = base_coords_generator(SCREEN_WIDTH, enemies_quantity, 20)
    base_velocity = (0,1)
    for coord in base_coords:
        new_enemy = Enemy(HP=1, speed=base_velocity, position=(coord, 0))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)


# cria a quantidade de inimigos desejada dispostos verticalmente na parte da esquerda do mapa
def strategy_leftright(enemies_quantity, enemies_sprite_group, all_sprite_group):
    base_coords = base_coords_generator(SCREEN_HEIGHT, enemies_quantity, 20)
    base_velocity = (1,0)
    for coord in base_coords:
        new_enemy = Enemy(HP=1, speed=base_velocity, position=(0, coord))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)

def strategy_square(enemies_sprite_group, all_sprite_group):
    coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]), (coordsX[0], coordsY[1]), (coordsX[1], coordsY[1])]
    vels = ((0,1),(-1,0),(1,0),(0,-1))
    print(coords)
    for i, coord in enumerate(coords):
            new_enemy = Enemy(HP=1, speed=vels[i], position=coord)
            enemies_sprite_group.add(new_enemy)
            all_sprite_group.add(new_enemy)
            print(new_enemy.__dict__)