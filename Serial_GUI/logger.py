import sys, pygame
import serial as sr
import math
import io

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QPlainTextEdit
from PyQt5 import QtCore

#later QComboBox

# QTextEdit
# setTextBackgroundColor (self, QColor c)
# setTextColor (self, QColor c)

windowsPorts = ["COM" + str(x)  for x in range(8)]

class HapticPaddleGUI(QWidget):
	def __init__(self):
		super().__init__()
		
		self.paddle = HapticPaddle()
		
		self.console = QPlainTextEdit()
		self.console.setReadOnly(True)
		
		self.menu = None
		
		self.mainbox = QVBoxLayout()
		self.mainbox.addWidget(self.console)
		
		self.setLayout(self.mainbox)
	def addSubMenu(self, mainMenu):
		#self.menu = mainMenu.addMenu( hash(self) ) #find a way to make unique identifiable names
		self.menu = mainMenu.addMenu( "Paddle" + str(self.paddle.times) )
	
	def log(self, text):
		pass

class HapticPaddle():
	times = 0
	def __init__(self):
		self.currentPort = None
		self.serial = None
		HapticPaddle.times += 1
		self.textStream = io.StringIO()
		
	def coupleSerial(self):
		try:
			ser = sr.Serial(self.currentPort)
			print("Connected to port "+self.currentPort+"\n"+ser.name)
			conectado = True
		except:
			print("Failed to connect to serial port "+self.currentPort)
			conectado = False
		finally:
			if(conectado):
				self.serial = ser
			return conectado


def portDetector(): #test later
	print([comport.device for comport in sr.tools.list_ports.comports()])



def reader(fileName, timeLimit):
	clocky = pygame.time.Clock()
	clocky.tick(30)

	i=0

	get_time = pygame.time.get_ticks
	time = get_time()
	sum = 0

	with open(fileName, 'w') as fp:
		while sum < timeLimit:
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
	return True





class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "EP3"
		self.left = 20
		self.top = 30
		self.width = 340
		self.height = 200
		self.initUI()

	
	def initUI( self ):
		self.setWindowTitle( self.title )
		self.setGeometry( self.left, self.top, self.width, self.height )

		self.mainMenu = self.menuBar( )
		fileMenu = self.mainMenu.addMenu( 'File' )
		#editMenu = self.mainMenu.addMenu( 'Edit' )
		#self.mainMenu.removeAction(editMenu.menuAction())
		
		exitButton = QAction('Exit', self )
		exitButton.setShortcut( 'Ctrl+Q' )
		exitButton.setStatusTip( 'Exit application' )
		exitButton.triggered.connect( self.close )
		fileMenu.addAction( exitButton )


		self.janela = Janela()
		self.setCentralWidget(self.janela)

		self.show()

class Janela(QWidget):
	def __init__(self):
		super(Janela, self).__init__()
		self.initUI()

	def initUI(self):
		self.setMinimumSize(QtCore.QSize(440, 340))

		buttBox = QHBoxLayout()

		self.buttonComp = QPushButton('Comprimir')
		self.buttonDescomp = QPushButton('Descomprimir')
		self.buttonDescomp.setEnabled(False)

		buttBox.addWidget(self.buttonComp)
		buttBox.addWidget(self.buttonDescomp)
		buttBox.setAlignment(QtCore.Qt.AlignBottom)


		mainbox = QVBoxLayout()
		mainbox.addLayout(buttBox)
		self.setLayout(mainbox)

def main():
	app = QApplication(sys.argv)
	exec = App()
	sys.exit(app.exec_())

if __name__ == "__main__": main()
