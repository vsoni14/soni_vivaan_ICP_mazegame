import pygame as pg

WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
TITLE = "Best game evah!!!"
FPS = 30

#Colors in rgb format
BGCOLOR = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (50, 255, 50)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

#player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5) 
# - 5 is allowing hiting but not hurting

PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)

# mob settings
MOB_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)