# import pygame module, mixer, and random 
import pygame
from pygame import mixer
import random
import time

# initialize pygame
pygame.init()

# set display, caption, and icon
clock = pygame.time.Clock()

win_x = 800
win_y = 600
screen = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Alien Beats")

# load the fonts
text1 = pygame.font.SysFont('menlo', 40)
text2 = pygame.font.SysFont('menlo', 80)
title = pygame.font.SysFont('menlo', 60)

# locations for ships and aliens
left_x = 160
down_x = 320
up_x = 480
right_x = 640

ship_y = 480

# create blast class
class Blast:
	def __init__(self, x, y, icon_location):
		self.locX = x
		self.locY = y
		self.icon = pygame.image.load(icon_location).convert_alpha()
	# getter and setter methods
	def getIcon(self):
		return self.icon
	def setIcon(self, icon_location):
		self.icon = pygame.image.load(icon_location).convert_alpha()
	def getX(self):
		return self.locX
	def setX(self, x):
		self.locX = x
	def getY(self):
		return self.locY
	def setY(self, y):
		self.locY = y
	# width and height of the blast object
	def getWidth(self):
		return self.icon.get_width()
	def getHeight(self):
		return self.icon.get_height()
	# method to make blast up
	def moveUp(self):
		if (self.locY >= 0):
			self.setY(self.locY - 14)
		else:
			blasts.remove(self)

# create alien class
alienspeed = 4

class Alien:
	def __init__(self, x, y, icon_location):
		self.locX = x
		self.locY = y
		self.icon = pygame.image.load(icon_location).convert_alpha()
	# getter and setter methods
	def getIcon(self):
		return self.icon
	def setIcon(self, icon_location):
		self.icon = pygame.image.load(icon_location).convert_alpha()
	def getX(self):
		return self.locX
	def setX(self, x):
		self.locX = x
	def getY(self):
		return self.locY
	def setY(self, y):
		self.locY = y
	# width and height of the alien object
	def getWidth(self):
		return self.icon.get_width()
	def getHeight(self):
		return self.icon.get_height()
	# method to make aliens go down
	def moveDown(self):
		if (self.locY <= ship_y):
			self.setY(self.locY + alienspeed)
		else:
			aliens.remove(self)
		
		
# create ship class
class Ship:
	def __init__(self, x, y, icon_location):
		self.locX = x
		self.locY = y
		self.icon = pygame.image.load(icon_location).convert_alpha()
	# getter and setter methods
	def getIcon(self):
		return self.icon
	def setIcon(self, icon_location):
		self.icon = pygame.image.load(icon_location).convert_alpha()
	def getX(self):
		return self.locX
	def setX(self, x):
		self.locX = x
	def getY(self):
		return self.locY
	def setY(self, y):
		self.locY = y
	# width and height of the ship object
	def getWidth(self):
		return self.icon.get_width()
	def getHeight(self):
		return self.icon.get_height()

# create list for blast objects
blasts = []

# draw blasts
def drawblasts():
	for b in blasts:
		screen.blit(b.getIcon(), (b.getX(), b.getY()))
		b.moveUp()

# create alien objects
whichalien = {1: left_x, 2: down_x, 3: up_x, 4: right_x}

aliens = []
def makeAlien(loc_x):
	if loc_x == left_x:
		icon_location = "images/alien_left.png"
	if loc_x == down_x:
		icon_location = "images/alien_down.png"
	if loc_x == up_x:
		icon_location = "images/alien_up.png"
	if loc_x == right_x:
		icon_location = "images/alien_right.png"
	aliens.append( Alien(loc_x, 0, icon_location))

# draw aliens
def drawaliens():
	for a in aliens:
		screen.blit(a.getIcon(), (a.getX(), a.getY()))
		a.moveDown()
		 
# create ship objects
ships = []
ships.append( Ship(left_x, ship_y, "images/ship_left.png" ))
ships.append( Ship(down_x, ship_y, "images/ship_down.png" ))
ships.append( Ship(up_x, ship_y, "images/ship_up.png" ))
ships.append( Ship(right_x, ship_y, "images/ship_right.png" ))

# draw ships
def drawships():
	for s in ships:
		screen.blit( s.getIcon(), (s.getX(), s.getY()))

# create lists for health
health = []
heart_locX = 4
heart_locY = 20
for i in range(5):
	health.append([heart_locX, heart_locY])
	heart_locY += 34
health_icon = pygame.image.load("images/health.png").convert_alpha()

# create stars list for moving background
stars = []
for i in range(80):
	stars.append([random.randint(1,win_x), random.randint(1,win_y)])

rand = random.randint(1,4)
x = whichalien[rand]
makeAlien(x)

def checkCollison():
	global scores
	for b in blasts:
		# to detect a collision, create the first Pygame rectangle based on the blast b width and height
		rect1 = pygame.Rect(  b.getX(), b.getY() + 30, b.getWidth(), b.getHeight()  )
		for a in aliens:
			# create the second Pygame rectangle based on the alien a width and height
			rect2 = pygame.Rect(  a.getX(), a.getY(), a.getWidth(), a.getHeight()  )
			if ( rect1.colliderect(rect2)  ):
				print("Collison")
				# and remove the enemy object from the aliens list
				aliens.remove(a)
				# update scores
				scores += 1
				try:
					blasts.remove(b)
				except:
					pass

i = 0
def checkHealth():
	global i
	for a in aliens:
		if a.getY() >= ship_y:
			health.remove(health[i])

# functions to handle the high scores

topfive = []

