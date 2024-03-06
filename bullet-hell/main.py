import pygame
from settings import *
from objects import *
from pygame.locals import (
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )

def updategrid(grid,enemies,all_sprites):
    for y in range(SCREEN_HEIGHT//10):
                for x in range(SCREEN_WIDTH//10):
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

    player = Player(10)
    """groups to hold enemy sprites, and every sprite
    - 'enemies' is used for collision detection and position updates
    - 'all_sprites' is used for rendering"""
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    #fazendo os spawners quando o jogo rodar pela 1 vez
    grid = [[] for _ in range(SCREEN_HEIGHT//10)]
    for y in range(SCREEN_HEIGHT//10):
        for x in range(SCREEN_WIDTH//10):
            grid[y].append(Spawner(x*10, y*10))

    counter = 0
    running = True
    while running:
        counter += 1 #para o teste do strategy
        counter = counter % 2000
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
        elif counter == 1000:
            strategy_leftright(grid)
            updategrid(grid, enemies, all_sprites)
        elif counter == 1999:
            strategy_updown(grid)
            updategrid(grid, enemies, all_sprites)
        enemies.update()
        player.surf.get

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

    pygame.quit()

if __name__ == "__main__":
    main()