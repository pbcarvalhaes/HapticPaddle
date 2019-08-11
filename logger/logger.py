import sys, pygame
import serial as sr
import math
import time

#pygame.init()

angle = 0

try:
	#ser = sr.Serial('COM3', timeout=0.01)
	ser = sr.Serial('COM3', timeout=1)
	print(ser.name)
except:
	print("Failed to connect to serial")
	ser = False

clocky = pygame.time.Clock()
clocky.tick(120)

i=0

get_time = pygame.time.get_ticks
time = get_time()
sum = 0

filename = "data_" + time.strftime("%Y.%m.%d_%H.%M.%S") + ".txt"

print("hello \n")
with open(filename, 'w') as fp:
	while sum < 10000:
		time = clocky.tick(10)
		if(ser):
			lineraw = ser.readlines()
			line = str(lineraw, 'utf-8')
			lines = line.split('\n')
			if(len(lines)<=1):
				continue
			try:
				#values = [float(x) for x in lines]
				values = map(float, lines)
				i+=1
				if(i>20):
					print("fps:", clocky.get_fps())
					i= i%20
				#pairs = [(str(x)+","+str(i*time/len(values))) for i,x in enumerate(values)]
				pairs = ["{0:d},{1:.6f}".format(x,sum+(i*time/len(values))) for i,x in enumerate(values)]
				fp.write("\n".join(pairs))
				
			except ValueError:
				print(line)
		sum += time
print("done :)")