# add function to read and display high scores
def readandDisplayScores():
	global topfive
	infile = open('high_scores.txt', 'r')
	for i in range(5):
		topfive.append(infile.readline())
	
	infile.close()
	
	showScores = True
	while showScores:
		# background color
		screen.fill((0,0,0))

		# Quit event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			# Keystroke input read for player action
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					showScores = False
				if event.key == pygame.K_ESCAPE:
					print("Goodby...")
					pygame.quit()
					break

		# create and add text to display scores screen
		top_scores = text2.render("Top 5 scores:", True, (0,0,255))
		screen.blit(top_scores, (250,20))
		score1 = text1.render(topfive[0], True, (255,255,255))
		score2 = text1.render(topfive[1], True, (255,255,255))
		score3 = text1.render(topfive[2], True, (255,255,255))
		score4 = text1.render(topfive[3], True, (255,255,255))
		score5 = text1.render(topfive[4], True, (255,255,255))
		screen.blit(score1, (250, 100))
		screen.blit(score2, (250, 150))
		screen.blit(score3, (250, 200))
		screen.blit(score4, (250, 250))
		screen.blit(score5, (250, 300))

		previous = text1.render("Press enter to previous screen", True, (0,0,255))
		screen.blit(previous, (250, 400))
	
		pygame.display.update()

			
# this function is to show the Game Over screen
def gameOver():
	showGameOver = True
	while(showGameOver):
		#Background color
		screen.fill((0,0,0))

		#Quit Event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			# Keystroke input read for player action
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					showGameOver = False
				if event.key == pygame.K_ESCAPE:
					print("Goodby...")
					pygame.quit()
					break
				if event.key == pygame.K_q:
					readandDisplayScores()

		# create and add text to the Gameover Screen
		gameover = text2.render("GAME OVER!", True, (255,0,0))
		screen.blit(gameover, (250,100))

		start_over = text2.render("Press ENTER to Start Over!", True, (255,255,255))
		screen.blit(start_over, (20,350))

		prompt2 = text1.render("Press Q to show high scores", True, (255,255,255))
		screen.blit(prompt2, (260,400))

		pygame.display.update()

def welcomeScreen():

	showWelcomeScreen = True
	while(showWelcomeScreen):

		#Background color
		screen.fill((0,0,0))

		#Quit Event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			# Keystroke input read for player action
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					showWelcomeScreen = False
				if event.key == pygame.K_ESCAPE:
					print("Goodby...")
					pygame.quit()
				if event.key == pygame.K_q:
					readandDisplayScores()


		# add text to the Welcome Screen
		rules1 = text1.render("How to play: Use arrow keys to blast the aliens.", True, (255,0,0))
		rules2 = text1.render("If aliens reach your ships 5 times it is game over.", True, (255,0,0))
		rules3 = text1.render("Every 100 points, the aliens come faster.", True, (255,0,0))
		screen.blit(rules1, (20,200))
		screen.blit(rules2, (20,240))
		screen.blit(rules3, (20,280))
		# title
		title_ = title.render('Alien Beats', True, (0,255,0))
		screen.blit(title_, (280,100))

		prompt = text1.render("Press Enter to Start", True, (255,255,255))
		screen.blit(prompt, (260,350))

		prompt2 = text1.render("Press Q to show high scores", True, (255,255,255))
		screen.blit(prompt2, (260,400))

		pygame.display.update()

# show welcome screen
welcomeScreen()

# main game loop
running = True
speed = 60
scores = 0
lastFire = speed
lastAlien = speed
while running:
	# speed of game
	clock.tick(speed)
	
	screen.fill((0,0,0))

	# moving background
	for v in stars:
		if v[0] > 0:
			v[0] -= 2
		else:
			v[0] = win_x
		pygame.draw.rect(screen, (255,255,255), (v[0],v[1], 1, 1))

	for h in health:
		screen.blit(health_icon, (h[0], h[1]))

	for a in aliens:
		if pygame.time.get_ticks() - lastAlien >= speed * 5:
			rand = random.randint(1,4)
			x = whichalien[rand]
			makeAlien(x)
			lastAlien = pygame.time.get_ticks()
	if len(aliens) == 0:
		rand = random.randint(1,4)
		x = whichalien[rand]
		makeAlien(x)
		lastAlien = pygame.time.get_ticks()
				
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		
		if event.type == pygame.KEYDOWN:
			if pygame.time.get_ticks() - lastFire >= speed * 2:
				if event.key == pygame.K_LEFT:
					blasts.append( Blast(left_x, ship_y, "images/blast_left.png"))
					lastFire = pygame.time.get_ticks()
				if event.key == pygame.K_DOWN:
					blasts.append( Blast(down_x, ship_y, "images/blast_down.png"))
					lastFire = pygame.time.get_ticks()
				if event.key == pygame.K_UP:
					blasts.append( Blast(up_x, ship_y, "images/blast_up.png"))
					lastFire = pygame.time.get_ticks()
				if event.key == pygame.K_RIGHT:
					blasts.append( Blast(right_x, ship_y, "images/blast_right.png"))
					lastFire = pygame.time.get_ticks()

	drawaliens()

	drawships()

	drawblasts()

	checkCollison()

	if len(health) > 0:
		checkHealth()
	else:
		aliens.clear()
		scores = 0
		alienspeed = 4
		gameOver()
		rand = random.randint(1,4)
		x = whichalien[rand]
		makeAlien(x)
		heart_locX = 4
		heart_locY = 20
		i = 0
		for j in range(5):
			health.append([heart_locX, heart_locY])
			heart_locY += 34
			health_icon = pygame.image.load("images/health.png").convert_alpha()

	scores_text = text1.render(f"Score: {scores}", True, (255,255,255))
	screen.blit(scores_text, ((win_x / 2), (win_y - 30)))
	if scores % 100 == 0:
		alienspeed += 0.5
		scores += 1

	pygame.display.update()

pygame.quit()
