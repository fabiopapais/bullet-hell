import pygame
import main
from settings import *
from objects import Button

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Polygon Wars')

font_play = pygame.font.Font('Dune_Rise.ttf', 48)
font_berserk = pygame.font.Font('Dune_Rise.ttf', 14)
font_logo = pygame.font.Font('Dune_Rise.ttf', 86)

running = True

while running :
     screen.fill((0,0,0))
     clock.tick(FPS)
    
     # Controla fim do programa
     for event in pygame.event.get():
          if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                    running = False
          elif event.type == QUIT:
                    running = False

     logo = font_logo.render("Polygon Wars", True, (255,255,255))

     screen.blit(logo, logo.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 -200)))

     button_play = Button("Play",SCREEN_WIDTH/2, SCREEN_HEIGHT/2  + 50, True, 300, 150, font_play,
                           (255,255,255), (50,50,50), (0,0,0), (255,255,255), 10, screen)
     
     button_berserk = Button("Berserk Mode",SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200, True, 180, 90, font_berserk,
                           (255,255,255), (50,50,50), (0,0,0), (255,255,255), 10, screen)

     if button_play.check_click() :
          main.main(1)

     if button_berserk.check_click() :
          main.main(2)

     pygame.display.flip()
pygame.quit()