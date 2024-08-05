import pygame
import math
import random

# intialize the game
pygame.init()

# to create new window for game
screen = pygame.display.set_mode((800,600))

# Background image
background = pygame.image.load("background.png")

# display game name
pygame.display.set_caption("Space Invaders")

# set icon
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 360
playerY = 480
playerX_change = 0                     # we dont take y direction cuz player cant move in x direction

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randrange(50,200))               # spawning different places
    enemyX_change.append(1.5)
    enemyY_change.append(25)                          # changing y direction after every hit on x direction

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480               # at player's position
bulletY_change = 7                      # we dont take x direction cuz bullet cant move in x direction
bullet_state = "ready" #ready = you can't see the bullet on the screen / fire = the bullet is currently moving

# Score

score_value = 0
font = pygame.font.Font(None,32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))     # blit means DRAW (it's drawing player image)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))     # blit means DRAW (it's drawing enemy image)

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))    # cuz bullet shooting from mid of the player img 

def isCollision(enemyX, enemyY, bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2))) #collision logic website:https://www.wikihow.com/Find-the-Distance-Between-Two-Points
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((0,0,150))    # fill screen with color (R,G,B)
    
    screen.blit(background,(0,0))   # background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke
        if event.type == pygame.KEYDOWN:      # it checks press any keystrokes from keyboard
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":      
                    bulletX = playerX             # we need to save starting position of firing bullet
                    fire_bullet(bulletX, bulletY)      # press space to fire bullet 

        if event.type == pygame.KEYUP:        # it checks release keystroks from keyboard
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement

    playerX += playerX_change   

    # creating boundaries

    if playerX <=0:
        playerX=0
    elif playerX >=736:      # (800 - 64) cuz player img having 64 x 64 pixel
        playerX=736

    # Enemy movement

    for i in range (num_of_enemies):
        enemyX[i] += enemyX_change[i]

        # creating boundaries

        if enemyX[i] <=0:
            enemyX_change[i]=1.5
            enemyY[i]+=enemyY_change[i]     # changing y direction after every hit on x direction  
        elif enemyX[i] >=736:         
            enemyX_change[i]=-1.5
            enemyY[i]+=enemyY_change[i]
        
        # Collision 
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randrange(50,200)
        
        enemy(enemyX[i],enemyY[i],i)         # calling enemy cuz we need show player everytime


    # Bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    

    player(playerX,playerY)      # calling player cuz we need show player everytime
    show_score(textX,textY)
    
    pygame.display.update()   # to upadte the display 