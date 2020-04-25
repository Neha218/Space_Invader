import pygame
import math
import random
import time
from pygame import mixer  # class that helps us to handle all kind of musics

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("Background.png")

# background sound
mixer.music.load('Background.wav')
mixer.music.play(-1)  # -1 is to play music in loop

# game window title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('Player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
enemyImg = pygame.image.load('Enemy.png')

for i in range(no_of_enemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(6)
    enemyY_change.append(40)

# bullet
# ready -> You can't see the bullet on the screen
# fire -> The bullet is currently moving
bulletImg = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# score text
score_value = 0
'''
freesansbold is the free font provided by pygame
if we want any other font, then we can download it from site dafont.com
after downloading it will give a zip file, which we need to extract and put in the project folder itself
'''
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    # going to render text onto the screen
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
# RGB


while running:
    screen.fill((0, 0, 0))
    # adding background image to the window
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -8
                print("left key is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
                print("right key is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('Laser.wav')
                    bullet_sound.play()
                    # get the current x-coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("A keystroke is released")

    # checking boundaries of the spaceship so that doesn't go out of the window
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Width is 800 and player image is of 64px i.e. 64x64. So 800-64=736
        playerX = 736

    # Enemy movement
    for i in range(no_of_enemies):
        if enemyY[i] > 440 and enemyX[i] > playerX - 20 and enemyX[i] < playerX + 20:
            mixer.music.load('Background.wav')
            mixer.music.stop()
            for j in range(no_of_enemies):
                enemyY[j] += 20
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # Width is 800 and enemy image is of 64px i.e. 64x64. So 800-64=736
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision and bullet_state == "fire":
            explosion_sound = mixer.Sound('Explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
