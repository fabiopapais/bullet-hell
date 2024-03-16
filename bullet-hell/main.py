import pygame
from settings import *
from objects import *
from pygame.locals import (
        K_ESCAPE,
        KEYDOWN,
        QUIT,
        K_SPACE,
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
    killed_enemies = 0
    myFont = pygame.font.SysFont("Times New Roman", 50) 
    """groups to hold enemy sprites, and every sprite
    - 'enemies' is used for collision detection and position updates
    - 'all_sprites' is used for rendering"""
    enemies = pygame.sprite.Group()
    ally_shoots = pygame.sprite.Group()
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
        if pressed_keys[K_SPACE] and (counter % 5 == 0):
          shoot_player = (Shoot_player(player.rect.center, (1,2), (0 , 1), 1))
          ally_shoots.add(shoot_player)
          all_sprites.add(shoot_player)
          
        
        
        player.update(pressed_keys)
        ally_shoots.update()

        
            
        if counter % 50 == 0:
            strategy_leftright(grid)
        if counter == 1999:
            strategy_updown(grid)
        enemies.update()
        updategrid(grid, enemies, all_sprites)
        strategy_reset(grid)

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

        for bullet in ally_shoots:
          collided_bullet_enemy = pygame.sprite.spritecollideany(bullet, enemies)
          if collided_bullet_enemy:
            collided_bullet_enemy.hp -= bullet.hp
            if collided_bullet_enemy.hp <= 0:
                collided_bullet_enemy.kill()
                killed_enemies += 1
            bullet.kill()
        
        enemiesDisplay = myFont.render(str(killed_enemies), 10, (255, 255, 255))
        screen.blit(enemiesDisplay, (20, 5))
        
        for i in range(0,player.hp) :
          pygame.draw.circle(screen, (0, 0, 255), (SCREEN_WIDTH -   20 - (i *20), 25), 5)
              

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()