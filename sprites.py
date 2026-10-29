import pygame as pg #imports pygame with shorthand of pg
from settings import * #imports everything from settings.py
from pygame.sprite import Sprite #imports Sprite class
from os import path #imports path to let us use our system's directory system
from utils import *
from random import randint

vec = pg.math.Vector2
 
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
 
def collide_with_walls(sprite, group, dir):
    #check for x collision
    if dir == 'x':
        #checking to see if we've collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to se if we're to the left of the wall
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
        self.coins = 0
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = self.spritesheet.get_image(0,0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE)) #gets character pixel size from settings.py
        # self.image.fill(WHITE) #fills the character white
        self.rect = self.image.get_rect() #draws rectangle for character
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # animation stuff
        self.last_update = 0
        self.current_frame = 0
        self.dir = "none"
        self.coins = 0
        self.jumping = False
        print('player instantiated')
        print(self.pos)

    def get_keys(self):
        self.dir = "none"
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]: #checks if left arrow or "a" key is pressed
            # self.vel.x = -PLAYER_SPEED #makes player_speed negative on the x axis
            self.acc.x = -PLAYER_SPEED #makes player_speed negative on the x axis
            #self.vx = -PLAYER_SPEED #makes player_speed negative on the x axis
        if keys[pg.K_RIGHT] or keys[pg.K_d]: #checks if right arrow or "d" key is pressed
            # self.vel.x = PLAYER_SPEED #makes player_speed positive on x_axis
            self.acc.x = PLAYER_SPEED #makes player_speed positive on x_axis
            #self.vx = PLAYER_SPEED #makes player_speed positive on x_axis
        if keys[pg.K_UP] or keys[pg.K_w]: #checks if up arrow or "w" key is pressed
            # self.vel.y = -PLAYER_SPEED #makes player_speed negative on y_axis since top left is (0,0)
            self.acc.y = -PLAYER_SPEED #makes player_speed negative on y_axis since top left is (0,0)
            #self.vy = -PLAYER_SPEED #makes player_speed negative on y_axis since top left is (0,0)
        if keys[pg.K_DOWN] or keys[pg.K_s]: #checks if down arrow or "s" key is pressed
            # self.vel.y = PLAYER_SPEED #makes player_speed positive on y_axis
            self.acc.y = PLAYER_SPEED #makes player_speed positive on y_axis
            #self.vy = PLAYER_SPEED #makes player_speed positive on y_axis

        # if self.vel.x != 0 and self.vel.y != 0:
        #     self.vel *= 0.7071

    def jump(self):
        pass

    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if self.dir == "none":
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.dir == "right":
            pass

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), # taling the frames starting at the top left
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE), # after 1 tilesize which is the length of the frame
                            ]
        self.run_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
                           self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)]
        
    def update(self):
        self.acc = vec(0, 0) # stop accelerating unless we start acccellerating as well as 9.8 gravity
        self.get_keys() # waits for input from gamer
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if hits:
            for i in range(1000):
                Particle(self.game, hits[0].pos.x, hits[0].pos.y)
            self.coins += 1
            self.game.pickup_snd.play()
            self.game.score += 1
        self.animate() # going and displaying the frames
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
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        # self.image.fill(RED)
        # pg.draw.circle(self.image, (YELLOW), (16, 16), 16)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # self.x = x*TILESIZE
        # self.y = y*TILESIZE
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.last_update = 0
        self.current_frame = 0
        # print("wall initialized")
        print(self.rect.x)
        print(self.rect.y)
    def load_images(self):
                self.idle_frames = [self.spritesheet.get_image(TILESIZE * 4,0,TILESIZE, TILESIZE),
                                    self.spritesheet.get_image(TILESIZE * 5,0,TILESIZE, TILESIZE)
                                    ]
    def animate(self):
            # use the time element to get now
            now = pg.time.get_ticks()
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        self.animate()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
 
class Mob(Sprite):
    def __init__(self, game, x, y): #method that initializes Sprite, only runs once
        self.groups = game.all_sprites, game.all_mobs #gets all of the sprite images
        Sprite.__init__(self, self.groups) #initializes Sprite
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png")) # finds the spritesheet
        self.image = self.spritesheet.get_image(0,0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK) # the background black
        self.load_images() # loading images
        self.image = pg.Surface((TILESIZE, TILESIZE)) #gets character pixel size from settings.py
        self.rect = self.image.get_rect() #draws rectangle for character
        self.speed = 1
        self.vx, self.vy = 500,0
        self.speed = 100
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.dir = "none"
        self.last_update = 0
        self.current_frame = 0
        self.hit_rect = MOB_HIT_RECT
        print("mob initialized")
        

    def load_images(self):
            self.idle_frames = [self.spritesheet.get_image(64,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(96,0,TILESIZE, TILESIZE)
                                ]
            self.run_frames = [self.spritesheet.get_image(64,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(96,0,TILESIZE, TILESIZE)
                                ]    
    def animate(self):
            now = pg.time.get_ticks()
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom    
            # uses autocomplete by creating a chase method using pos bectors and obj as a parameter
    # using autocomplete by creating a chase method using pos vectors and obj as a parameter.
    def chase(self, obj):
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0

        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0
            
    def update(self):
        self.animate()
        self.chase(self.game.player)
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

class Particle(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(randint(-180, 180), randint(-180, 180))
        self.pos = vec(x, y)
        self.speed = 5
        # Track spawn time in milliseconds using pygame ticks directly
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        # Check if 1000 milliseconds (which is ticks have) passed --> then it kills the particle
        if pg.time.get_ticks() - self.spawn_time > 1000:
            self.kill()

        self.pos += self.vel * self.speed * self.game.dt
        # Use center for vector-to-rect assignment to avoid float errors
        self.rect.center = self.pos

    
    # def load_images(self):
    #             self.idle_frames = [self.spritesheet.get_image(TILESIZE * 4,0,TILESIZE, TILESIZE)]
    
