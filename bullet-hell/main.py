import pygame
from settings import *
from objects import *
from strategies import *
from pygame.locals import (        
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player(HP=INITIAL_HP, speed=INITIAL_SPEED)
    killed_enemies = 0
    myFont = pygame.font.SysFont("Times New Roman", 50) 
    enemies = pygame.sprite.Group()
    ally_shoots = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

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

        if pygame.mouse.get_pressed()[0] and (counter % 5 == 0):
            shoot_player = (Shoot_player(player.rect.center, 2.3, 1, player_object=player))
            ally_shoots.add(shoot_player)
            all_sprites.add(shoot_player)
        
        player.update(pressed_keys)
        ally_shoots.update()

        # controla criação de inimigos
        if counter == 2:
            strategy_updown(5, enemies, all_sprites)
        if player.rect.centerx < 200 and counter%30 == 0:
            strategy_leftright(6, enemies, all_sprites)
        if player.hp < 3 and counter%30 == 0:
            strategy_square(enemies, all_sprites)
        if player.rect.centerx > 650 and counter%120 == 0:
            strategy_guided_square(enemies, all_sprites)
        if counter%120 == 0:
            strategy_chase_bullet(enemies, all_sprites, player)
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
        clock.tick(120)
    pygame.quit()

if __name__ == "__main__":
    main()