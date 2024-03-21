from dis import Instruction
import pygame

import main
import settings
from objects import Button

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def menu():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Polygon Wars')

    #Musica menu
    music_menu = pygame.mixer.Sound('./bullet-hell/assets/music-menu.mp3')
    music_menu.play(-1)

    #Efeitos sonoros
    sound_button_hover = pygame.mixer.Sound('./bullet-hell/assets/button-sound.mp3')
    sound_click = pygame.mixer.Sound('./bullet-hell/assets/sound-click.mp3')


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

        logo = settings.font_logo.render("Polygon Wars", True, (255, 255, 255))
        screen.blit(logo, logo.get_rect(
            center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 - 200)))

        instructions = settings.font_instructions.render("W A S D  to move, MOUSE to shoot", True, (255, 255, 255))
        screen.blit(instructions, instructions.get_rect(
            center = (settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 - 100) ))

        button_play = Button("Play", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 50, True, 300, 150, settings.font_play,
                        (settings.white), (settings.background_color), settings.background_color, (settings.white), (settings.white), 60, screen)

        button_berserk = Button("Berserk", settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 200, True, 180, 90, settings.font_berserk,
                            (settings.white), (settings.background_color), settings.background_color, (settings.white), (settings.white), 40, screen)
        button_play.draw()
        button_berserk.draw()

        # bersek mode instructions hover
        if button_berserk.check_hover():
            description_text = settings.font_description.render("don't spawn lives", True, (255, 255, 255))
            screen.blit(description_text, description_text.get_rect(
                center =(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2 + 270)))

        if button_play.check_click():
            sound_click.play()
            music_menu.stop()
            settings.MODE = "normal"
            main.main(1)
            running = False
        elif button_berserk.check_click():
            sound_click.play()
            music_menu.stop()
            settings.MODE = "BERSERK"
            main.main(2)
            running = False

        pygame.display.flip()
    pygame.quit()

menu()