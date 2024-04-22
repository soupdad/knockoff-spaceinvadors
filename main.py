import pygame
import random
from pygame import mixer

#initatize pygame
pygame.init()

#creates screen ((width,height))
#when viewing screen top,left corner is 0,0
		#and the bottom,right is 800,600
screen = pygame.display.set_mode((800, 600))

#Background Img
background = pygame.image.load("space.jpg")

#Background Sound
#mixer.music supports wav and mp3
#mixer.Sound only supports wav
mixer.music.load('background.wav')
#adding (-1) makes it loop
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invadors")

#my window doesnt have space for icon so idunno
#icon = pygame.image.load("ufo.png")
#pygame.display.set_icon(icon)

#Player
player_img = pygame.image.load("ship.png")
#where img will be placed
#has to take img into account thats why its not 400 perfectly
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemy_img.append(pygame.image.load("alien.png"))
	enemyX.append(random.randint(0,736))
	enemyY.append(random.randint(20,100))
	enemyX_change.append(10)
	enemyY_change.append(10)

#Bullet
#ready - cant see bullet on screen
#fire - the bullet is currently moving
bullet_img = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 25)

textX = 50
textY = 30

#Game Over
over = pygame.font.Font("freesansbold.ttf", 70)


def print_points(x,y):
	#render("text wanted", bool for disp on screen, color of font)
	score = font.render("Score: " + str(score_value), True, (255,255,255))
	screen.blit(score, (x,y))

def player(x,y):
	#.blit(img,(cordinates)) means to draw
	screen.blit(player_img, (x,y))

def enemy(x,y,i):
	#.blit(img,(cordinates)) means to draw
	screen.blit(enemy_img[i], (x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemyX,enemyY,bulletX,bulletY):
	di = (((enemyX-bulletX)**2) + ((enemyY-bulletY)**2))**0.5
	return (di < 27)

def game_over():
	over_text = over.render("GAME OVER", True, (255,255,255))
	screen.blit(over_text, (200,250))



#Game Loop
running = True
while running:

	#change bg color
	screen.fill((15,0,20))

	#bg img
	screen.blit(background, (0,0))

	#loops through all events to see if there's a match
	#all events are stores in pygame.event.get()
	for event in pygame.event.get():
		#if close button it pressed makes game stop running
		if event.type == pygame.QUIT:
			running = False

		#moving ship with arrow keys
		#if keystroke check whether right or left
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -1
			if event.key == pygame.K_RIGHT:
				playerX_change = 1
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					bullet_sound = mixer.Sound("laser.wav")
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX,bulletY)
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0


	#bullet movement
	if bullet_state == "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change

	playerX += playerX_change

	#adding boundaries for ship
	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736

	#enemy movement
	for i in range(num_of_enemies):

		#Game Over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over()
			break

		enemyX[i] += enemyX_change[i]
	#boundaries for enemy
		if enemyX[i] <= 0:
			enemyX_change[i] = 0.1
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -0.1
			enemyY[i] += enemyY_change[i]

		#collision
		collision = is_collision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosion_sound = mixer.Sound("explosion.wav")
			explosion_sound.play()
			bulletY = 480
			bullet_state = "ready"
			#MAKE SO SCORE APPEARS ON SCREEN
			score_value += 1
			enemyX[i] = random.randint(0,736)
			enemyY[i] = random.randint(20,100)

		enemy(enemyX[i],enemyY[i],i)

	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"
	
	player(playerX,playerY)
	print_points(textX,textY)
	#need this at end to update screen with stuff
	pygame.display.update()
