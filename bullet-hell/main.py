import pygame

from settings import *
from objects import Player, AllyBullet
from strategies import *

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player(hp=INITIAL_HP, speed=INITIAL_PLAYER_SPEED)

    # Grupos de sprites
    bullets = pygame.sprite.Group()
    ally_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Informações mostradas ao jogador
    killed_enemies = 0
    myFont = pygame.font.SysFont("Times New Roman", 50)

    counter = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        counter += 1
        # é possível controlar o passo do jogo (dificuldade), alterando o mod
        counter = counter % 500
        screen.fill((0, 0, 0))

        # Controla fim do programa
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # controla tiro do player
        if pygame.mouse.get_pressed()[0] and (counter % INITIAL_ALLY_BULLET_COOLDOWN == 0):
            shoot_player = (AllyBullet(2.3, 1, player_object=player))
            ally_bullets.add(shoot_player)
            all_sprites.add(shoot_player)

        player.update(pygame.key.get_pressed())
        ally_bullets.update()

        # Controla dinâmica de criação de inimigos 
        # (usamos o % mod para controlar os intervalos entre a criação de strategies)
        if counter == 2:
            strategy_updown(5, bullets, all_sprites)
        if player.rect.centerx < 200 and counter % 30 == 0:
            strategy_leftright(6, bullets, all_sprites)
        if player.hp < 3 and counter % 30 == 0:
            strategy_square(bullets, all_sprites)
        if player.rect.centerx > 650 and counter % 120 == 0:
            strategy_guided_square(bullets, all_sprites)
        if counter % 120 == 0:
            strategy_chase_bullet(bullets, all_sprites, player)
        bullets.update()

        # Lógica de colisões entre player e tiros inimigos
        collided_enemy = pygame.sprite.spritecollideany(player, bullets)
        if collided_enemy:
            collided_enemy.kill()
            player.hp -= 1
            if player.hp <= 0:
                player.kill()
                running = False

        # Lógica de colisões com entre tiros inimigos e aliados (TODO: avaliar forma mais eficiente)
        for bullet in ally_bullets:
            collided_bullet_enemy = pygame.sprite.spritecollideany(
                bullet, bullets)
            if collided_bullet_enemy:
                collided_bullet_enemy.hp -= bullet.hp
                if collided_bullet_enemy.hp <= 0:
                    collided_bullet_enemy.kill()
                    killed_enemies += 1
                bullet.kill()

        # Atualiza informações mostradas ao jogador
        enemiesDisplay = myFont.render(
            str(killed_enemies), 10, (255, 255, 255))
        screen.blit(enemiesDisplay, (20, 5))
        for i in range(0, player.hp):
            pygame.draw.circle(screen, (0, 0, 255),
                               (SCREEN_WIDTH - 20 - (i * 20), 25), 5)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
        clock.tick(120) # Altera o fps do jogo
    pygame.quit()


if __name__ == "__main__":
    main()
