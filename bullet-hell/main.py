import pygame
from settings import *
from objects import *
from pygame.locals import (        
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player(INITIAL_HP)
    # cria grupos de sprites
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collectables = pygame.sprite.Group() #grupo de coletaveis
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
        
        # controla criação de inimigos
        if counter == 2:
            strategy_updown(5, enemies, all_sprites)
        if player.rect.centerx < 200 and counter%30 == 0:
            strategy_leftright(6, enemies, all_sprites)
        if INITIAL_HP > player.hp and counter%30 == 0:
            strategy_square(enemies, all_sprites)

        screen.fill((0, 0, 0))

        # atualiza os sprites
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # controla colisões
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