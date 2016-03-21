from __future__ import division
import math
import sys
import pygame
import random
import time

# fix the showing up of clicked function

class Piece(object):
    def __init__(self, position, image):
        self.image = image
        self.position = list(position[:])
        self.time_image = 20
        self.font = pygame.font.Font(None, 100)

    def draw_image(self,screen):
        rect = self.image.get_rect()
        rect = rect.move(self.position[0] - rect.width//2, self.position[1]-rect.height//2)
        screen.blit(self.image,rect)

class Orange(Piece):
    def __init__(self,position):
        super(Orange,self).__init__(position, \
            pygame.transform.scale((pygame.image.load('orange.png')), (200,200)))

class Purple(Piece):
    def __init__(self,position):
        super(Purple,self).__init__(position, \
            pygame.transform.scale((pygame.image.load('purple.png')), (200,200)))

class Green(Piece):
    def __init__(self,position):
        super(Green,self).__init__(position, \
            pygame.transform.scale((pygame.image.load('Green.png')), (200,200)))

class Yellow(Piece):
     def __init__(self,position):
        super(Yellow,self).__init__(position, \
            pygame.transform.scale((pygame.image.load('yellow.png')), (200,200)))


class Game(object):
    # Different states of playing
    STARTING, PLAYING, GAME_OVER = range(3)
    
    def __init__(self):
        """Initialize a new game"""
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)	
        pygame.init()
		
		# set up the screen/window
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

		# use a black background (Red, Green, Blue) - between 0 - 255
        self.bg_color = 0,0,0
        
        self.font = pygame.font.Font(None, 50)
        self.beep = pygame.mixer.Sound('beep.wav')
        self.clap = pygame.mixer.Sound('clap.wav')
        self.cheer = pygame.mixer.Sound('cheer.wav')
        self.cry = pygame.mixer.Sound('cry.wav')
        self.soundtrack = pygame.mixer.Sound('treasure.wav')
        self.soundtrack.set_volume(.0001)

        # load colours
        self.orange = Orange((250, 150))
        self.purple = Purple((500, 150))
        self.green= Green((250, 450))
        self.yellow = Yellow((500, 450))
        self.colours = []
        
        self.state = Game.STARTING
        self.add = 4

        self.lives = 3
        self.score = 0
        
        self.correct = 0
        self.check = 3
        self.incorrect = 0
        self.time = 60
        self.i = 0

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 30		# how many times the frame resets per seconds 
        self.REFRESH = pygame.USEREVENT+1
		# the timer refreshes the page by itself - 
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        # Now just start waiting for events
        self.event_loop()
    
    def shuffle (self):
        self.c = list((self.orange, self.purple, self.green, self.yellow))
        for i in range(0, self.add):
            self.colours.append(random.choice(self.c))
        
        # at a score of 300 add another colour to the pattern displayed 
        if self.score % 300 == 0:
            self.add += 1

    def show_colours(self):
        """Draws all the boxes on the screen"""
        self.orange.draw_image(self.screen)
        self.purple.draw_image(self.screen)
        self.green.draw_image(self.screen)
        self.yellow.draw_image(self.screen)

    def disappearing_draw_image(self, p):
        """Draws out which ever image is called upon, on the screen with its initial position and causes it to disappear"""
        if p.time_image > 0:
            rect = p.image.get_rect()
            rect = rect.move(p.position[0]-rect.width//2, p.position[1]-rect.height//2)
            self.screen.blit(p.image, rect)
            p.time_image -= 1
        elif p.time_image == 0:
            p.time_image = 30 
            self.i += 1
            
            if self.i >= self.add :
                self.i = self.add
        
        if p.time_image == 1:
            self.beep.play()
    
    def win(self):
        """Displays a correct sign when the player clicks on the correct box"""
        if self.time > 0:
            text = self.font.render('CORRECT!!!!', 1, (255,255,0))
            self.screen.blit(text, (300, self.height/2))
            self.time -= 1
        else:
            self.check = 3
            self.play_again()
        
        if self.time >= 30:
            self.cheer.play()

    def lose(self):
        """Displays a sorry sign when the player clicks on the incorrect box"""
        if self.time > 0:
            text = self.font.render("I'm sorry that was incorrect ):", 1, (255,0,0))
            self.screen.blit(text, (200,self.height/2))
            self.time -= 1
        else:
            self.check = 3
            self.play_again()
        
        if self.time >= 30:
            self.cry.play()


    def game_over(self):
        """ Displays the 'GAME OVER' screen"""
        if self.time > 0:
            text = self.font.render('GAME OVER !!!!!!!', 1, (255, 255, 255))
            self.screen.blit(text, (200, self.height/2))
            self.time -= 1
        else:
            self.keep_play()

    def display(self):
        """ Displays the score and lives on the screen""" 
        text = self.font.render('Score: %i' %self.score, 1, (0,245,255))
        self.screen.blit(text,(10,10))
        
        text2 = self.font.render('Lives: %i' %self.lives, 1, (0,245,255))
        self.screen.blit(text2, (650, 10))

    def starting_screen(self):
        """Displays the start screen"""
        text = self.font.render('Hit the SPACEBAR to Start', 1, (255,255,255))
        self.screen.blit(text,(200, self.height//2))

    def click(self, m, i):
        """If the player clicks on a box"""
        if self.correct >= 0:
            rect = self.colours[i].image.get_rect()
            rect = rect.move(self.colours[i].position[0] - rect.width//2, self.colours[i].position[1]-rect.height//2)
            if rect.collidepoint(m):
                self.correct += 1
            else:
                self.incorrect += 1
            
            if self.correct == 4:           # if you get all four correct
                self.check = 0 
                self.score += 100
            elif self.incorrect == 1 :      # if you get one wrong
                self.check = 1
                self.lives -= 1
            
            if self.lives == 0:
                self.state = Game.GAME_OVER

    def play_again(self):
        """Play after winning a round""" 
        self.colours = []
        self.time = 60
        self.i = 0
        self.correct = 0
        self.incorrect = 0
        self.state = Game.STARTING
        

    def event_loop(self):
        """Loop forever processing events"""
        running = True
        while running:
            event = pygame.event.wait()
            self.mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.state == Game.STARTING:
                """Hit the spacebar to start playing"""
                self.state = Game.PLAYING
                self.shuffle()
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == Game.PLAYING:
                """click on the boxes that appear"""
                self.clap.play()
                if self.lives > 0:
                    self.click(event.pos, self.i)
                    self.i += 1

            elif event.type == self.REFRESH:
                # time to draw a new frame
                self.draw()
                pygame.display.flip()


            else:
                pass #an event type we don't handle	
				
    def draw(self):
        """Update the display"""
        # everything we draw now is to a buffer that is not displayed
        self.screen.fill(self.bg_color)
        self.display()
                
        if self.state == Game.STARTING:
            self.starting_screen()

        elif self.state == Game.PLAYING:
            if self.i < self.add :
                self.disappearing_draw_image(self.colours[self.i])
            ### ERROR is here - if self.add == 4, the above function will still run even though it says < not <=     
            elif self.i >= self.add:    
                self.show_colours()
                
        elif self.state == Game.GAME_OVER:
            self.game_over()
            if self.time == 0:
                self.keep_play()

Game()
pygame.quit()
sys.exit()
