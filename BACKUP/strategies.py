from settings import *
from objects import *

# essa função facilita a criação de divisões e coordenadas pelo mapa, substituindo a lógica de grid
# cria 'divide_by' divisões no intervalo [0 a 'interval'] especificado,
# adicionando um 'padding' aos lados
# exemplo: interval = SCREEN_WIDTH = 1000, divide_by = 5, padding = 60
# retorna [60, 280, 500, 720, 940]
def base_coords_generator(interval: int, divide_by: int, padding: int = 60):
    division_size = (interval - padding*2) / (divide_by - 1)
    base_coords = []
    for division in range(0, divide_by):
        base_coords.append(int(division_size*division + padding))
    return base_coords

# cria a quantidade de inimigos desejada dispostos horizontalmente na parte de cima do mapa


def strategy_updown(enemies_quantity, enemies_sprite_group, all_sprite_group):
    base_coords = base_coords_generator(SCREEN_WIDTH, enemies_quantity, 20)
    base_velocity = (0, 1)
    for coord in base_coords:
        new_enemy = Enemy(HP=1, speed=base_velocity, position=(coord, 0))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)

# cria a quantidade de inimigos desejada dispostos verticalmente na parte da esquerda do mapa


def strategy_leftright(enemies_quantity, enemies_sprite_group, all_sprite_group):
    base_coords = base_coords_generator(SCREEN_HEIGHT, enemies_quantity, 20)
    base_velocity = (1, 0)
    for coord in base_coords:
        new_enemy = Enemy(HP=3, speed=base_velocity, position=(0, coord))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)


def strategy_square(enemies_sprite_group, all_sprite_group):
    coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]),
                (coordsX[0], coordsY[1]), (coordsX[1], coordsY[1])]
    base_vels = ((0, 1), (-1, 0), (1, 0), (0, -1))
    for i, coord in enumerate(coords):
        new_enemy = Enemy(HP=1, speed=base_vels[i], position=coord)
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)


def strategy_guided_square(enemies_sprite_group, all_sprite_group):
    coordsX = base_coords_generator(SCREEN_WIDTH, 2, SCREEN_WIDTH // 2 - 100)
    coordsY = base_coords_generator(SCREEN_HEIGHT, 2, SCREEN_HEIGHT // 2 - 100)
    coords = [(coordsX[0], coordsY[0]), (coordsX[1], coordsY[0]),
                (coordsX[0], coordsY[1]), (coordsX[1], coordsY[1])]
    for i, coord in enumerate(coords):
        new_enemy = GuidedBullet(
            HP=1, speed=1.3, position=coord, target_position=(500, 400))
        enemies_sprite_group.add(new_enemy)
        all_sprite_group.add(new_enemy)


def strategy_chase_bullet(enemies_sprite_group, all_sprite_group, player_object):
    new_enemy = ChaseBullet(HP=1, speed=1, position=(randrange(
        0, SCREEN_WIDTH), randrange(0, SCREEN_HEIGHT)), player_object=player_object)
    enemies_sprite_group.add(new_enemy)
    all_sprite_group.add(new_enemy)