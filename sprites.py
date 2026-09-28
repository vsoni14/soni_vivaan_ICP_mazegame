import pygame as pg #imports pygame with shorthand of pg
from settings import * #imports everything from settings.py
from pygame.sprite import Sprite #imports Sprite class
from os import path #imports path to let us use our system's directory system
from utils import *
 
vec = pg.math.Vector2
 
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
 
def collide_with_walls(sprite, group, dir):
    #check for x collision
    if dir == 'x':
        #checking to see if we've collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx: #checks if we're to the left of the wall/object
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2 #reposition the player (sprite) to left side of wall/object
            if hits[0].rect.centerx < sprite.hit_rect.centerx: #checks if we're to the right of the wall/object
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 #reposition player (sprite) to right side of wall/object
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery: # checks to see if we are above the wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery: # checks to see if we are bellow the wall
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
 
class Player(Sprite): #creates class Player
    def __init__(self, game, x, y): #method that initializes Sprite, only runs once
        self.groups = game.all_sprites #gets all of the sprite images
        Sprite.__init__(self, self.groups) #initializes Sprite
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = self.spritesheet.get_image(0,0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        self.image = pg.Surface((TILESIZE, TILESIZE)) #gets character pixel size from settings.py
        # self.image.fill(WHITE) #fills the character white
        self.rect = self.image.get_rect() #draws rectangle for character
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]: #checks if left arrow or "a" key is pressed
            self.vel.x = -PLAYER_SPEED #makes player_speed negative on the x axis
            #self.vx = -PLAYER_SPEED #makes player_speed negative on the x axis
        if keys[pg.K_RIGHT] or keys[pg.K_d]: #checks if right arrow or "d" key is pressed
            self.vel.x = PLAYER_SPEED #makes player_speed positive on x_axis
            #self.vx = PLAYER_SPEED #makes player_speed positive on x_axis
        if keys[pg.K_UP] or keys[pg.K_w]: #checks if up arrow or "w" key is pressed
            self.vel.y = -PLAYER_SPEED #makes player_speed negative on y_axis since top left is (0,0)
            #self.vy = -PLAYER_SPEED #makes player_speed negative on y_axis since top left is (0,0)
        if keys[pg.K_DOWN] or keys[pg.K_s]: #checks if down arrow or "s" key is pressed
            self.vel.y = PLAYER_SPEED #makes player_speed positive on y_axis
            #self.vy = PLAYER_SPEED #makes player_speed positive on y_axis
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
 
    def update(self):
        self.get_keys() #waits for input from games
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
 
       
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
 
class Mob(Sprite):
    def __init__(self, game, x, y): #method that initializes Sprite, only runs once
        self.groups = game.all_sprites, game.all_mobs #gets all of the sprite images
        Sprite.__init__(self, self.groups) #initializes Sprite
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) #gets character pixel size from settings.py
        self.image.fill(RED) #fills the character white
        self.rect = self.image.get_rect() #draws rectangle for character
        self.speed = 1
        self.vx, self.vy = 500,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        print("player initialized")
        self.rect.x = self.x
        self.rect.y = self.y
 
    def update(self):
        if self.rect.x > WIDTH or self.rect.x < 0:
            print("I've broken out of my cage")
            self.speed *= -1
            self.y += TILESIZE
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x
        #self.y += self.vy * self.game.dt * self.speed
        self.rect.y = self.y
 