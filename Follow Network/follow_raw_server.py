import serial as sr
import math
import socket


from multiprocessing import Process, Pipe, Value


TCP_IP = ''
BUF_SIZE = 30
#T_PORT = 65435

#Parallelize the server stuff
def f(T_PORT, player1, player2):
	print("I'm",socket.gethostbyname(socket.gethostname()))
	TCP_IP = socket.gethostname()

	with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as k:
		k.bind((TCP_IP, T_PORT))
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
def ard(ser, potencio):
	try:
		#ser = sr.Serial(S_PORT, timeout=0.01)
		ser = sr.Serial("COM3", timeout=0.1)
		print(ser.name)
	except sr.SerialException as msg:
		print( "Error opening serial port %s" % msg)
		print("Failed to connect to serial")
		ser = False
	if(ser):
		while(True):
			lineraw = ser.readline()
			line = str(lineraw, 'utf-8')
			line = line.strip()
			#lines = "".join([str(x, 'utf-8') for x in lineraw])
			#lines = lines.strip().split('\r\n')
			#lines = [x for x in lines if len(x)>0]
			#lines = "".join(lines)
			#lines = lines.strip().split('\n')
			#lines = "".join(lines)
			#print(line)
			#lines = lineraw
			try:
				value = float(line)

				#print(value)
				potencio.value = value
			except ValueError:
				print("Error: ", lineraw)

if __name__ == "__main__":
	import sys, pygame
	#import pyglet

	def interpolator(left_min, left_max, right_min, right_max):
		leftSpan = left_max - left_min
		rightSpan = right_max - right_min
		scaleFactor = float(rightSpan)/float(leftSpan)
		def interpol_funct(value):
			return right_min + (value-left_min)*scaleFactor
		return interpol_funct

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

	screen.blit(subScreenSurface,(0,0))

	pygame.display.flip()

	scaledSSS = subScreenSurface
	scale = scaledSSS.get_size()

	# ser = serial.Serial('COM3')
	# print(ser.name)

	speed = 0.05


	#clockpy = pyglet.clock.Clock()
	#clockpy.set_fps_limit(60)

	clocky = pygame.time.Clock()

	#line = ser.readline()
	#ballPos = int(line.strip())
	#ballPos = screen.get_size()[0]//2
	
	maxSpeed = 0
	ballPos = 50
	ball2Pos = 0

	player1 = Value('I', 30)
	player2 = Value('I', 10)
	p = Process(target=f, args=(65435, player1, player2), daemon=True)
	p.start()

	potencio = Value('f', 0)
	p2 = Process(target=ard, args=("COM3", potencio), daemon=True)
	p2.start()

	accumulated = 0
	
	while 1:
		#time = clockpy.tick()
		time = clocky.tick_busy_loop(60)
		#time = 1000*time
		
		accumulated += time
		
		screenSize = screen.get_size()
		#line = ser.readline()
		#ballPos = int(line.strip())
		#angle = batPos
		
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				#ser.close()
				p.terminate()
				p2.terminate()
				sys.exit(0)
			elif (event.type==pygame.VIDEORESIZE):
				screen=pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
				scale = event.dict['size']
				scale = (scale[0], scale[0]*defaultSize[1]//defaultSize[0])
				print(scale)
				rectSSS = (0,(event.dict['size'][1]-scale[1])//2)
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

		ballPos = 50+50*potencio.value
		ballPos = max(0, min(ballPos, 100))

		
		player1.value = int(ballPos)

		
		ball2Pos = player2.value
		
		ballRect.x = (interpolate(ballPos)) - ball.get_size()[0]//2
		ballRect.y = 250
		
		ball2Rect.x = (interpolate(ball2Pos)) - ball2.get_size()[0]//2
		ball2Rect.y = 0
		
		subScreenSurface.fill(gray)
		subScreenSurface.blit(ball, ballRect)
		subScreenSurface.blit(ball2, ball2Rect)
		
		scaledSSS=pygame.transform.smoothscale(subScreenSurface, scale)
		screen.fill(white)
		screen.blit(scaledSSS,rectSSS)
		pygame.display.flip()


