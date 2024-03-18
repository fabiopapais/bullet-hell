import pygame

from random import randint, choice
from settings import *
from objects import Player, AllyBullet, Collectable
from strategies import *

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player(hp=INITIAL_HP, speed=INITIAL_PLAYER_SPEED, atkspd=INITIAL_ATKSP)
    playerinvincible = False
    playerinvincible_counter = 0

    # Grupos de spriteswd
    bullets = pygame.sprite.Group()
    ally_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    collectables = pygame.sprite.Group()
    # Informações mostradas ao jogador
    killed_enemies = 0
    myFont = pygame.font.SysFont("Comic sans", 50)
    alliedbulletspeed = INITIAL_ALLY_BULLET_SPEED
    
    counter = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        # é possível controlar o passo do jogo (dificuldade), alterando o mod, allways chose a multiple of 60
        playerinvincible_counter -= 1
        if playerinvincible_counter == 0:
            playerinvincible = False
        counter += 1
        counter = counter % 1200
        screen.fill((0, 0, 0))

        # Controla fim do programa
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # controla tiro do player
        if pygame.mouse.get_pressed()[0] and player.can_shoot:
            player.last_shot = counter
            shoot_player = (AllyBullet(alliedbulletspeed, 1, player_object=player))
            ally_bullets.add(shoot_player)
            all_sprites.add(shoot_player)

        player.update(pygame.key.get_pressed(), counter)
        ally_bullets.update()

        # Controla dinâmica de criação de inimigos 
        # (usamos o % mod para controlar os intervalos entre a criação de strategies)
        if counter%200 == 0:
            strategy_updown(5, bullets, all_sprites, 20)
        if  counter % 20 == 0 and 600 <= counter < 1200 and player.hp >= INITIAL_HP//3 and 100 > killed_enemies > 50:
            strategy_leftright(6, bullets, all_sprites, 20)
        if player.hp < 3 and counter % 30 == 0:
            strategy_square(bullets, all_sprites, 20)
        if counter % 240 == 0:
            strategy_guided_square(bullets, all_sprites, player)
        if counter % 120 == 0:
            strategy_chase_bullet(bullets, all_sprites, player)
        if counter%20 == 0 and killed_enemies > 100 and 300<counter<600:    
            diagonal(6, bullets, all_sprites, 15)
        # strategy_guided_squaretop(bullets, all_sprites, player)
        # strategy_guided_squarebottom(bullets, all_sprites, player)
        bullets.update()
        # Lógica de spawn de coletável
        if counter == 1:
            col = Collectable(((randint(0,SCREEN_WIDTH-COLLECTABLE_RADIUS),randint(0,SCREEN_HEIGHT-COLLECTABLE_RADIUS))),COLLECTABLE_RADIUS,(0,0,255))
            collectables.add(col)
            all_sprites.add(col)

        # Lógica de colisões entre player e coletaveis
        collided_collectable = pygame.sprite.spritecollideany(player, collectables)
        if collided_collectable:
            if collided_collectable.color == (0,0,255):
                player.hp += 1
            elif collided_collectable.color == ("#FAEC5D"):
                player.set_atkspd(1)

            elif collided_collectable.color == ("#D164FA") and alliedbulletspeed < 10:
                alliedbulletspeed += 1
            collided_collectable.kill()

        # Lógica de colisões entre player e tiros inimigos
        collided_enemy = pygame.sprite.spritecollideany(player, bullets)
        if collided_enemy:
            collided_enemy.kill()
            if not playerinvincible:
                playerinvincible = True
                player.hp -= 1
                playerinvincible_counter = INVINCIBILITY_FRAMES
                if player.hp <= 0:
                    player.kill()
                    running = False

        # Lógica de colisões com entre tiros inimigos e aliados (TODO: avaliar forma mais eficiente)
        for A_bullet in ally_bullets:
            collided_bullet_enemy = pygame.sprite.spritecollideany(A_bullet, bullets)
            if collided_bullet_enemy:
                collided_bullet_enemy.hp -= A_bullet.hp
                if collided_bullet_enemy.hp <= 0:
                    if randint(0,99)in range(COLLECTABLE_SPAWN_CHANCE):
                        colorlist = [("#FAEC5D"),("#D164FA")] # hp, atksp, bulletspeeda
                        col = Collectable(((collided_bullet_enemy.rect.center)),COLLECTABLE_RADIUS,choice(colorlist))
                        collectables.add(col)
                        all_sprites.add(col)
                    collided_bullet_enemy.kill()
                    killed_enemies += 1
                A_bullet.kill()

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
        clock.tick(FPS) # Altera o fps do jogoa
    pygame.quit()


if __name__ == "__main__":
    main()
