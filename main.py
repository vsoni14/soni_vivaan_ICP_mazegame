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

    def draw_light_rays(self, t):
# Set the center point where all the light rays begin
        center = (WIDTH // 2, HEIGHT // 2 - 100)


        # Create 36 individual light rays
        for i in range(36):


            # Calculate the angle of each ray
            # The time value makes the rays rotate slowly
            angle = (i / 36) * math.pi * 2 + t * 0.12


            # Calculate the ending x position of each ray
            end_x = center[0] + math.cos(angle) * 400


            # Calculate the ending y position of each ray
            end_y = center[1] + math.sin(angle) * 300


            # Draw the ray from the center to its endpoint
            pg.draw.line(
                self.screen,
                (15, 30, 55),
                center,
                (int(end_x), int(end_y)),
                1
            )



    def draw_glowing_orb(self, t):

        # Set the position of the glowing orb
        center = (WIDTH // 2, HEIGHT // 2 - 100)

        # Calculate the pulsing size using the sine function
        pulse = int(5 * math.sin(t * 3))

        # Draw the largest outer glow circle
        pg.draw.circle(self.screen, (10, 25, 60), center, 90 + pulse)

        # Draw the middle glow circle
        pg.draw.circle(self.screen, (15, 50, 100), center, 65 + pulse)

        # Draw the smaller inner glow circle
        pg.draw.circle(self.screen, (25, 100, 180), center, 35 + pulse)

        # Draw the bright center of the glowing orb
        pg.draw.circle(self.screen, (120, 210, 255), center, 13)


    def draw_game_title(self):

        # Create the font for the main game title
        title_font = pg.font.SysFont("arial", 65, bold=True)

        # Create the font for the subtitle and instructions
        subtitle_font = pg.font.SysFont("arial", 18)

        # Render the main game title
        title = title_font.render(
            "SHADOW RUNNER",
            True,
            (225, 240, 255)
        )

        # Position the title at the top center of the screen
        self.screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, 90))
        )

        # Render the subtitle
        subtitle = subtitle_font.render(
            "FIND THE LIGHT. ESCAPE THE DARKNESS.",
            True,
            (110, 180, 220)
        )

        # Position the subtitle underneath the title
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(WIDTH // 2, 140))
        )

        # Render the instructions at the bottom of the screen
        footer = subtitle_font.render(
            "COLLECT LIGHT ORBS  |  REACH THE EXIT",
            True,
            (90, 105, 135)
        )

        # Position the instructions near the bottom
        self.screen.blit(
            footer,
            footer.get_rect(center=(WIDTH // 2, HEIGHT - 45))
        )



    def draw_background(self):

        # Fill the screen with a dark background
        self.screen.fill((5, 7, 18))

        # Store the positions of decorative stars
        stars = [
            (100, 100), (250, 180), (400, 80),
            (600, 150), (750, 90), (900, 200),
            (150, 350), (350, 450), (700, 400),
            (850, 500), (500, 300), (950, 100)
        ]

        # Draw each star as a small blue circle
        for x, y in stars:
            pg.draw.circle(
                self.screen,
                (100, 140, 190),
                (x, y),
                2
            )

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
            # Get the current time for the animated effects
            t = pg.time.get_ticks() / 1000

            # Draw the dark background and stars
            self.draw_background()

            # Draw the rotating light rays
            self.draw_light_rays(t)

            # Draw the pulsing glowing orb
            self.draw_glowing_orb(t)

            # Draw the game title and instructions
            self.draw_game_title()


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
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.jump()

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