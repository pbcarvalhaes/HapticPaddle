#import sys, pygame, pyglet
import serial
import math
import socket

#from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from multiprocessing import Process, Pipe, Value


TCP_IP = ''
BUF_SIZE = 30
#T_PORT = 65435

#Parallelize the server stuff
def f(T_PORT, player1, player2):

	print("I'm",socket.gethostbyname(socket.gethostname()))
	TCP_IP = socket.gethostname()
	#TCP_IP = '192.168.0.28'

	with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as k:
		print("Before")
		k.bind((TCP_IP, T_PORT))
		print("I got here")
		k.listen(2)
		con, addr = k.accept()
		print ('Connection Address is: ' , addr)
		with con:
			while True :
				try:
					data = con.recv(BUF_SIZE)
					if not data:
						print("Disconnected")
						break
					a = int.from_bytes(data, byteorder='big')
					#print("Recieving: ", a)
					player2.value = a
					#print("Sending: ", player1())
					con.send((player1.value).to_bytes(2, byteorder='big'))
				except ConnectionResetError:
					print("Disconnected")
					break
	print("Process finished")

#also need to paralellize the input

def interpolator(left_min, left_max, right_min, right_max):
	leftSpan = left_max - left_min
	rightSpan = right_max - right_min
	scaleFactor = float(rightSpan)/float(leftSpan)
	def interpol_funct(value):
		return right_min + (value-left_min)*scaleFactor
	return interpol_funct


if __name__ == "__main__":
	import sys, pygame, pyglet

	pygame.init()

	gray = 25,25,25
	white = 255,255,255


	defaultSize = 850,400
	screen = pygame.display.set_mode(defaultSize, pygame.RESIZABLE)
	pygame.display.set_caption("Servidor")

	green = 0, 225, 0
	ball = pygame.Surface((200, 200)).convert_alpha()
	ball.fill((0,0,0,0))
	ballRect = ball.get_rect()
	pygame.draw.circle(ball, green, ballRect.center, 50)

	red = 225, 0, 0
	ball2 = pygame.Surface((200, 200)).convert_alpha()
	ball2.fill((0,0,0,0))
	ball2Rect = ball2.get_rect()
	pygame.draw.circle(ball2, red, ball2Rect.center, 50)

	subScreenSurface = screen.copy()
	rectSSS = subScreenSurface.get_rect()

	interpolate = interpolator(0,100,0, screen.get_size()[0])

	subScreenSurface.fill(gray)
	#subScreenSurface.blit(ball, ballRect)

	screen.blit(subScreenSurface,(0,0))

	pygame.display.flip()

	scaledSSS = subScreenSurface
	scale = scaledSSS.get_size()

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
	# def player1():
	# 	global ballPos
	# 	return int(ballPos)
	# print(player1())
	maxSpeed = 0

	ball2Pos = 0
	# @pyqtSlot(int)
	# def player2(x):
	# 	global ball2Pos
	# 	ball2Pos = x
	#ball2Pos = 50
	#player2(90)

	# worker = Worker()
	# worker.signals.pos.connect(player2)
	# pool = QThreadPool()
	# pool.start(worker)

	#parent_conn1, child_conn1 = Pipe()
	#parent_conn2, child_conn2 = Pipe()
	player1 = Value('I', 30)
	player2 = Value('I', 10)
	p = Process(target=f, args=(65435,player1, player2), daemon=True)
	#p.daemon = True
	p.start()

	accumulated = 0
	print("hello")
	while 1:
		#time = clocky.tick(60)
		time = clockpy.tick()
		time = 1000*time
		
		accumulated += time
		
		screenSize = screen.get_size()
		#line = ser.readline()
		#ballPos = int(line.strip())
		#angle = batPos
		
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				#ser.close()
				p.terminate()
				sys.exit(0)
			elif (event.type==pygame.VIDEORESIZE):
				screen=pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
				scale = event.dict['size']
				scale = (scale[0], scale[0]*defaultSize[1]//defaultSize[0])
				print(scale)
				rectSSS = (0,(event.dict['size'][1]-scale[1])//2)
				#scaledSSS=pygame.transform.scale(subScreenSurface, scale)
				#scaledSSS=pygame.transform.smoothscale(subScreenSurface, scale)
			elif (event.type==pygame.KEYDOWN):
				if(event.dict['key']==pygame.K_RIGHT):
					ballPos+= (time*speed)//0.8
				elif(event.dict['key']==pygame.K_LEFT):
					ballPos-= (time*speed)//0.8
		if(pygame.key.get_pressed()[pygame.K_RIGHT]):
			ballPos += time*speed
		if(pygame.key.get_pressed()[pygame.K_LEFT]):
			ballPos -= time*speed
		
		if not p.is_alive():
			sys.exit(0)

		ballPos = max(0, min(ballPos, 100))

		#parent_conn1.send(int(ballPos))
		player1.value = int(ballPos)

		#ball2Pos = 50 + 45*math.sin(2*math.pi*(accumulated)/5000)
		#ball2Pos = parent_conn2.recv()
		ball2Pos = player2.value
		
		ballRect.x = (interpolate(ballPos)) - ball.get_size()[0]//2
		ballRect.y = 250
		
		ball2Rect.x = (interpolate(ball2Pos)) - ball2.get_size()[0]//2
		ball2Rect.y = 0
		
		subScreenSurface.fill(gray)
		##subScreenSurface.blit(back, (0,0))
		subScreenSurface.blit(ball, ballRect)
		subScreenSurface.blit(ball2, ball2Rect)
		
		scaledSSS=pygame.transform.smoothscale(subScreenSurface, scale)
		screen.fill(white)
		screen.blit(scaledSSS,rectSSS)
		#pygame.display.update(ballRect)
		#pygame.display.update(ball2Rect)
		pygame.display.flip()


