import pygame
import os
from random import randint, choice

import settings
import gameover
from objects import Player, AllyBullet, Collectable
from strategies import *

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.display.set_caption('Polygon Wars')

def main(difficulty=2):
    # Altera parâmetros para dificuldade
    if difficulty == 2 :
        settings.INITIAL_HP = 5
        settings.INITIAL_ATKSP = 2
        settings.FPS = 120
        pygame.mixer.music.load('./bullet-hell/assets/sound-berssek.mp3')
        pygame.mixer.music.play(-1)
        settings.player_color = settings.red
        settings.INVINCIBILITY_FRAMES = 40
        settings.INITIAL_PLAYER_SPEED = 2
        settings.COLLECTABLE_SPAWN_CHANCE == 20
    
    else:
        pygame.mixer.music.load('./bullet-hell/assets/music-game-normal.mp3')
        pygame.mixer.music.play(-1)

    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)

    player = Player(hp=settings.INITIAL_HP, speed=settings.INITIAL_PLAYER_SPEED, atkspd=settings.INITIAL_ATKSP)

    # Grupos de sprites
    bullets = pygame.sprite.Group()
    ally_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    collectables = pygame.sprite.Group()

    # Informações mostradas ao jogador
    killed_enemies = 0
    playerinvincible_counter = 0
    alliedbulletspeed = settings.INITIAL_ALLY_BULLET_SPEED
    playerinvincible = False

    #Sound effects
    sound_damage = pygame.mixer.Sound('./bullet-hell/assets/sound-damage.mp3')
    sound_shoot = pygame.mixer.Sound('./bullet-hell/assets/sound-shoot2.wav')
    sound_shoot.set_volume(0.3)
    sound_collectable = pygame.mixer.Sound('./bullet-hell/assets/sound-collectable.mp3')
    sound_collectable.set_volume(0.3)
    sound_enemy_die = pygame.mixer.Sound('./bullet-hell/assets/sound-enemy-die.wav')
    sound_enemy_die.set_volume(0.25)
    
    counter = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        # handle screen resizing
        current_screen_width, current_screen_height = pygame.display.get_surface().get_size()

        # é possível controlar o passo do jogo (dificuldade), alterando o mod, allways chose a multiple of 60
        playerinvincible_counter -= 1
        if playerinvincible_counter == 0:
            playerinvincible = False
        counter += 1
        counter = counter % 1200
        screen.fill((settings.background_color))

        # handle screen resizing
        current_screen_width, current_screen_height = pygame.display.get_surface().get_size()
        for event in pygame.event.get():
            # Controla redimensionamento da tela
            current_screen_width, current_screen_height = screen.get_size()
            if current_screen_width < settings.MIN_SCREEN_WIDTH or current_screen_height < settings.MIN_SCREEN_HEIGHT:
                screen = pygame.display.set_mode((max(settings.MIN_SCREEN_WIDTH, current_screen_width), max(settings.MIN_SCREEN_HEIGHT, current_screen_height)), pygame.RESIZABLE)
            if current_screen_width > settings.MAX_SCREEN_WIDTH or current_screen_height > settings.MAX_SCREEN_HEIGHT:
                screen = pygame.display.set_mode((min(settings.MIN_SCREEN_WIDTH, current_screen_width), min(settings.MIN_SCREEN_HEIGHT, current_screen_height)), pygame.RESIZABLE)
            settings.SCREEN_WIDTH = screen.get_size()[0]
            settings.SCREEN_HEIGHT = screen.get_size()[1]
            # Controla fim do programa
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # controla tiro do player
        if pygame.mouse.get_pressed()[0] and player.can_shoot:
            sound_shoot.play()
            player.last_shot = counter
            shoot_player = (AllyBullet(alliedbulletspeed, 1, player_object=player))
            ally_bullets.add(shoot_player)
            all_sprites.add(shoot_player)

        player.update(pygame.key.get_pressed(), counter)
        ally_bullets.update()

        # Controla dinâmica de criação de inimigos 
        # (usamos o % mod para controlar os intervalos entre a criação de strategies)
        if killed_enemies <= 100: # estágio 1
            if  counter % 20 == 0 and 600 <= counter < 1200 and player.hp >= settings.INITIAL_HP//3:
                strategy_leftright(6, bullets, all_sprites, 20,2)
            if counter % 120 == 0:
                strategy_chase_bullet(bullets, all_sprites, player)
        elif killed_enemies > 100 and killed_enemies <= 250: # estágio 2
            if  counter % 20 == 0 and 600 <= counter < 1200 and player.hp >= settings.INITIAL_HP//3:
                strategy_leftright(6, bullets, all_sprites, 20,3)
            if counter%90 == 0:
                strategy_updown(5, bullets, all_sprites, 20)
            if counter % 120 == 0:
                strategy_chase_bullet(bullets, all_sprites, player)
        elif killed_enemies > 250 and killed_enemies <= 500: # estágio 3
            if counter%20 == 0:    
                diagonal(6, bullets, all_sprites, 15, 3)
            if counter% 120 == 0:
                strategy_guided_square_bottom(bullets, all_sprites, player)
            if counter % 200 == 0:
                strategy_leftright(20,bullets, all_sprites,20,2)
        elif 1000 >= killed_enemies > 500: # estágio 4
            if counter % 180 == 0:
                strategy_guided_squaretop(bullets, all_sprites, player)
                strategy_guided_square_bottom(bullets, all_sprites, player)
            if counter % 240 == 0:
                strategy_guided_square_edge(bullets, all_sprites, player)
            if  counter % 20 == 0 and 300 <= counter < 1200 and player.hp >= settings.INITIAL_HP//3:
                strategy_leftright(6, bullets, all_sprites, 20,5)

        elif 2000 > killed_enemies > 1000: # último estágio
            if counter % 60 == 0:
                strategy_chase_bullet(bullets, all_sprites, player)
            if counter % 10 == 0:
                strategy_star(bullets, all_sprites, 5,2)
            if counter % 240 == 0:
                strategy_star(bullets, all_sprites, 10,5)
        elif killed_enemies > 2000:
            if counter%10 == 0:
                strategy_guided_square_edge(bullets, all_sprites, player)
        bullets.update()

        # Lógica de spawn de coletável
        if counter == 1 and difficulty != 2 and settings.MODE != "BERSERK":
            col = Collectable(((randint(0,settings.SCREEN_WIDTH-settings.COLLECTABLE_RADIUS),randint(0,settings.SCREEN_HEIGHT-settings.COLLECTABLE_RADIUS))),settings.COLLECTABLE_RADIUS,(settings.green))
            collectables.add(col)
            all_sprites.add(col)

        # Lógica de colisões entre player e coletaveis
        collided_collectable = pygame.sprite.spritecollideany(player, collectables)
        if collided_collectable:
            sound_collectable.play()
            if collided_collectable.color == (settings.green):
                player.hp += 1
            elif collided_collectable.color == (settings.blue):
                player.set_atkspd(1)

            elif collided_collectable.color == (settings.yellow) and alliedbulletspeed < 10:
                alliedbulletspeed += 1
            collided_collectable.kill()

        # Lógica de colisões entre player e tiros inimigos
        collided_enemy = pygame.sprite.spritecollideany(player, bullets)
        if collided_enemy:
            collided_enemy.kill()
            if not playerinvincible:
                playerinvincible = True
                sound_damage.play()
                player.hp -= 1
                playerinvincible_counter = settings.INVINCIBILITY_FRAMES
                if player.hp <= 0:
                    player.kill()
                    killed_enemies_total = killed_enemies
                    pygame.mixer.music.stop()
                    gameover.gameover()
                    running = False

        # Lógica de colisões com entre tiros inimigos e aliados
        for A_bullet in ally_bullets:
            collided_bullet_enemy = pygame.sprite.spritecollideany(A_bullet, bullets)
            if collided_bullet_enemy:
                collided_bullet_enemy.hp -= A_bullet.hp
                if collided_bullet_enemy.hp <= 0:
                    if randint(0,99)in range(settings.COLLECTABLE_SPAWN_CHANCE):
                        colorlist = [(settings.blue),(settings.yellow)] # hp, atksp, bulletspeeda
                        col = Collectable(((collided_bullet_enemy.rect.center)),settings.COLLECTABLE_RADIUS,choice(colorlist))
                        collectables.add(col)
                        all_sprites.add(col)
                    sound_enemy_die.play()
                    collided_bullet_enemy.kill()
                    killed_enemies += 1
                A_bullet.kill()
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Atualiza informações mostradas ao jogador
        for i in range(0, player.hp):
            pygame.draw.circle(screen, (settings.green),
                               (settings.SCREEN_WIDTH - 20 - (i * 20), 25), 5)
        enemiesDisplay = settings.score_font.render(str(f'Kills  {killed_enemies}'), 10, (settings.white))
        screen.blit(enemiesDisplay, (20, 20))

        # prints attack speed
        attack_speed_icon = pygame.image.load(os.path.abspath('./bullet-hell/assets/attack-speed.png'))
        attack_speed_icon = pygame.transform.scale(attack_speed_icon, (35, 35))
        screen.blit(attack_speed_icon, (20, 90))

        attack_speedDisplay = settings.stats_font.render(str(player.atkspd), 10, (settings.white))
        screen.blit(attack_speedDisplay, (70, 95))

        # prints bullet speed
        bullet_speed_icon = pygame.image.load(os.path.abspath('./bullet-hell/assets/bullet-speed.png'))
        bullet_speed_icon = pygame.transform.scale(bullet_speed_icon, (35, 35))
        screen.blit(bullet_speed_icon, (20, 150))

        bullet_speedDisplay = settings.stats_font.render(str(alliedbulletspeed), 10, (settings.white))
        screen.blit(bullet_speedDisplay, (70, 155))
        
        pygame.display.flip()
        clock.tick(settings.FPS) # Altera o fps do jogo

if __name__ == "__main__":
    main()