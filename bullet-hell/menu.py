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

#Musica menu
music_menu = pygame.mixer.Sound('./bullet-hell/assets/music-menu.mp3')
music_menu.play(-1)
sound_button_hover = pygame.mixer.Sound('./bullet-hell/assets/button-sound.mp3')


running = True

while running:
    screen.fill(settings.background_color)
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

    logo = settings.font_logo.render("Polygon Wars", True, (255, 255, 255))
    screen.blit(logo, logo.get_rect(
        center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 - 200)))

    button_play = Button("Play", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 50, True, 300, 150, settings.font_play,
                        (255, 255, 255), (50, 50, 50), settings.background_color, (255, 255, 255), 10, screen, sound_button_hover )
    
    button_berserk = Button("Berserk Mode", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 200, True, 180, 90, settings.font_berserk,
                            (255, 255, 255), (50, 50, 50), settings.background_color, (255, 255, 255), 10, screen, sound_button_hover)

    if button_play.check_click():
        music_menu.stop()
        main.main(1)

    if button_berserk.check_click():
        music_menu.stop()
        main.main(2)

    pygame.display.flip()
pygame.quit()
