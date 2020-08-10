import threading, random, time, pyautogui, numpy as np, datetime, os
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtOpenGL

def refresh2D(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

class Display:
	def __init__(self):
		
		self.mapImage = {}
		self.currentTerrain = 1
		self.winDim = [800,400]
		self.viewSpace = [700,800]
		self.winId = random.randint(0,1)
		self.zoom = [50,50]
		self.pos = [0,0]
		self.dragPoint = 0
		
		self.Processes =  [threading.Thread(target=i) for i in [self.glLoop]]
		self.Finished = False

		for Process in self.Processes:
			Process.start()

	def glLoop(self):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.winDim[0],self.winDim[1])
		glutInitWindowPosition(200,300)
		window = glutCreateWindow("Level Editor")
		glutDisplayFunc(self.draw)
		glutMouseFunc(self.clicks)
		glutKeyboardFunc(self.taptaps)
		glutIdleFunc(self.draw)
		glutMainLoop()
		
	def rect(self, x, y, w, h):
		glBegin(GL_QUADS)
		glVertex2f(x,y)
		glVertex2f(x+w,y)
		glVertex2f(x+w,y+h)
		glVertex2f(x,y+h)
		glEnd()
		
	def line(self,x,y,X,Y):
		glBegin(GL_LINES)
		glVertex2f(x,y)
		glVertex2f(X,Y)
		glEnd()
		
	def clicks(self,button,state,x,y):
		print(button,state,x,y)
		if(button == 0):
			if(state == 0):	self.dragPoint = pyautogui.position()
			else:
				self.dragPoint = 0
		elif(button == 1): self.zoom = [50,50]
		elif(button == 2):
			if(state == 0):
				name_X = (self.winDim[1]-(-1*self.pos[0]+y))/self.zoom[1]
				if(name_X <= 0): name_X -= 1
				name_X = int(name_X)

				name_Y = ((self.pos[1]+x))/self.zoom[0]
				if(name_Y <= 0): name_Y -= 1
				name_Y = int(name_Y)
				self.mapImage[str(name_X)+"_"+str(name_Y)] = self.currentTerrain
			print(self.mapImage)
		elif(button == 3): self.zoom = [int(i * 19.0/20.0) for i in self.zoom]
		elif(button == 4): self.zoom = [int(i * 20.0/19.0) for i in self.zoom]
			
			
	def taptaps(self,Key,x,y):
		print(Key)
		if(Key == b's'):
			self.save()
		
	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		
		if(self.dragPoint):
			self.pos = [self.pos[0] - self.dragPoint[1] + pyautogui.position().y, self.pos[1] - pyautogui.position().x + self.dragPoint[0]]
			self.dragPoint = [pyautogui.position().x,pyautogui.position().y]
			print(self.pos)
		refresh2D(self.winDim[0],self.winDim[1])
		glColor3f(1.0,1.0,1.0)
		self.rect(50,50,self.winDim[0]-100,self.winDim[1]-100)
		glColor3f(0.0,0.0,0.0)
		for i in range(int(self.viewSpace[0]/self.zoom[0])+1):
			offset = self.pos[0] % self.zoom[0]
			self.line(50,50-offset+self.zoom[0]*i,self.winDim[0]-50,50-offset+self.zoom[0]*i)

		
		for i in range(int(self.viewSpace[1]/self.zoom[1])+1):
			offset = self.pos[1] % self.zoom[1]
			self.line(50-offset+self.zoom[1]*i,50,50-offset+self.zoom[1]*i,self.winDim[1]-50)
			
			
		glColor3f(1.0,0.0,0.0)
		for i,j in self.mapImage.items():
			i = [int(u) for u in i.split("_")]
			self.rect(i[1]*self.zoom[1] - self.pos[1], i[0]*self.zoom[0] - self.pos[0], self.zoom[0], self.zoom[1])
			

		
		glutSwapBuffers()

	def save(self):
		X_Range = [None,None]
		Y_Range = [None,None]
		for item in self.mapImage:
			print(item)
			a = [int(i) for i in item.split("_")]
			if(None in X_Range): X_Range = [int(a[0]) for i in range(2)]
			elif(a[0] < X_Range[0]): X_Range[0] = int(a[0])
			elif(a[0] > X_Range[1]): X_Range[1] = int(a[0])
			if(None in Y_Range): Y_Range = [int(a[1]) for i in range(2)]
			elif(a[1] < Y_Range[0]): Y_Range[0] = int(a[1])
			elif(a[1] > Y_Range[1]): Y_Range[1] = int(a[1])
			
		X_diff = X_Range[1]-X_Range[0]
		Y_diff = Y_Range[1]-Y_Range[0]
		
		map_Form = [[0 for i in range(0,X_diff+1)] for y in range(0,Y_diff+1)]
		print(len(map_Form),len(map_Form[0]))
		
		for item in self.mapImage:
			a = [i for i in item.split("_")]
			print(a)
			map_Form[int(a[0])-X_diff][int(a[1])-Y_diff] = self.mapImage[item]
		
			
		print(X_Range,Y_Range)
			
		#map_Form = "-_-"

		i = 0
		while(1):
			if (os.path.exists("./Saved_Map_"+str(i)+".txt")):
				i += 1
			else:
				break
		
			
		open("Saved_Map_"+str(),'w').write(str(map_Form))
Display()
