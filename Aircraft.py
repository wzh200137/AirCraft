import time, sys, random, pygame, math, os
from PIL import Image,ImageDraw,ImageFont

t = time.gmtime()


#初始化界面
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Air Craft')
icon = pygame.image.load('ufo.png') #icon
pygame.display.set_icon(icon)
bgImg = pygame.image.load('bg.png')#背景图片
running = True

#添加音效
pygame.mixer.music.load('bg.wav')
pygame.mixer.music.play(-1)
boom_sound = pygame.mixer.Sound('exp.wav')
#Aircraft
playerImg = pygame.image.load('player.png')#Aircraft
playerX = 400 
playerY = 500
playerStep = 0

score = 0
font1 = pygame.font.Font('freesansbold.ttf', 32)
def show_score():
	text = f"Scores:{score}"
	score_render = font1.render(text, True, (255,255,255))
	screen.blit(score_render, (10,10))


is_over = False
font2 = pygame.font.Font('freesansbold.ttf',64)
def check_is_over():
	if is_over:
		text = "Game Over!"
		render = font2.render(text, True, (255,0,0))
		screen.blit(render,(200,250))
#添加敌人
number_of_enemies = 1

f = open("TOFEL words.txt","r")
text = f.read()
TOFEL_words = text.split()

image = Image.open('enemy2.png')
draw = ImageDraw.Draw(image)
font=ImageFont.truetype('font/msyh.ttc',10)
draw.text((10,30), TOFEL_words[random.randint(0,571)], (0,0,0),font)
image.save("enemy2_now" + ".png")


class Enemy():
	def __init__(self):
		self.img = pygame.image.load("enemy2_now.png")
		self.x = random.randint(200,600)
		self.y = 0
		self.step = random.randint(1, 2)
	def reset(self):
		self.img = pygame.image.load("enemy2_now.png")
		self.x = random.randint(200,600)
		self.y = 0

enemies = []
for i in range(number_of_enemies):
	enemies.append(Enemy())

def distance(bx, by, ex, ey):
	a = bx - ex
	b = by - ey
	return math.sqrt(a*a + b*b)


class Bullet():
	def __init__(self):
		self.img = pygame.image.load('bullet.png')
		self.x = playerX + 16
		self.y = playerY - 10
		self.step = 10
	
	def hit(self):
		global score
		for e in enemies:
			if (distance(self.x, self.y, e.x, e.y) < 30):
				boom_sound.play()
				bullets.remove(self)
				image = Image.open('enemy2.png')
				draw = ImageDraw.Draw(image)
				font=ImageFont.truetype('font/msyh.ttc',10)
				draw.text((10,30), TOFEL_words[random.randint(0,571)], (0,0,0),font)
				image.save("enemy2_now" + ".png")
				e.reset()#秒投胎
				score += 1

bullets = []

def show_bullets():
	for b in bullets:
		screen.blit(b.img,(b.x,b.y))
		b.hit()
		b.y -= b.step

		if b.y < 0:
			bullets.remove(b)


def show_enemy():
	global is_over
	for e in enemies:
		screen.blit(e.img, (e.x,e.y))
		e.y += e.step
		if e.y > 450:
			is_over = True
			enemies.clear()
		


def move_player():
	global playerX
	playerX += playerStep
	#防止飞机出界
	if playerX >736:
		playerX = 736
	if playerX < 0 :
		player = 0
#游戏主循环
while 1:
	screen.blit(bgImg,(0,0))
	show_score()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:sys.exit()
		
		#键盘按下
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				playerStep = 5
			elif event.key == pygame.K_LEFT:
				playerStep = -5
			elif event.key == pygame.K_SPACE:
				bullets.append(Bullet())

		if event.type == pygame.KEYUP:
			playerStep = 0

	screen.blit(playerImg, (playerX, playerY))
	move_player()
	show_enemy()
	show_bullets()		
	check_is_over()
	pygame.display.update()
			