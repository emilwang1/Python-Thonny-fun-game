"""
Pygame Example
Game where the user moves a sea otter with the mouse to avoid abalone.
ICS3U
Courtney Edwards
History:
February 25, 2023: Program Creation
February 7, 2024: Updated to end when the player lasts 10 seconds or hits an abalone

Program based heavily on the realpython tutorial: https://realpython.com/pygame-a-primer
This is created to show the tutorial all in one place, with some variations (e.g. background image, timer, win/lose screens)
Accessed: Feb 2023
"""

# ============== Useful notes about Pygame ==============
"""
A number of classes are included in pygame
Surface --> defines a rectangular area on which you can draw.
Rect class --> Surface objects will have Rect, same as images and windows.
            Generally you blit an object's surface at the position of it's rectangle
display --> everything is drawn on the user-created display. Either a window or a full screen.
            Created using .set_mode() --> this will return a Surface and that's the visible part of your window.
            When you then draw an object or display objects, it's this display screen that it is referring to (e.g. pygame.display.update())
image module --> load & save images. They are loaded into Surface objects
"""

# ============== Image Sources ==============
"""
otter image source: https://www.pngitem.com/so/otter/
abalone image source: https://www.freepik.com/premium-photo/raw-fresh-abalone-white-background_37554842.htm
background source: https://www.flickr.com/photos/pareeerica/6131901917
"""

# ======================== IMPORTS & SETUP ========================
import sys
import time  # just for the end win/lose screen
import random

# allows access to the pygame library
import pygame

