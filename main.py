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

GOALS: Win the race 

RULES: Cannot go out of the track 

FEEDBACK: 

FREEDOM: Push opponents outside the racetrack to eliminate them. 
Pickup differnt powerups aiding your ability to stun or eliminate opponents
'''
 
import pygame as pg #importing as pg to make typing pygame easier
from os import path
from settings import * #imports everything from settings.py
from sprites import * #imports everything from sprites.py
from utils import *
import math

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

    def show_start_screen(self):

        # Create the PLAY button in the center of the screen
        button = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)

        # Keep displaying the start screen until the player starts the game
        while self.running:

            # Limit the screen refresh rate
            self.clock.tick(FPS)

            # Get the current position of the mouse
            mouse = pg.mouse.get_pos()

            # Check if the mouse is hovering over the PLAY button
            hovering = button.collidepoint(mouse)

            # Check for player input and window events
            for event in pg.event.get():

                # Close the game if the player clicks the X button
                if event.type == pg.QUIT:
                    self.running = False
                    return False

                # Check if the player clicks the left mouse button
                if event.type == pg.MOUSEBUTTONDOWN:

                    # Start the game if the PLAY button is clicked
                    if event.button == 1 and button.collidepoint(event.pos):
                        return True

            # Fill the screen with a black background
            self.screen.fill((0, 0, 0))

            # Create the font used for the PLAY button
            font = pg.font.SysFont("arial", 30, bold=True)

            # Change the button color when the mouse hovers over it
            if hovering:
                button_color = (70, 130, 200)
            else:
                button_color = (30, 80, 140)

            # Draw the PLAY button with rounded corners
            pg.draw.rect(
                self.screen,
                button_color,
                button,
                border_radius=10
            )

            # Create the PLAY text
            play_text = font.render("PLAY", True, (255, 255, 255))

            # Position the PLAY text in the center of the button
            self.screen.blit(
                play_text,
                play_text.get_rect(center=button.center)
            )

            # Update the display to show the button
            pg.display.flip()

        return False


    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "highscore.txt") # assigns the salve file to the fire "highscore.txt"

        self.img_dir = path.join(self.game_dir, 'images')
 
        # sound handling
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "coin.mp3")) # gets the file from the audio folder
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
        self.all_particles.update() # updates the particles and makes sure the particles are generated

    def draw(self):
        # this order matters: the first things are on the bottom are the first to be drawn
        self.screen.fill(BGCOLOR) #tells the code which color to fill the background
        self.all_sprites.draw(self.screen) #everything will be drawn on the screen
        self.all_particles.draw(self.screen)
        self.draw_text("Frames per second: " + str(floor(1/self.dt) ), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins:{self.player.coins}", 24, WHITE, WIDTH/2, HEIGHT/7)
        self.draw_text(f"High Score:{self.high_score}", 24, WHITE, WIDTH/2, HEIGHT/12)
        pg.display.flip()

if __name__ == "__main__": #checks if we are in main.py and if we are in main.py, it will initialize Game
    g = Game()

    if g.show_start_screen(): # 
        while g.running: #keeps the window open forever
            g.new()
            g.run()