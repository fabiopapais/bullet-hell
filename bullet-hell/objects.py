from random import random, randrange
import pygame

from math import sqrt
from settings import *

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, HP: int, speed:int=2):
        super(Player, self).__init__()
        self.surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.surf, pygame.Color('steelblue2'), [(0, 0), (0, 40), (40, 20)])
        self.rect = self.surf.get_rect(center=(500, 400))
        self.hp = HP
        self.speed = speed

        # for Player rotation
        self.pos = pygame.Vector2(self.rect.center)
        self.orig_surf = self.surf

    # Moves the sprite based on keypresses
    def update(self, pressed_keys):
        # for Player rotation
        self.rotate()
        
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -2)
            
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 2)
            
        if pressed_keys[K_a]:
            self.rect.move_ip(-2, 0)
            
        if pressed_keys[K_d]:
            self.rect.move_ip(2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        self.pos = pygame.Vector2(self.rect.center)
        
    def rotate(self):
        direction = pygame.mouse.get_pos() - self.pos
        
        radius, angle = direction.as_polar()
        
        self.surf = pygame.transform.rotate(self.orig_surf, -angle)
        
        self.rect = self.surf.get_rect(center=self.rect.center)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, HP: int, speed: tuple, position: tuple):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 20))  # tamanho do quadrado
        self.surf.fill((255, 0, 0))
        self.hp = HP
        self.xvelocity = speed[0]
        self.yvelocity = speed[1]
        self.rect = self.surf.get_rect(
            center=position
        )

    def update(self):
        self.rect.move_ip(self.xvelocity, self.yvelocity)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > SCREEN_WIDTH:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Um tipo de inimigo que spawna no lugar desejado e anda na direção da posição especificada
class GuidedBullet(pygame.sprite.Sprite):
    def __init__(self, HP: int, speed: float, position: tuple, target_position: tuple):
        super(GuidedBullet, self).__init__()
        self.surf = pygame.Surface((20, 20))  # tamanho do quadrado
        self.surf.fill((255, 125, 0))
        self.hp = HP
        self.rect = self.surf.get_rect(
            center=position
        )
        self.speed = speed
        # convertemos as posições em vetores
        self.position = pygame.Vector2(position)
        self.target_position = pygame.Vector2(target_position)
        # este método transforma o vetor resultante das duas posições em um vetor
        # com distância (magnitude) 1, mantendo sua direção.
        self.direction = (self.target_position - self.position).normalize()

    def update(self):
        # Move o inimigo na direção especificada com determinada velocidade
        # multiplica o vetor normalizado pela velocidade desejada e soma ele à posição
        self.position += self.direction * self.speed
        # assinala a posição ao rect, efetuando a mudança na posição do sprite
        self.rect.center = self.position


# um tipo de inimigo que segue o player, dado o objeto do player
class ChaseBullet(pygame.sprite.Sprite):
    def __init__(self, HP: int, speed: float, position: tuple, player_object: object):
        super(ChaseBullet, self).__init__()
        self.surf = pygame.Surface((20, 20))  # tamanho do quadrado
        self.surf.fill((255, 0, 130))
        self.hp = HP
        self.rect = self.surf.get_rect(
            center=position
        )
        self.speed = speed
        self.position = pygame.Vector2(position)
        # assim podemos acessar a posição em tempo real do player
        self.player_object = player_object

    def update(self):
        # semelhante ao GuidedBullet, porém aqui calculamos a nova direção a cada update()
        direction = (pygame.Vector2(self.player_object.pos) -
                    self.position).normalize()
        # Move o inimigo na direção especificada com determinada velocidade
        self.position += direction * self.speed
        self.rect.center = self.position


class Shoot_player(pygame.sprite.Sprite):
    def __init__(self, position: tuple, speed: int, hp: int, player_object: object):
        super(Shoot_player, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 100, 92))
        self.rect = self.surf.get_rect(center=position)
        self.speed = speed
        self.direction = (pygame.mouse.get_pos() - player_object.pos).normalize()
        self.hp = hp
        self.position = pygame.Vector2(player_object.pos + self.direction * 25) # se quiser mudar o spawn do tiro é aqui

    def update(self):

        self.position += self.direction * self.speed
        # assinala a posição ao rect, efetuando a mudança na posição do sprite
        self.rect.center = self.position

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > SCREEN_WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()