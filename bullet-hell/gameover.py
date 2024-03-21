import pygame

import main
import settings
from objects import Button

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def gameover():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(
        (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Polygon Wars')

    running = True

    while running:
        screen.fill(settings.background_color)
        clock.tick(settings.FPS)

        for event in pygame.event.get():
            # Controla redimensionamento da tela
            settings.SCREEN_WIDTH = screen.get_size()[0]
            settings.SCREEN_HEIGHT = screen.get_size()[1]
            # Controla fim do programa
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

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

        you_died = settings.font_logo.render("YOU DIED", True, (255, 0, 0))
        screen.blit(you_died, you_died.get_rect(
            center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 - 200)))

        button_restart = Button("Restart", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 50, True, 400, 150, settings.font_play,
                        (settings.white), (settings.background_color), settings.background_color, (settings.white), (settings.white), 60, screen)

        button_menu = Button("Menu", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 300, True, 180, 90, settings.font_berserk,
                            (settings.white), (settings.background_color), settings.background_color, (settings.white), (settings.white), 60, screen)
        button_restart.draw()
        button_menu.draw()

        if button_restart.check_click():
            if settings.MODE == "normal":
                main.main(1)
                running = False
            if settings.MODE == "BERSERK":
                main.main(2)
                running = False

        if button_menu.check_click():
            from menu import menu
            menu()
            running = False

        pygame.display.flip()
