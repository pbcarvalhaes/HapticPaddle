import sys, pygame, pyglet
import serial
import os

position = 100, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])


class Player():
	def __init__(self):
		pass

class Screen():
	def __init__(self, defaultX, defaultY):
		self.defaultSize = defaultX, defaultY
		self.backColor = 0,0,0
		
		self.screen = pygame.display.set_mode(defaultSize, pygame.RESIZABLE)
		
		self.subScreenSurface = self.screen.copy()
		self.rectSSS = self.subScreenSurface.get_rect()

		self.subScreenSurface.fill(self.backColor)
		
		self.scaledSSS = self.subScreenSurface
		self.scale = self.scaledSSS.get_size()
		
	
	def resize(self, size):
		size = tuple(map(int, size))
		self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
		self.scale = size
		self.scale = self.scale[0], self.scale[0]*self.defaultSize[1]//self.defaultSize[0]
		self.rectSSS = (0,(size[1]-self.scale[1])//2)
	
	def update(self):
		
		#self.subScreenSurface.fill(self.backColor)
		
		self.scaledSSS=pygame.transform.smoothscale(self.subScreenSurface, self.scale)
		self.screen.fill(white)
		self.screen.blit(self.scaledSSS, self.rectSSS)
		pygame.display.flip()


def interpolator(left_min, left_max, right_min, right_max):
	leftSpan = left_max - left_min
	rightSpan = right_max - right_min
	scaleFactor = float(rightSpan)/float(leftSpan)
	def interpol_funct(value):
		return right_min + (value-left_min)*scaleFactor
	return interpol_funct

pygame.init()


defaultSize = 2560, 1440
ballPos = 0

maxDisplay = pygame.display.Info()
displaySize = (maxDisplay.current_w, maxDisplay.current_h)

print(displaySize)

screen = Screen(defaultSize[0], defaultSize[1])

interpolate = interpolator(0,100,0, defaultSize[0])

green = 0, 225, 0

#ball = pygame.image.load("data/ball.png")
ball = pygame.Surface((200, 200))
ball = ball.convert_alpha()
ball.fill((0,0,0,0))
ballRect = ball.get_rect()
pygame.draw.circle(ball, green, ballRect.center, 100)

screen.resize((displaySize[0]//1.25, displaySize[1]//1.25))

gray = 25,25,25
white = 255,255,255

# ser = serial.Serial('COM3')
# print(ser.name)

speed = 0.05

#clocky = pygame.time.Clock()
#clocky.tick(60)

clockpy = pyglet.clock.Clock()
clockpy.set_fps_limit(60)

#line = ser.readline()
#ballPos = int(line.strip())
#ballPos = screen.get_size()[0]//2
ballPos = 50
maxSpeed = 0

print("hello")
while 1:
	#time = clocky.tick(30)
	time = clockpy.tick()
	time *= 500
	#screenSize = screen.get_size()
	#line = ser.readline()
	#ballPos = int(line.strip())
	#angle = batPos
	ballRect.x = (interpolate(ballPos)) - ball.get_size()[0]//2
	ballRect.y = 280
	screen.subScreenSurface.fill(gray)
	##subScreenSurface.blit(back, (0,0))
	screen.subScreenSurface.blit(ball, ballRect)
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			#ser.close()
			sys.exit(0)
		elif (event.type==pygame.VIDEORESIZE):
			screen.resize(event.dict['size'])
		elif (event.type==pygame.KEYDOWN):
			if(event.dict['key']==pygame.K_RIGHT):
				ballPos+= 2*time*speed
			elif(event.dict['key']==pygame.K_LEFT):
				ballPos-= 2*time*speed
	if(pygame.key.get_pressed()[pygame.K_RIGHT]):
		ballPos += time*speed
	if(pygame.key.get_pressed()[pygame.K_LEFT]):
		ballPos -= time*speed
	screen.update()