# These allow you to just write QUIT instead of having to write pygame.QUIT. Not necessary, but handy as shortforms.
from pygame.locals import (
    K_SPACE,
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# Initialize pygame - this is required.
pygame.init()

# ================== CONSTANTS =============

#  Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ======================== FUNCTIONS ========================
def doNothing():
    pygame.display.update()
    
def createLaser(laser, mousePos):
    # fire laser on the Player's rectangle based on the mouse position
    laser.image = pygame.image.load("laser.png").convert() # load the image, which returns a surface. Convert makes it faster to blit
    laser.image.set_colorkey((255,255,255), RLEACCEL) # This can be used to make a specific colour on your image transparent (white, here).

    # Place the abalone randomly on the screen, starting between 20-100 pixels beyond the right hand side of the screen
    laser.rect = laser.image.get_rect(
        center = (mousePos[0], mousePos[1]-320)
    )

def createGem(gem):
    """
    Adds an image, rectangle, and speed to a gem object
    gem.image (Surface): abalone image
    gem.rect (Rectangle): initial position is randomly placed just to the right of the screen
    gem.speed (int): Random integer between 5 and 20
    
    Args:
        gem (Sprite)
    Note that nothing is returned. The gem is mutable and passed by reference
    When we change the surface / rectangle of the gem in the function, it changes that object's attributes in the global scope
    """
    gem.image = pygame.image.load("gem3.png").convert() # load the image, which returns a surface. Convert makes it faster to blit
    gem.image.set_colorkey((255,255,255), RLEACCEL) # This can be used to make a specific colour on your image transparent (white, here).

    # Place the abalone randomly on the screen, starting between 20-100 pixels beyond the right hand side of the screen
    gem.rect = gem.image.get_rect(
        center=(
          random.randint(0, SCREEN_WIDTH),  # Must be at least 50 pixels away from top left where player spawns. This could be further optimized but works for demo
          0,
        )
    )
    # Select a random speed
    gem.speed = random.randint(5, 20)
    
def gemUpdate(gem):
    """
    Updates the position of the abalone sprite, destorying it if it off screen
    Args:
    food
    """
    # position is shifted in x-direction only, based on the sprite's speed
    gem.rect.move_ip(0, gem.speed)

    # if off screen, kill/destroy the object
    if gem.rect.bottom < 0: 
        gem.kill()

def createPlayer(player):
    """
    Initializes Player surface and rectangle.
    player.image (Surface): otter image
    player.rect (Rectangle): rectangle placed at bottom centre of screen

    Args:
        player (Sprite)

    Note that nothing is returned. The player is mutable and passed by reference
    When we change the surface / rectangle of the player in the function, it changes that object's attributes in the global scope
    """
    # load the image, which returns a surface. Convert makes it faster to blit
    player.image = pygame.image.load("Malcolm_cropped.png").convert()
    #Make a specific colour on the image transparent (white, here).
    player.image.set_colorkey((255, 255, 255), RLEACCEL)
    # the rectangle is used for the location of an object (where to place it), but also for collisions, etc..
    # this creates with the size of the surf. Without parameters, the rect is located wherever the surf was created
    player.rect = player.image.get_rect()

    # Move player to bottom centre of the screen
    # Constants are in the global scope. Note that changing the name of these constants would cause an issue.
    player.rect.x = SCREEN_WIDTH / 2
    player.rect.bottom = SCREEN_HEIGHT


def playerUpdate(player, pressed_keys):
    """
    Move the Player sprites based on mouse position
    Args:
    player (Sprite)
    mousePos (tuple(float)): Mouse position
    """

    # Move the Player's rectangle based on the mouse position
    if pressed_keys[K_UP]: # checks if the value for the K_UP key is True in the dictionary (i.e. the user pressed the up key)
        player.rect.move_ip(0, -7.5) # move_ip = move in place (x, y)
    if pressed_keys[K_DOWN]: # notice if not elif, so more than one can be pressed
        player.rect.move_ip(0,7.5)
    if pressed_keys[K_LEFT]:
        player.rect.move_ip(-7.5,0)
    if pressed_keys[K_RIGHT]:
        player.rect.move_ip(7.5,0)


    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    if player.rect.top <= 0:
        player.rect.top = 0
    elif player.rect.bottom >= SCREEN_HEIGHT:
        player.rect.bottom = SCREEN_HEIGHT

    #  Keep player on the screen
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    if player.rect.top <= 0:
        player.rect.top = 0
    elif player.rect.bottom >= SCREEN_HEIGHT:
        player.rect.bottom = SCREEN_HEIGHT


def createFood(food):
    """
    Adds an image, rectangle, and speed to a food object
    food.image (Surface): abalone image
    food.rect (Rectangle): initial position is randomly placed just above the screen
    food.speed (int): Random integer between 5 and 20

    Args:
        food (Sprite)
    Note that nothing is returned. The food is mutable and passed by reference
    When we change the surface / rectangle of the food in the function, it changes that object's attributes in the global scope
    """
    food.image = pygame.image.load("abalone.png").convert(
    )  # load the image, which returns a surface. Convert makes it faster to blit
    food.image.set_colorkey(
        (255, 255, 255), RLEACCEL
    )  # This can be used to make a specific colour on your image transparent (white, here).

    # Place the abalone randomly on the screen, starting between 20-100 pixels beyond the right hand side of the screen
    food.rect = food.image.get_rect(center=(
        random.randint(player.rect.left - 150, player.rect.right + 150),
        random.randint(-50, 0),
    ))
    # Select a random speed
    food.speed = 3
def createDaggar(daggar):
    """
    Adds an image, rectangle, and speed to a food object
    food.image (Surface): abalone image
    food.rect (Rectangle): initial position is randomly placed just above the screen
    food.speed (int): Random integer between 5 and 20

    Args:
        food (Sprite)
    Note that nothing is returned. The food is mutable and passed by reference
    When we change the surface / rectangle of the food in the function, it changes that object's attributes in the global scope
    """
    daggar.image = pygame.image.load("daggar.png").convert(
    )  # load the image, which returns a surface. Convert makes it faster to blit
    daggar.image.set_colorkey(
        (255, 255, 255), RLEACCEL
    )  # This can be used to make a specific colour on your image transparent (white, here).

    # Place the abalone randomly on the screen, starting between 20-100 pixels beyond the right hand side of the screen
    daggar.rect = food.image.get_rect(center=(
        random.randint(player.rect.left - 150, player.rect.right + 150),
        random.randint(-50, 0),
    ))
    # Select a random speed
    daggar.speed = 3
def daggarUpdate(daggar):
    daggar.rect.move_ip(0, daggar.speed)
    daggar.speed += daggar.speed * daggar.speed * 0.01
    # if off screen, kill/destroy the object
    if daggar.rect.top > SCREEN_HEIGHT:
        daggar.kill()
def foodUpdate(food):
    """
    Updates the position of the abalone sprite, destorying it if it off screen
    Args:
        food (Sprite)
    """
    # position is shifted in y-direction only, based on the sprite's speed
    food.rect.move_ip(0, food.speed)
    food.speed += food.speed * food.speed * 0.01
    # if off screen, kill/destroy the object
    if food.rect.top > SCREEN_HEIGHT:
        food.kill()
def nextlevel(screen):
    screen = pygame.display.set_mode(
    [SCREEN_WIDTH, SCREEN_HEIGHT]
)
    bg = pygame.image.load("cave5.png").convert()
    return bg
def nextlevel2(screen):
    bg = pygame.image.load("saharadesert.png").convert()
    return bg
def lastlevel(screen):
    bg = pygame.image.load("Epicbackground.png").convert()
    return bg
def end(status, screen):
    """
    Win screen shown at the end of the game
    Args:
        status (str)
        screen (Surface)
    """
    # Set screen as black with white text.
    screen.fill((0, 0, 0))
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Create text object, with associated rectangle in centre of screen
    text = font.render('YOU ' + status.upper(), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

    # blit needed for it to be placed on the surface, then display updated for it to show up.
    screen.blit(text, textRect)
    pygame.display.update()


# ======================== MAIN ========================

#  Set up the drawing window
screen = pygame.display.set_mode(
    [SCREEN_WIDTH, SCREEN_HEIGHT]
)  # Returns a Surface, which represents the inside dimensions of your drawing window --> the OS controls the borders & title bar, etc.

#  Create a custom event for adding a new food
ADDFOOD = pygame.USEREVENT + 1  # USEREVENT is the last kind of event that pygame reserves, so by adding 1 to this number, ADDFOOD becomes a new event with its own individual #
pygame.time.set_timer(ADDFOOD, 1000)  # this makes the ADDFOOD event happen every 1000ms (1/s). We call this once, but it fires throughout the game.
# Timer
ADDTIME = pygame.USEREVENT + 2  # Needs to be one bigger than ADDFOOD
pygame.time.set_timer(
    ADDTIME, 1000
)  # this makes the timer event happen once per second. We call this once, but it fires throughout the game.
timer = 0
ADDGEM = pygame.USEREVENT + 3 # USEREVENT is the last kind of event that pygame reserves, so by adding 1 to this number, ADDFOOD becomes a new event with its own individual 
pygame.time.set_timer(ADDGEM, 1000) # this makes the ADDFOOD event happen every 250ms (4/s). We call this once, but it fires throughout the game.
ADDDAGGAR = pygame.USEREVENT + 4
gems = 0
# ====PLAYER SPRITE
# Create a player sprite. This allows adding a surface, rectangle, etc.. durectly to the player so all the data is kept with that sprite. It also allows adding the player to a sprite group, which will come in handy later
player = pygame.sprite.Sprite()
# Add a surface (image) and rectangle (what is moved and where the image is drawn) to the player using the function we defined above
createPlayer(player)

# =====SPRITE GROUPS
#  Create groups to hold food sprites and all sprites
#  - foodGrp is used for collision detection and position updates
#  - all_sprites is used for rendering
daggarGrp = pygame.sprite.Group()
gemGrp = pygame.sprite.Group()
foodGrp = pygame.sprite.Group()
laserGrp = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#  Adjust the timing so the framerate isn't so high (adjusted in the game loop)
clock = pygame.time.Clock()

status = ''  # Used to determine whether the user quit (default setting), lost, or won

#  Run until the user asks to quit or game ends
running = True
changelevel = True
changelevel2 = True
changelastlevel = True
clock = pygame.time.Clock()
last_shoot_time = 0  # Get the last shoot time
laserReady = False
while running:
    shoot_time = pygame.time.get_ticks()
    if shoot_time - last_shoot_time >= 3000:
        if laserReady == False and gems >= 3:
          laserReady = True
          player.image = pygame.image.load("MalcolmReady.png").convert()
          player.image.set_colorkey((255,255,255), RLEACCEL)

    #  Did the user click the window close button?
    for event in pygame.event.get(
    ):  # every user input --> an event. This gets each of the events in a list.
        if event.type == KEYDOWN:
            # Check if the user clicked the escape key
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                if laserReady == True:
                  new_laser = pygame.sprite.Sprite()  
                  createLaser(new_laser, [(player.rect.left + player.rect.right) / 2, player.rect.top])
                  laserGrp.add(new_laser)
                  all_sprites.add(new_laser)
                  last_shoot_time = pygame.time.get_ticks()
                  gems -= 3
                  laserReady = False
                  player.image = pygame.image.load("Malcolm_cropped.png").convert()
                  player.image.set_colorkey((255,255,255), RLEACCEL)
                else:
                    doNothing()
        if event.type == ADDTIME:
            timer += 1
        #  Add a new food?
        if event.type == ADDFOOD:
            #  Create the new food
            new_food = pygame.sprite.Sprite()
            # Call createFood to add image, rectangle, and speed
            createFood(new_food)
            # Add new food to the food group and to the all sprites group
            foodGrp.add(new_food)
            all_sprites.add(new_food)
        if event.type == ADDGEM:
            #  Create the new food
            new_gem = pygame.sprite.Sprite()
            # Call createFood to add image, rectangle, and speed
            createGem(new_gem)
            # Add new food to the food group and to the all sprites group
            gemGrp.add(new_gem)
            all_sprites.add(new_gem)
        if event.type == ADDDAGGAR:
            #  Create the new food
            new_daggar = pygame.sprite.Sprite()
            # Call createFood to add image, rectangle, and speed
            createDaggar(new_daggar)
            # Add new food to the food group and to the all sprites group
            daggarGrp.add(new_daggar)
            all_sprites.add(new_daggar)
    # update player position based on key presses
    pressed_keys = pygame.key.get_pressed()
    playerUpdate(player, pressed_keys)
    for gem in gemGrp:
        gemUpdate(gem)
            
        #  Check if any of the foodGrp have collided with the player
    col = pygame.sprite.spritecollideany(player, gemGrp)
    if col is not None:
        col.kill() # kill the food it ate
        gems += 1
    # Update position of each food object
    for food in foodGrp:
        foodUpdate(food)
    for daggar in daggarGrp:
        daggarUpdate(daggar)
    #  Check if any of the foodGrp have collided with the player
    col = pygame.sprite.spritecollideany(player, foodGrp)
    if col is not None:
        col.kill()  # kill the food it ate
        running = False
        status = 'lose'
    col = pygame.sprite.spritecollideany(player, daggarGrp)
    if col is not None:
        col.kill()  # kill the food it ate
        running = False
        status = 'lose'
    if timer >= 30 and changelastlevel == True:
        bg = lastlevel(screen)
        changelastlevel = False
        pygame.time.set_timer(ADDFOOD, 500)
        pygame.time.set_timer(ADDDAGGAR, 500)
        pygame.time.set_timer(ADDGEM, 10000000)
    if 30 > timer >= 20 and changelevel2 == True:
        pygame.time.set_timer(ADDFOOD, 250)
        bg = nextlevel2(screen)
        changelevel2 = False
    if 20 > timer >= 10 and changelevel == True:
        pygame.time.set_timer(ADDFOOD, 500)
        bg = nextlevel(screen)
        changelevel = False
    if timer < 10:
        bg = pygame.image.load("background.jpg")
    #  Draw the background
    # screen.fill((0,0,0)) # solid colour option
    screen.blit(bg, (0, 0))  # bg image displayed with top left corner at 0,0
    # Draw all sprites
    # draw is a built in method. We pass the display screen, and it will draw the sprites within the group
    # In order to draw the sprites, they must have an image attribute (.image -- this is a Surface) and a rect attribute (.rect)
    all_sprites.draw(screen)
    laserSprites = laserGrp.sprites()
    if len(laserSprites) > 0:
        laserSprite = laserSprites[0]
        collaser = pygame.sprite.spritecollideany(laserSprite, foodGrp)
        if collaser != None:
          gems += 1
          collaser.kill() # kill the food it ate
        if shoot_time - last_shoot_time >= 300:  
          laserSprite.kill() # kill the laser
          
    # if survive for 30 seconds you win
    if timer == 60:
      running = False
      status = 'win'
      
    # Display the time level
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render('Time: ' + str(timer), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, 50
    screen.blit(text, textRect)
    
    # Display the time level
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render('Gems: ' + str(gems), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, 80
    screen.blit(text, textRect)

    #  Update the display
    pygame.display.update()

    #  Set framerate to 30 frames per second
    clock.tick(30)

# At end of game, display a win or lose screen
if status in ['win', 'lose']:
    end(status, screen)
    # User won't be able to close the game here.
    # This is annoying for the user, but done here just to show drawing a screen outside of the loop
    time.sleep(3)
# Quit
pygame.quit()