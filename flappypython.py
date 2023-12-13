
# Collaborator notes: Although this was a solo project, I discussed my project and received help from LMU computer science tutor. 
    # I mainly needed help for the physics section and for the layout of the project.
# >>> NOTES FOR GRADER:


import pygame, math, random, time # Importing to use Randit, clock, sleep, misc. math functions  

pygame.init()

game_ui = pygame.display.set_mode((480, 700)) # Create game window 
score = 0 # Score starts at 0

visual_button = pygame.image.load('assets/startbutton.png') # Load button visual
visual_background = pygame.image.load('assets/background.png') # Load background visual
visual_ground = pygame.image.load('assets/ground.png') # Load ground visual

scroll_rate = 5.5 # How fast environment moves left

boosting = False # Boolean; is snake avatar currently boosting in air?

time_between_pipes = 650 # Time in MS between pipe sets 
pipes_width = 280 # Gap width for avatar to boost through
pipes_cleared = False # Has snake avatar succesfully passed through pipe? 
pipes_previous = pygame.time.get_ticks() - time_between_pipes # Time between present and when last pipe was generated 

font_color = pygame.Color('white') # Change text to white
font = pygame.font.SysFont('Pokemon GB.ttf', 50) # Font and text size

fps = 120 # frames per second, smoothness of game 
timer = pygame.time.Clock() # <<< controls frame rate 

endgame = False # Game over is initially set as false 

snake_set = pygame.sprite.Group() # Stores snake sprite
pipe_set = pygame.sprite.Group() # Stores pipe sprites 

# Reset avatar positioning and score after a death 
def restart():
    global score, boosting, endgame # global variables 
    score = 0 
    python.rect.y = 350 # reset y coordinate of snake
    python.rect.x = 100 # reset x coordinate of snake 
    boosting = False
    endgame = False
    pipe_set.empty()  # Clear existing pipes from previous run, we want a clean map 
    return score

# Draw text onto game UI
def score_number(text, font, text_col, x, y):
    game_ui.blit(font.render(text, True, text_col), (x, y)) # text rendering 


# Snake avatar class
class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # Intializes the parent class sprite 
        self.index = 0 # Index to track appearence 
        self.speed = 0
        self.visuals = [pygame.transform.scale(pygame.image.load("assets/p1.png"), (96, 64)) for _ in range(1, 10)] # list for snake image specifications 
        self.jetpack_image = pygame.transform.scale(pygame.image.load("assets/p2.png"), (116, 84)) # Load other snake image that has jetpack flames (p2.png)
        self.image = self.visuals[self.index] # Initial image for snake 
        self.rect = self.image.get_rect(center=(x, y)) # Set inital position for center of snake's rectangle 
        self.pressed = False # To track user input 
        self.using_jetpack = False # Check if jetpack is being used 

    def update(self):
        if boosting:
            if self.rect.bottom < 600: # Is snake below ceiling? 
                self.rect.y += self.speed # Snake moves vertically based on its speed 
                self.using_jetpack = pygame.mouse.get_pressed()[0] == 1 # Has mouse button been pressed to activate jetpack boost? 
            self.speed += 0.4 # Speed increase while boosting with jetpack 
        else:
            self.using_jetpack = False 

        if not endgame:
            if not self.pressed and pygame.mouse.get_pressed()[0] == 1: # Check for user input
                self.speed = -9 # speed decreases 
                self.pressed = True # User input being pressed set to true 
            if pygame.mouse.get_pressed()[0] == 0: # Has user input stopped? 
                self.pressed = False
        if self.using_jetpack:
            self.image = self.jetpack_image # *** SET SNAKE IMAGE TO JETPACK if using jetpack 
        else:
            aspect_ratio = self.visuals[self.index].get_width() / self.visuals[self.index].get_height() # determine aspect ratio between width and height 
            new_snake_height = int(118 / aspect_ratio) # Adjust height based on A:R 
            self.image = pygame.transform.scale(self.visuals[self.index], (96, new_snake_height)) # Scale image using new_snake_height 


# Start button class 
class Start_button():
    def __init__(self, x, y, image, width, height):
        self.image = pygame.transform.scale(image, (int(284.9), int(105))) # scale button 
        self.rect = self.image.get_rect() # create rect for button 
        self.rect.topleft = (x, y)

    def draw(self):
        mouse_placement = pygame.mouse.get_pos() # get positon of mouse to later check if it is inside button rect 
        pressed = False
        pressed = pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(mouse_placement)
        game_ui.blit(self.image, (self.rect.x, self.rect.y)) # Draw "start" button
        return pressed # Return if mouse was pressed
       
