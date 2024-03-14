import pygame
from settings import *
from objects import *
from pygame.locals import (        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )

def updategrid(grid,enemies,all_sprites):
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

    player = Player(999)
    """groups to hold enemy sprites, and every sprite
    - 'enemies' is used for collision detection and position updates
    - 'all_sprites' is used for rendering"""
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    #fazendo os spawners quando o jogo rodar pela 1 vez
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

            # elif event.type == ADDENEMY:
            #     new_enemy = Enemy(1,) 
            #     enemies.add(new_enemy)
            #     all_sprites.add(new_enemy)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        if counter == 0:
            strategy_reset(grid)
        if counter == 2:
            strategy_updown(grid)
            updategrid(grid, enemies, all_sprites)
        # if counter not in [0,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90]:
        if player.rect.centerx < 200:
            strategy_leftright(grid)
            updategrid(grid, enemies, all_sprites)
        # if counter == 1:
        #     strategy_fast(grid, player)
        #     updategrid(grid, enemies, all_sprites)
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