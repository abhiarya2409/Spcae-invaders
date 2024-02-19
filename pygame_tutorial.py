import pygame
import random
import math
from pygame import mixer

#intializing pygame
pygame.init()

#Create the screen
screen=pygame.display.set_mode((800,600))

#Background
background=pygame.image.load('background.jpg')

#Background Sound:
mixer.music.load('background.mp3')
mixer.music.play(-1)            # I have used -1 so that music continues playing

 
#Title and icon
pygame.display.set_caption("Space Invadors")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player description
playerImg=pygame.image.load('player.png')
playerX=370                      # X position of player
playerY=480                      # Y position of player
playerX_change=0

#Enemy description(multiple enemies)
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)


#Bullet description
#ready : you cant see the bullet on the screen
#fire: bullet is currently moving
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=1
bullet_state="ready"

#Score:
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

#Game over text:
over_font=pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score= font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
    
def game_over_text():
    over_text= over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))
    


def player(x,y):
    screen.blit(playerImg, (x, y))
    
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg, (x+16, y+10))
    

def is_collision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
    
# ... (Previous code)

# Game loop
running = True
game_over = False

while running:
    # RGB= RED, GREEN, BLUE 
    screen.fill((255, 15, 155))
    # Background Image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Keystroke is pressed, check whether it is pressed left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
                
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
                
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
                
            if event.key == pygame.K_r and game_over:
                # Reset game variables and restart game
                game_over = False
                score_value = 0
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)
                playerX = 370
                playerY = 480
                playerX_change = 0
                bullet_state = "ready"
                bulletY = 480
                mixer.music.play(-1)
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
    # Checking for boundaries for the spaceship, so it doesn't go out   
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    # Enemy movement and collision
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyX[j] = 2000
            game_over_text()
            game_over = True
            break
            
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
            
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            
        enemy(enemyX[i], enemyY[i], i)
    
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
            
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

    # Check if game is over and provide restart option
    if game_over:
        # Print message to restart the game
        font = pygame.font.Font('freesansbold.ttf', 32)
        restart_text = font.render("Press 'R' to play again", True, (255, 255, 255))
        screen.blit(restart_text, (250, 300))

    pygame.display.update()