# "Start" button dimensions
button_width = 300  
button_height = 50
button = Start_button((480 - button_width) / 2, (700 - button_height) / 2, visual_button, button_width, button_height) 
# ^^^ dimensions and position start button 

# Pipe obstacle class
class Pipes(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__() # super to call parent class "Sprite"
        self.image = pygame.image.load("assets/pipe.png")
        self.rect = self.image.get_rect()
        self.passed = False # Has snake passed pipe set? 
        self.set_pipe(x, y, position) # setting intiial coordinates/position of pipe set

    def set_pipe(self, x, y, position):
        pipe_offset = int(pipes_width / 2) # vertical offset is half of pipe set gap 
        pipe_flip = position == 1 # variable in case pipes need to be flipped up/down 
        if pipe_flip:
            self.rect.topleft = [x, y + pipe_offset] # lower pipe >>> top left pos 
        else:
            self.image = pygame.transform.flip(self.image, False, True) 
            self.rect.bottomleft = [x, y - pipe_offset] # upper pipe >>> bottom left pos 

    def update(self):
        self.pipe_slide() # Update pipe coordinates/position 

    def pipe_slide(self):
        self.rect.x -= scroll_rate # lock pipe movement across screen to scroll rate variable 
        if self.rect.right < 0:
            self.pipe_delete() # once pipe set is out of screen, delete it

    def pipe_delete(self):
        self.kill() # Kill function to remove pipe sprite from pipe group once out of screen 


python = Snake(110, 300) # Starting coordinates for snake sprite 
snake_set.add(python) # Starting snake sprite (python) is added into sprite group 

game_on = True
while game_on:
    game_ui.blit(visual_background, (.5,.5)) # draw background

    snake_set.draw(game_ui) # draw snake
    snake_set.update() # update snake appearence and coordinates 
    pipe_set.draw(game_ui) # draw pipe sets 

    # If game is ongoing and snake is boosting, keep creating pipes!! 
    if not endgame and boosting:
        pipe_set_level = random.randint(-120, 90) # CRITICAL LINE: use randit to have random pipe levels for a new "map" each new game 
        time_now = pygame.time.get_ticks() # Get time in MS 
        if time_between_pipes < (time_now - pipes_previous):
            pipes_previous = time_now # update time to time_now 
            pipe_ceiling = Pipes(480, pipe_set_level + 350, 1) # Create upper pipe within bounds
            pipe_set.add(pipe_ceiling) # Add new upper pipe to set 
            pipe_floor = Pipes(480, pipe_set_level + 350, -1) # Create lower pipe within bounds 
            pipe_set.add(pipe_floor) # Add new lower pipe to set 
        pipe_set.update()

    hit_pipe = pygame.sprite.groupcollide(snake_set, pipe_set, False, False) # Groupcollide creates dictionary that checks if key sprite is colliding with key obstacles, initially set to false
    hit_ceiling = 0 > python.rect.top # Snake hits the ceiling if it goes into negative coordinates 
    hit_floor = 600 < python.rect.bottom # Snake hits floor if it goes further than 600 down 
    if hit_pipe or hit_ceiling or hit_floor: # End the game if the snake hits the pipe, ceiling, or floor rects 
        endgame = True 

    score_number(str(score), font, font_color, 240, 25) # Log player score 

    # Check if there are pipes in the pipe set 
    if 0 < len(pipe_set): 
        next_pipe = min(pipe_set, key=lambda pipe: pipe.rect.right) # defines the pipe closest to right side of snake's rect    
        if not next_pipe.passed and next_pipe.rect.right < snake_set.sprites()[0].rect.left: # update score after checking if snake has cleared next pipe set 
            next_pipe.passed = True
            pipes_cleared = False
            score += 1


    # Check game status 
    if endgame:
        restart_game = button.draw() # draw restart game button 
        if restart_game:
            score = restart() # reset score/restart game
            endgame = False # endgame flag to false if restarting game 
            
    if not boosting and not endgame:
        user_input = pygame.mouse.get_pressed()
        if user_input[0]: # check if user is inputting, if they are then boosting is true 
            boosting = True

    game_actions = pygame.event.get() # get list of game actions that have occurred using pygame 
    for game_action in game_actions:
        if game_action.type == pygame.QUIT: # quit pygame & application
            game_on = False # exit game loop but turning game off 

    timer.tick(fps)
    pygame.display.update()

pygame.quit()

# You've reached the end! Thanks for checking out Flappy Python :D 