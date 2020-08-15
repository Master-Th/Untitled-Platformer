import threading, random, time, pyautogui, numpy as np, datetime, os, pygame, easygui,loadedDefaults
from PIL import Image

class Display:
	def __init__(self):
		
		self.mapImage = {}
		self.currentTerrain = 1
		self.winDim = [1000,1000]
		self.viewSpace = [900,800]
		self.winId = random.randint(0,1)
		self.zoom = [50,50]
		self.pos = [0,0]
		self.dragPoint = 0
		self.TerrainTextures = {
			"1": pygame.image.load("./sprites/Lab_Hard_Block.png"),
			"3": pygame.image.load("./sprites/Hard_Block_Test.png")
		}
		self.BG = [loadedDefaults.Paralayer("test_BG.png",[50,50],[0.8,0.8],[0.1,0.1])]

		self.Window = pygame.display.set_mode(self.winDim)
		
		self.Processes =  [threading.Thread(target=i) for i in [self.Main,self.input]]
		self.Finished = False

		for Process in self.Processes:
			Process.start()

	def Main(self):

		while(True):
			for event in pygame.event.get():
				#print(event)
				if(event.type == pygame.KEYDOWN):
					if(event.key == pygame.K_s): self.save()
					elif(event.key == pygame.K_ESCAPE):
						pygame.quit()
				elif(event.type == pygame.MOUSEBUTTONDOWN):
					self.clicks(event.button,0,event.pos[0],event.pos[1])
				elif(event.type == pygame.MOUSEMOTION):
					if(pygame.mouse.get_pressed()[0]):
						self.pos = [self.pos[i] - event.rel[1-i] for i in range(2)]


			self.Window.fill((0,0,0,0))

			for Layer in self.BG:
				self.Window.blit(pygame.transform.scale(Layer.sprite,[int(Layer.res[i] / Layer.zoom[i]) for i in range(2)]),[Layer.zoom[i]*(Layer.init[i]-Layer.pace[i]*self.pos[1-i]) for i in range(2)])

	#		pygame.draw.rect(self.Window,(255,255,255),[50,50,self.winDim[0]-100,self.winDim[1]-100])

			for i in range(int(self.viewSpace[0]/self.zoom[0])+1):

				offset = self.pos[1] % self.zoom[1]
				pygame.draw.line(self.Window, (0,0,0,0),[50-offset+self.zoom[0]*i,50],[50-offset+self.zoom[0]*i,self.winDim[1]-50])

			for i in range(int(self.viewSpace[1]/self.zoom[1])+1):

				offset = self.pos[0] % self.zoom[0]
				pygame.draw.line(self.Window, (0,0,0,0),[50,50-offset+self.zoom[1]*i],[self.winDim[0]-50,50-offset+self.zoom[1]*i])

			for i,j in self.mapImage.items():
				i = [int(u) for u in i.split("_")]
				placement = [i[1]*self.zoom[1] - self.pos[1], i[0]*self.zoom[0] - self.pos[0], self.zoom[0], self.zoom[1]]
				try:
					self.Window.blit(pygame.transform.scale(self.TerrainTextures[str(j)],self.zoom),placement)
				except Exception as E:
					print(E)
					#pygame.draw.rect(self.Window,(255,0,0),placement)

			pygame.draw.rect(self.Window,(0,0,0,0),[0,0,50,self.viewSpace[1]])
			pygame.draw.rect(self.Window,(0,0,0,0),[0,0,self.viewSpace[0],50])
			pygame.draw.rect(self.Window,(0,0,0,0),[self.viewSpace[0]-50,0,self.winDim[0],self.winDim[1]])
			pygame.draw.rect(self.Window,(0,0,0,0),[0,self.viewSpace[1]-50,self.winDim[1],self.winDim[0]])

			pygame.display.update()


		if(self.dragPoint):
			self.pos = [self.pos[0] - self.dragPoint[1] + pyautogui.position().y, self.pos[1] + pyautogui.position().x - self.dragPoint[0]]
			self.dragPoint = [pyautogui.position().x,pyautogui.position().y]
			#print(self.pos)

	def clicks(self,button,state,x,y):
		#print(button,state,x,y)
		if(button == 1):
			if(state == 0):
				self.dragPoint = pyautogui.position()
			else:
				self.dragPoint = 0
		elif(button == 2): self.zoom = [50,50]
		elif(button == 3):
			if(state == 0):
				name_X = ((self.pos[0]+y))/self.zoom[1]
				if(name_X <= 0): name_X -= 1
				name_X = int(name_X)

				name_Y = ((self.pos[1]+x))/self.zoom[0]
				if(name_Y <= 0): name_Y -= 1
				name_Y = int(name_Y)
				self.mapImage[str(name_X)+"_"+str(name_Y)] = self.currentTerrain
				if(not self.currentTerrain): del self.mapImage[str(name_X)+"_"+str(name_Y)]
			print(self.mapImage)
		elif(button == 3): self.zoom = [int(i * 19.0/20.0) for i in self.zoom]
		elif(button == 4): self.zoom = [int(i * 20.0/19.0) for i in self.zoom]

	def input(self):
		while(True):
			Command = easygui.textbox(msg='', title='Enter options', text='', codebox=False, callback=None, run=True).split(" ")
			try: 
				if(len(Command) == 1):
					if(not int(Command[0]) or str(Command[0]) in self.TerrainTextures or 1): self.currentTerrain = int(Command[0])
				if(Command[0] == "Texture_Set"):
					Command[1] = str(int(Command[1]))
					self.Textures[Command[1]] = pygame.image.load("./sprites/" + Command[2])
				elif(Command[0] == "Add_To_Background"):
					try: self.Background.insert(int(Command[1]),loadedDefaults.Background_Layer("./Backgrounds/"+Command[2]))
					except: self.Background.append(loadedDefaults.Background_Layer("./Backgrounds/"+Command[2],list(Command[3])))
			except Exception as E:
				easygui.buttonbox(msg=E, title='!', choices=('mmkay'), image=None, images=None, default_choice=None, cancel_choice=None, callback=None, run=True)

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
			map_Form[int(a[0])-X_diff+1][int(a[1])-Y_diff+1] = self.mapImage[item]
		
			
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
