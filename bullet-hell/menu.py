import pygame
import os

import main
import settings
from objects import Button

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Polygon Wars')

font_play = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 48)
font_berserk = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 14)
font_logo = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 86)

running = True

while running:
    screen.fill((0, 0, 0))
    clock.tick(settings.FPS)

    # handle screen resizing
    current_screen_width, current_screen_height = pygame.display.get_surface().get_size()

    for event in pygame.event.get():
        # Controla redimensionamento da tela
        current_screen_width, current_screen_height = screen.get_size()
        settings.SCREEN_WIDTH = screen.get_size()[0]
        settings.SCREEN_HEIGHT = screen.get_size()[1]
        # Controla fim do programa
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    logo = font_logo.render("Polygon Wars", True, (255, 255, 255))

    screen.blit(logo, logo.get_rect(
        center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 - 200)))

    button_play = Button("Play", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 50, True, 300, 150, font_play,
                        (255, 255, 255), (50, 50, 50), (0, 0, 0), (255, 255, 255), 10, screen)

    button_berserk = Button("Berserk Mode", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 200, True, 180, 90, font_berserk,
                            (255, 255, 255), (50, 50, 50), (0, 0, 0), (255, 255, 255), 10, screen)

    if button_play.check_click():
        main.main(1)

    if button_berserk.check_click():
        main.main(2)

    pygame.display.flip()
pygame.quit()
