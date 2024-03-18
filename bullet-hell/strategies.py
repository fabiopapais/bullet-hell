from random import randrange

from settings import *
from objects import *


def base_coords_generator(interval: int, divide_by: int, padding: int = 60):
    """
    Facilita a criação de divisões e coordenadas pelo mapa.

    Ela cria 'divide_by' divisões no intervalo [0 a 'interval'] especificado, adicionando um 'padding' 
    aos lados. Exemplo: chamar a função com interval = SCREEN_WIDTH = 1000, divide_by = 5, padding = 60
    retorna [60, 280, 500, 720, 940]
    """
    division_size = (interval - padding*2) / \
        (divide_by - 1)  # tamanho de cada divisão
    base_coords = []
    for division in range(0, divide_by):
        base_coords.append(int(division_size*division + padding))

    return base_coords

# cria a quantidade de inimigos desejada dispostos horizontalmente na parte de cima do mapa


def strategy_updown(enemies_quantity, enemies_sprite_group, all_sprite_group, big):
    base_coords = base_coords_generator(SCREEN_WIDTH, enemies_quantity, 20)
    base_velocity = (0, 8)
    for coord in base_coords:
        new_enemy = Bullet(hp=1, speed=base_velocity, size = big, position=(coord, 0))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)

# cria a quantidade de inimigos desejada dispostos verticalmente na parte da esquerda do mapa


def strategy_leftright(enemies_quantity, enemies_sprite_group, all_sprite_group, big):
    base_coords = base_coords_generator(SCREEN_HEIGHT, enemies_quantity, 20)
    base_velocity = (2, 0)
    for coord in base_coords:
        new_enemy = Bullet(hp=3, speed=base_velocity, size = big , position=(0, coord))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)


def strategy_square(enemies_sprite_group, all_sprite_group, big):
    coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]),
              (coordsX[0], coordsY[1]), (coordsX[1], coordsY[1])]
    base_vels = ((0, 2), (-2, 0), (2, 0), (0, -2))
    for i, coord in enumerate(coords):
        new_enemy = Bullet(hp=1, speed=base_vels[i], size = big , position=coord)
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)


def strategy_guided_square(enemies_sprite_group, all_sprite_group, player_object):
    coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]),
              (coordsX[0], coordsY[1]), (coordsX[1], coordsY[1])]
    for i, coord in enumerate(coords):
        new_enemy = GuidedBullet(
            hp=1, speed=8, position=coord, target_position=player_object.rect.center)
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)

def strategy_guided_squaretop(enemies_sprite_group, all_sprite_group, player_object):
    # coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    # coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coordsX = [200,400,600,800]
    coordsY = [0,0,]
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]),
              (coordsX[2], coordsY[1]), (coordsX[3], coordsY[1])]
    for i, coord in enumerate(coords):
        new_enemy = GuidedBullet(
            hp=1, speed=8, position=coord, target_position=player_object.rect.center)
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)

def strategy_guided_squarebottom(enemies_sprite_group, all_sprite_group, player_object):
    # coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    # coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coordsX = [200,400,600,800]
    coordsY = [SCREEN_HEIGHT,SCREEN_HEIGHT]
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]),
              (coordsX[2], coordsY[1]), (coordsX[3], coordsY[1])]
    for i, coord in enumerate(coords):
        new_enemy = GuidedBullet(
            hp=1, speed=8, position=coord, target_position=player_object.rect.center)
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)



def strategy_chase_bullet(enemies_sprite_group, all_sprite_group, player_object):
    new_enemy = ChaseBullet(hp=1, speed=2, position=(randrange(0, SCREEN_WIDTH), randrange(0, SCREEN_HEIGHT)), object_to_chase=player_object)
    enemies_sprite_group.add(new_enemy)
    all_sprite_group.add(new_enemy)

def diagonal(enemies_quantity, enemies_sprite_group, all_sprite_group, big):
    list = []
    for j in range(0 , SCREEN_WIDTH , SCREEN_WIDTH//enemies_quantity):
        list.append((j,0))
    for j in range(0 , SCREEN_HEIGHT , SCREEN_WIDTH//enemies_quantity):
        if j != 0:
            list.append((SCREEN_WIDTH,j))
    for i in list:
        new_enemy = Bullet(2,(-2,2), big,position = i)
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)
