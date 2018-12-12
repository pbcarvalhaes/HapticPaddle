import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


dataFiles = [x for x in os.listdir() if ".csv" in x]

for file in dataFiles:
	data = pd.read_csv(file, names=["Signal", "Time"])
	
	fig = plt.figure()
	plt.plot(data.Time/1000, data.Signal)
	plt.ylabel("leitura do sensor")
	plt.xlabel("Tempo (s)")
	plt.grid()
	bottom, top = plt.ylim()
	if(bottom>0 and bottom < top):
		plt.ylim(bottom=0, top=1.01*top)
	elif(top<0 and bottom<top):
		plt.ylim(top=0, bottom=1.01*bottom)
	ax = plt.gca()
	ax.ticklabel_format(useOffset=False, style="plain")
	pictureFile = file.replace(".csv", ".png")
	fig.savefig(pictureFile)
