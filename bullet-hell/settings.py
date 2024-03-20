import pygame
import os
pygame.font.init()
# constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
MIN_SCREEN_WIDTH = 0
MIN_SCREEN_HEIGHT = 0
MAX_SCREEN_WIDTH = 2000
MAX_SCREEN_HEIGHT = 1200
INITIAL_HP = 10
INITIAL_PLAYER_SPEED = 4
INITIAL_ATKSP = 5
INITIAL_ALLY_BULLET_SPEED = 4
INVINCIBILITY_FRAMES = 20
COLLECTABLE_RADIUS = 10
COLLECTABLE_SPAWN_CHANCE = 10
FPS = 60


# colors
background_color = '#0F1420'
white = '#FFFFFF'
red = '#CF151B'
pink = '#E043D9'
orange = '#DB5F21'
green = '#34D16A'
player_color = '#4B8B9C'
yellow = '#FFE354'
blue = '#2E2EE6'

# fonts
score_font = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 30)
stats_font = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 35)
font_play = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 48)
font_berserk = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 14)
font_logo = pygame.font.Font(os.path.abspath('./bullet-hell/assets/Dune_Rise.ttf'), 86)