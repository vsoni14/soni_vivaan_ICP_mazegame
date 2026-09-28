import pygame as pg

WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
TITLE = "Best game evah!!!"
FPS = 30

#Colors in rgb format
BGCOLOR = (255, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5) 
# - 5 is allowing hiting but not hurting