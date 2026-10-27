# This file was made by Vivaan Soni
'''
Why are we making game a class?
Why is it capitalized?
What is init?
What is pass?
 
Data types: boolean, JSON, strings
 
Input (events): Keyboard input, mouse click, voice,
power button, eye tracking, camera, gyroscoping, electrostatic, location, volume, microphone
 
Process: cursor position, position of player, score, enemy position, velocity, aim in FPS,
 
Output: graphics - things are drawn, sound - jump, power up, wakling, haptics

GOALS:

RULES:

FEEDBACK:

FREEDOM:
'''
 
import pygame as pg #importing as pg to make typing pygame easier
from os import path
from settings import * #imports everything from settings.py
from sprites import * #imports everything from sprites.py
from utils import *
 
class Game: #initializing class Game
    def __init__(self):
        pg.init() #initializing pygame
        pg.mixer.init() #initializing pygame sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #setting screen size to 800x600 from settings.py
        print("game initialized...")
        pg.display.set_caption(TITLE) #changing window name to TITLE from settings.py
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
        self.high_score = 0
        self.score = 0
        
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "highscore.txt")

        self.img_dir = path.join(self.game_dir, 'images')
        # sound handling
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "coin.mp3"))
        self.map = Map(path.join(self.game_dir, map))

        try:
            with open(self.game_save_file, 'x', encoding="utf-8") as file:
                file.write("hello world!")
            print("file created successfully!")

        except FileExistsError:
            print("File already exists")

        with open(self.game_save_file, 'r') as file:
            try:
                self.high_score = int(file.read())
            except:
                # self.high_score = 0
                print("high score not read...")
    def new(self):
        self.load_data('level1.txt')
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()
 
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
                if tile == "C":
                    Coin(self, col, row)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row)

        pg.mixer.music.load(path.join(self.snd_dir, "thetrip.flac"))
        pg.mixer.music.play(loops=-1)

    def run(self):
        self.playing = True
        while self.playing: #will always be True until user exits game where self.running will become False
            self.dt = self.clock.tick(FPS) / 1000
            self.events() #when user launches game, self.running will be True, so it will run the events method
            #self.update()
            self.update() #updates the movement of the white block
            self.draw() #draws the background color
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.score > self.high_score:
                    with open(path.join(self.game_dir, self.game_save_file), 'w') as f:
                        f.write(str(self.score))
                if self.playing:
                    self.playing = False
                self.running = False

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        self.all_sprites.update() #updates the position of the block based on vx and vy

    def draw(self):
        # this order matters: the first things are on the bottom are the first to be drawn
        self.screen.fill(BGCOLOR) #tells the code which color to fill the background
        self.all_sprites.draw(self.screen) #everything will be drawn on the screen
        self.draw_text("Frames per second: " + str(floor(1/self.dt) ), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Frames per second:{1/self.dt}", 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins:{self.player.coins}", 24, WHITE, WIDTH/2, HEIGHT/7)
        pg.display.flip()

if __name__ == "__main__": #checks if we are in main.py and if we are in main.py, it will initialize Game
    g = Game()
 
while g.running: #keeps the window open forever
    g.new()
    g.run()