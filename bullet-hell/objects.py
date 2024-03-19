import pygame

from settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
)


class Player(pygame.sprite.Sprite):
    """
    Classe que representa o jogador.

    Será instanciada apenas uma vez, e basicamente controla a movimentação
    na horizontal, vertical e rotação do player (com base na posição do mouse)
    """

    def __init__(self, hp: int, speed: int = 2):
        """
        Inicializa a classe.

        Args:
            hp: quantidade de vidas inicial do player
            speed: velocidade inicial do player
        """
        super(Player, self).__init__()
        self.surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.surf, pygame.Color('steelblue2'), [
                            (0, 0), (0, 40), (40, 20)])  # cria triângulo do player
        # spawna o player no centro do mapa
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.hp = hp
        self.speed = speed

        # armazena a posição como vetor
        self.position = pygame.Vector2(self.rect.center)
        self.original_surf = self.surf  # cópia do surf para auxiliar rotação

    def update(self, pressed_keys):
        """
        Movimenta o player na horizontal/vertical e faz rotação baseada no mouse.

        Args:
            pressed_keys: teclas clicadas pelo jogador
        """
        self.rotate()  # rotação do player

        # movimentação horizontal/vertical do player
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        # impede player de sair da tela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # assinala posição rect à propriedade pos
        self.position = pygame.Vector2(self.rect.center)

    # função que realiza rotação com base na posição do mouse
    def rotate(self):
        # cria um vetor com da posição atual até o mouse
        direction = pygame.mouse.get_pos() - self.position
        _, angle = direction.as_polar()  # extrai a direção em graus do vetor direction

        self.surf = pygame.transform.rotate(self.original_surf, -angle)
        self.rect = self.surf.get_rect(center=self.rect.center)


class Bullet(pygame.sprite.Sprite):
    """
    Tiro inimigo convencional.

    Cria um tiro comum, que irá seguir na direção determinada pela
    velocidade até atingir o player, ser destruído ou chegar ao fim do mapa
    """

    def __init__(self, hp: int, speed: tuple, position: tuple):
        """
        Inicializa a classe.

        Args:
            hp: quantidade de "vidas" do tiro
            speed: velocidade de deslocamento em (x,y) do tiro
            position: posição em (x,y) onde o tiro será spawnado
        """
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=position
        )
        self.hp = hp
        self.speed = speed

    def update(self):
        """
        Movimenta o tiro a cada iteração com base na velocidade especificada
        """
        self.rect.move_ip(self.speed[0], self.speed[1])
        # impede tiro de sair da tela
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > SCREEN_WIDTH:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.top > SCREEN_HEIGHT:
            self.kill()


class GuidedBullet(pygame.sprite.Sprite):
    """
    Tipo de Bullet guiado numa direção. 

    Spawna no lugar desejado e anda indefinidamente na direção da posição especificada
    até colidir com o player, ser destruído ou chegar ao fim do mapa.
    """

    def __init__(self, hp: int, speed: float, position: tuple, target_position: tuple):
        """
        Inicializa a classe.

        Args:
            hp: quantidade de "vidas" do tiro
            speed: velocidade de deslocamento do tiro em float
            position: posição em (x,y) onde o tiro será spawnado
            target_position: posição em (x,y) para onde o tiro deve seguir
        """
        super(GuidedBullet, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 125, 0))
        self.hp = hp
        self.rect = self.surf.get_rect(
            center=position
        )
        self.speed = speed
        # posições convertidas em vetores
        self.position = pygame.Vector2(position)
        self.target_position = pygame.Vector2(target_position)
        # este método transforma o vetor resultante das duas posições em um vetor
        # com distância (magnitude) 1, mantendo sua direção.
        self.direction = (self.target_position - self.position).normalize()

    def update(self):
        """
        Move o inimigo na direção especificada com determinada velocidade,
        multiplicando o vetor normalizado pela velocidade desejada e somando ele à posição
        """
        self.position += self.direction * self.speed
        # assinala a posição ao rect, efetuando a mudança na posição do sprite
        self.rect.center = self.position


class ChaseBullet(pygame.sprite.Sprite):
    """
    Tipo de Bullet guiado em tempo real à posição de um objeto. 

    Spawna no lugar desejado e anda em direção da posição de um objeto fornecido
    (como o player, por exemplo) até colidir com o player ou ser destruído.
    """

    def __init__(self, hp: int, speed: float, position: tuple, object_to_chase: object):
        """
        Inicializa a classe.

        Args:
            hp: quantidade de "vidas" do tiro
            speed: velocidade de deslocamento do tiro em float
            position: posição em (x,y) onde o tiro será spawnado
            object_to_chase: objeto que será seguindo (deve ter a propriedade .position)
        """
        super(ChaseBullet, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 0, 130))
        self.rect = self.surf.get_rect(
            center=position
        )
        self.hp = hp
        self.speed = speed
        self.position = pygame.Vector2(position)
        self.object_to_chase = object_to_chase

    def update(self):
        """
        Move o inimigo na direção especificada com determinada velocidade,
        calculando a direção pela posição atual do objeto
        """
        direction = (pygame.Vector2(self.object_to_chase.position) -
                     self.position).normalize()
        # Move o inimigo na direção especificada com determinada velocidade
        self.position += direction * self.speed
        self.rect.center = self.position


class AllyBullet(pygame.sprite.Sprite):
    """
    Bullet atirada pelo usuário. 

    Spawna na frente do player e anda em direção da posição do mouse
    até colidir com outra Bullet inimiga ou chegar ao fim do mapa.
    """

    def __init__(self, speed: int, hp: int, player_object: object):
        """
        Inicializa a classe.

        Args:
            hp: posição do tiro
            speed: velocidade de deslocamento do tiro em float
            position: posição em (x,y) onde o tiro será spawnado
            player_object: objeto do player para consultar posição atual
        """
        super(AllyBullet, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 100, 92))
        self.speed = speed
        self.hp = hp
        # direção definitiva que irá ser seguida
        self.direction = (pygame.mouse.get_pos() -
                          player_object.position).normalize()
        # ela é spawnada um pouco à frente do player
        self.rect = self.surf.get_rect(
            center=pygame.Vector2(player_object.position + self.direction * 25)
        )
        self.position = self.rect.center

    def update(self):
        """
        Move o tiro na direção determinada com determinada velocidade e
        previne que saia da borda do mapa
        """
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
