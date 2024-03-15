import pygame
from settings import *
from objects import *
from pygame.locals import (        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )
HP_inicial = 10
def updategrid(grid,enemies,all_sprites):
    """
    acctually creates the enimies
    """
    for y in range(SCREEN_HEIGHT//gsd):
        for x in range(SCREEN_WIDTH//gsd):
            spawner = grid[y][x]
            new_enemy = spawner.update()
            if new_enemy is not None:
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # custom event for adding a new enemy.
    ADDENEMY = pygame.USEREVENT + 1
    #pygame.time.set_timer(ADDENEMY, 500)

    player = Player(HP_inicial)
    """groups to hold enemy sprites, and every sprite
    - 'enemies' is used for collision detection and position updates
    - 'all_sprites' is used for rendering"""
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collectables = pygame.sprite.Group() #grupo de coletaveis
    all_sprites.add(player)
    #generating the spawners on the initialization
    grid = [[] for _ in range(SCREEN_HEIGHT//gsd)]
    for y in range(SCREEN_HEIGHT//gsd):
        for x in range(SCREEN_WIDTH//gsd):
            grid[y].append(Spawner(x*gsd, y*gsd))

    counter = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        counter += 1 #para o teste do strategy
        counter = counter % 500
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False


        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        
        if counter == 2:
            strategy_updown(grid)
            updategrid(grid, enemies, all_sprites)
        if player.rect.centerx < 200 and counter%30 == 0:
            strategy_leftright(grid)
            updategrid(grid, enemies, all_sprites)
        if HP_inicial//2 > player.hp and counter%30 == 0: #
            strategy_square(grid,((20,20),(20,70),(60,20),(60,70)),((0,1),(-1,0),(1,0),(0,-1)))
        
        updategrid(grid, enemies, all_sprites)
        strategy_reset(grid)
        enemies.update()

        screen.fill((0, 0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        collided_enemy = pygame.sprite.spritecollideany(player, enemies)
        if collided_enemy:
            collided_enemy.kill()
            player.hp -= 1
            if player.hp <= 0:
                player.kill()
                running = False

        pygame.display.flip()
        clock.tick(120)
    pygame.quit()

if __name__ == "__main__":
    main()