import pygame, threading, random, time, sys, math, loadedDefaults, Effects, Items

Trenchcoat = pygame.image.load("Trenchcoat.png")
Generic_Pants = pygame.image.load("Generic_pants.png")
Soviet_Head = pygame.image.load("Head.png")

Trenchcoat = loadedDefaults.spriteSheet("Trenchcoat.png",frmDims = [10,20])
Generic_Pants = loadedDefaults.spriteSheet("Generic_pants.png", frmDims = [10,20])
Soviet_Head = loadedDefaults.spriteSheet("Head.png", frmDims = [10,20])


class saveFile:
	def __init__(self,Sim,configFile = None):
		self.Sim = Sim
		if(configFile):
			self.Source = open(configFile,'r').read()
			print(time.time())

	def loadMap(self,map):
		rawData = open("./maps/"+map,'r').read().split("\n\n")
		exec("self.Sim.Map = " + rawData[1])
		self.Sim.Sprites = ["./sprites/"+i for i in rawData[2].split("\n")]
		for i in range(len(self.Sim.Sprites)):
			try: self.Sim.Sprites[i] = pygame.image.load(self.Sim.Sprites[i])
			except: pass
		self.Sim.Sprites.pop(-1)
		self.Sim.Special_Sprites = {
			"Background": pygame.transform.scale(self.Sim.Sprites.pop(-1),self.Sim.Res)
			}
		self.Sim.Background = self.Sim.Special_Sprites["Background"]
		#self.Sim.Foreground = self.Sim.Sprites.pop(-1)


		

#class Game

class Sim:
	def __init__(self):
		pygame.init()
		self.toggle0 = 0
		self.keysDown = []
		self.effectQueue = [loadedDefaults.testEffect]
		self.activeEffects = []
		self.items = []
		self.itemQueue = []
		self.Sprites = [pygame.image.load("Block.png")]	# Hope to load from map data
		self.Res = [500,500]									# screen resolution
		self.cameraPos = [0,0]							# Camera scroll location
		self.zoom = [40,40]								# Block size
		self.SF = 4										# Scaling factor
		self.bg = [random.randint(0,255) for i in range(3)] # 4 the m3mz
		self.creatures = [Creature(self,is_player=True)]				# Intend to generate from map in future
		
		self.Current = None
		self.Processes =  [threading.Thread(target=i) for i in [self.Display, self.Compute, self.Learn]]	# Suitable for MMO adaptation?
		self.Finished = False	# To kill threads. Forgot about sys.exit(0). Might repurpose
		self.Modes = {	"Title": 1,
						"Main_Menu": 2,
						"Cutscene": 3,
						"In-game scene": 4,
						"In-game": 5,
						"Pause": 6,
						"Script": 7}
		self.Mode = 1
		self.Params = [None,
			{
				"Font": pygame.font.Font("JuliusSansOne-Regular.ttf",48)
			},
			{
				
			}
		]
		self.activeText = [self.Params[1]["Font"].render("When all are dead...", True, (255,255,255))]

		for Process in self.Processes: Process.start()

	def Display(self):
		
		#self.Background = pygame.image.load("test_BG.png")
		#self.Res = [500,500]
		#self.bg = [random.randint(0,255) for i in range(3)]
		self.Clock = pygame.time.Clock()
		try:	self.Window = pygame.display.set_mode(self.Res)
		except Exception as E: print(E+":P")
		#while(True):
			#time.sleep(5)
			#if(self.Mode == self.Modes["Title"]):
				#pass
				
			#if(self.Finished): return
			#self.bg = [self.bg[i] + random.randint(-1,1) for i in range(3)]
			#for i in range(len(self.bg)):
					#if(self.bg[i] > 255): self.bg[i] = 255
					#elif(self.bg[i] < 0): self.bg[i] = 0

	def Compute(self):
		time.sleep(1)
		exec("self.Map = "+open("map.txt",'r').read())

		testIndex = 0

		while(True):
			if(self.Finished): return
			if(self.Mode == self.Modes["Title"]):
				
				for event in pygame.event.get():
					if(event.type == pygame.QUIT): pygame.quit()
					if(event.type == pygame.KEYDOWN):
					#self.Finished = True
						if(event.key == pygame.K_ESCAPE):
							self.Finished = True
							pygame.quit()
						elif(event.key == pygame.K_RETURN):
							self.Mode = 2
							
				try:
					self.Window.blit(self.activeText[0],[50,50])
				except Exception as E: print(E)
				
			elif(self.Mode == self.Modes["Main_Menu"]):	
				
				for event in pygame.event.get():
					if(event.type == pygame.QUIT): pygame.quit()
					if(event.type == pygame.KEYDOWN):
					#self.Finished = True
						if(event.key == pygame.K_ESCAPE):
							#self.Finished = True
							pygame.quit()
						elif(event.key == pygame.K_RETURN):
							#self.Mode = 2
							self.saveFile = saveFile(self)
							self.saveFile.loadMap("Home_Lab_I")
							self.Mode = self.Modes["In-game"]
				
				self.Window.fill([0,0,0])
				self.Window.blit(self.Params[1]["Font"].render("Fresh boot", True, (255,255,255)), [200,350])
				#self.Window.blit("Materialize from cached configuration")
				#self.Window.blit("Custom materialization")
				
			elif(self.Mode == self.Modes["In-game"]):
					self.effectQueue = [i for i in self.effectQueue if i]
					while(len(self.effectQueue)):
						print(self.effectQueue)
						self.effectQueue[0].Effect([self])
						self.activeEffects.append(self.effectQueue.pop(0))
					for effect in [ sf for sf in list(reversed(range(len(self.activeEffects)-1)))]:
						print(effect)
						if(self.activeEffects[effect].endCondition([self])):
							self.activeEffects.pop(effect)
					for event in pygame.event.get():
						try:
							if(event.type == pygame.KEYDOWN):self.keysDown.append(event.key)
							elif(event.type == pygame.KEYUP): self.keysDown.remove(event.key)
						except: pass
				
					self.Window.fill(self.bg)
					self.Window.blit(self.Background,[0,0])
					self.QueryAll()
					self.mapDraw()
					self.physUpdate()
					self.UI_Response()
					#time.sleep(0.2)
					self.Clock.tick(20)

			elif(self.Mode == self.Modes["Script"]):
				if(self.activeScript):
				
					self.Window.fill(self.bg)
					self.Window.blit(self.Background,[0,0])
					self.mapDraw()
					self.scriptDraw()
#					self.physUpdate()
#					self.UI_Response()
					#time.sleep(0.2)
					self.Clock.tick(20)
				else:
					pass


			elif(self.Mode == self.Modes["Pause"]): pass
					
			pygame.display.flip()
				
	def mapDraw(self):
			for i in range(len(self.Map) - 2): assert(len(self.Map[i]) == len(self.Map[i+1]))
			for i in range(len(self.Map)):
				for j in range(len(self.Map[0])):
					if(self.Map[i][j]):
						#self.Window.blit(pygame.transform.scale(self.Sprites[self.Map[i][j]-1],self.zoom),[self.zoom[1]*j-self.cameraPos[0],self.zoom[0]*i-self.cameraPos[0]])
						self.Window.blit(pygame.transform.scale(self.Sprites[self.Map[i][j]-1],self.zoom),[self.zoom[1]*j-self.cameraPos[0],self.zoom[0]*i-self.cameraPos[1]])
						
	def scriptDraw(self):
		if(not self.Current):
			self.Current = self.activeScript.pop(0)
		if(self.Current[0] == "Talk"):
			self.Window.blit(pygame.transform.scale(self.Current[1],[int(self.Res[0]*0.9),int(self.Res[1]*0.35)]),[int(self.Res[0]*0.05),int(self.Res[1]*0.6)])#[int(self.Res[0]*0.9),int(self.Res[1]*0.35)])
			self.Window.blit(pygame.transform.scale(self.Current[2],
			[int(self.Res[0]*0.2),int(self.Res[1]*0.2)]),
			[int(self.Res[0]*0.1),self.Res[1]*0.65])
			
			self.Window.blit(self.Params[1]["Font"].render(self.Current[3], True, (255,255,255)), [int(self.Res[0]*0.3),int(self.Res[1]*0.65)])


		elif(self.Current[0] == "Action"):
			if(self.Current[1] == "Return"):
				pass
#				self.effectQueue.remove(self.Current)
				self.Mode = self.Modes["In-game"]
			
		for event in pygame.event.get():
			try:
				if(event.type == pygame.KEYDOWN):
					self.keysDown.append(event.key)
					if(event.key == pygame.K_RETURN):
						self.Current = None
				elif(event.type == pygame.KEYUP):
					self.keysDown.remove(event.key)
			except: pass
		
	def UI_Response(self):
		for event in pygame.event.get():
			if(event.type == pygame.KEYDOWN):
				try: self.keysDown.append(event.key)
				except: pass
			elif(event.type == pygame.KEYUP):
				try: self.keysDown.remove(event.key)
				except: pass
	
	def envelSqr(self,Creature): pass
		
		
	def physUpdate(self):
		for item in self.itemQueue:
			self.items.append(item[0]())
			self.items[-1].pos = item[1]
			for effect in self.items[-1].Params["Effects"]:
				if(effect):
					self.effectQueue.append(effect)
					effect.itemBound = item
			
		for Creature in self.creatures + self.items:
			#print(Creature.pos,self.cameraPos)
			Creature.lastPos = Creature.pos
			Creature.pos = [Creature.pos[i] + Creature.velocity[i] for i in range(2)]
			Creature.velocity = [Creature.velocity[i] + Creature.accel[i] for i in range(2)]
			Creature.accel = [Creature.accel[i] * Creature.airDense for i in range(2)]

			if(not (Creature.grounded or Creature.latched) or True): Creature.velocity[1] += 4.0
			if(Creature.grounded): Creature.velocity[0] = Creature.accel[0] = 0.0
			if(Creature.latched): Creature.velocity = Creature.accel = [0.0,0.0]

			envelopedSquares = True
			toggle = False
			if(True):
				mins = [loadedDefaults.shDiv(Creature.pos[i],self.zoom[i]) for i in range(2)]
				maxes = [loadedDefaults.shDiv(Creature.pos[i]+self.zoom[i]*Creature.dims[i],self.zoom[i]) for i in range(2)]
				
				for i in [mins[0],maxes[0]]:
					if(self.Map[loadedDefaults.shDiv(mins[1]+maxes[1],2)][i] == 1):
						if(i == mins[0]):
							Creature.pos[0] += (self.zoom[0] - (Creature.pos[0] % self.zoom[0]))
							Creature.velocity[0] = 0
						elif(i == maxes[0]):
							Creature.pos[0] -= (Creature.pos[0] + Creature.dims[0] * self.zoom[0]) % self.zoom[0] + 1
							Creature.velocity[0] = 0

							
				mins = [loadedDefaults.shDiv(Creature.pos[i],self.zoom[i]) for i in range(2)]
				maxes = [loadedDefaults.shDiv(Creature.pos[i]+self.zoom[i]*Creature.dims[i],self.zoom[i]) for i in range(2)]

				for i in [mins[1],maxes[1]]:
					if(self.Map[i][loadedDefaults.shDiv(mins[0]+maxes[0]+1,2)] == 1):
						if(i == mins[1]):
							Creature.pos[1] += (self.zoom[1] - (Creature.pos[1] % self.zoom[1]))
							Creature.velocity[1] = 0
						elif(i == maxes[1]):
							Creature.pos[1] -= (Creature.pos[1] + Creature.dims[1] * self.zoom[1]) % self.zoom[1] + 1
							Creature.velocity[1] = 0
							Creature.grounded = True
				
				for j in [mins[1],maxes[1]]:
					if(self.Map[i][j] == 1):
						pass

				print(mins, maxes)
				
		for Creature in self.creatures + self.items:
			for layer in Creature.spriteLayers:
				if(Creature.velocity[0] < 0):
				 	self.Window.blit(pygame.transform.flip(pygame.transform.scale(layer.Sheet,[a*self.SF for a in layer.sRes]),True,False),[self.Res[i]/2 + self.zoom[i]*Creature.sprOffset[i] for i in range(2)],(1920*4-self.SF*layer.frmDims[0]*(Creature.frm+1),frmDims[1]*Creature.idx,self.SF*frmDims[0],self.SF*frmDims[1]))
				else:
					self.Window.blit(pygame.transform.scale(layer.Sheet,[a*self.SF for a in layer.sRes]),
				 [self.Res[i]/2 + self.zoom[i]*Creature.sprOffset[i] for i in range(2)],(self.SF*10*Creature.frm,self.SF*20*Creature.idx,self.SF*10,self.SF*20))
			#pygame.draw.rect(self.Window,(0,0,0,0),[Creature.pos[0],Creature.pos[1],self.zoom[0]*Creature.dims[0],self.zoom[1]*Creature.dims[1]],1)
			pygame.draw.rect(self.Window,(0,0,0,0),[self.Res[0]/2, self.Res[1]/2,self.zoom[0]*Creature.dims[0],self.zoom[1]*Creature.dims[1]],1)
			Creature.frm = (Creature.frm + 1) % 9
		#	if(not Creature.frm or True):
		#		Creature.idx = Creature.qidx
		#		Creature.qidx = Creature.qidx2
			
	def QueryAll(self):
		for Creature in self.creatures:
			if(Creature.is_player):
				self.cameraPos = [Creature.pos[i] - self.Res[i]/2 for i in range(2)]
						
			Creature.Query()
			Move = Creature.Response
			
			if(not (-2 <= Move["LR"] and Move["LR"] <= 2)): Move["LR"] = 0
			if(Move["LR"] == 2):	# Run right
				if(Creature.grounded): Creature.velocity[0] = (Creature.accelLR * Creature.maxRunVelo + Creature.velocity[0]) / 2.0
#				Creature.velocity[0] = 4.0
			elif(Move["LR"] == 1):	# Walk right
				if(Creature.grounded): Creature.velocity[0] = (Creature.accelLR * Creature.maxWalkVelo + Creature.velocity[0]) / 2.0
				else: Creature.velocity[0] *= (Creature.maxAirVelo)
#				Creature.velocity[0] = 8.0
			elif(Move["LR"] == 0):	# Idle
				if(Creature.grounded): Creature.velocity[0] *= Creature.Slippery
				else: Creature.velocity[0] = Creature.velocity[0] * Creature.airDense
			elif(Move["LR"] == -1):	# Walk left
				if(Creature.grounded): Creature.velocity[0] = (-1 * Creature.accelLR * Creature.maxWalkVelo + Creature.velocity[0]) / 3.0
				else: Creature.velocity[0] *= (Creature.maxAirVelo)
				Creature.velocity[0] = -8.0
			elif(Move["LR"] == -2):	# Run left
				if(Creature.grounded): Creature.velocity[0] = (-1 * Creature.accelLR * Creature.maxRunVelo + Creature.velocity[0]) / 3.0
#				Creature.velocity[0] = -4.0
				
				
			if(Move["Item"] != 0):
				if(Move["Item"] == 1): self.effectQueue.append(Creature.Items["Primary-Equipped"].Params["Interact"]["action-1"]([Creature.Items["Primary-Equipped"],self]))		# Primary attack with active weapon; usually a heavier attack
				elif(Move["Item"] == 2): self.effectQueue.append(Creature.weapons[0].secondary)	# Secondary attack with active weapon; usually a quick jab
				elif(Move["Item"] == 3):
					self.effectQueue.append(Creature.weapons[1].secondary) # Quick attack with secondary weapon when the primary weapon is two-handed; if both are one-handed or it is hybrid, a primary attack. If a focus weapon, it is the tertiary attack.
				elif(Move["Item"] == 4):
					pass	# Secondary attack from second weapon when dual-wielding or hybridized. If focus, slot 4.
				elif(Move["Item"] == 5):
					pass # For using your active utility gear: wings, industrial battery, climbing gear, et cetera.
				elif(Move["Item"] == 6): # For using some trinket currently active. A magic gem, grenade, or network packet capturer, something of the sort.
					pass
				elif(Move["Item"] == 7):
					pass # If the square has a creature or item on it, you can interact with it.
				elif(Move["Item"] == 8):
					pass # Moving items around.
				
			if(Move['UD'] == 1):
				if(Creature.grounded):
					Creature.velocity[1] -= 16.0
					Creature.pos[1] -= 5
					Creature.grounded = False
					Creature.frm = 0
					Creature.qidx = 1
					Creature.qidx2 = 0
			
			if(Move['UD'] == -1):
				if(not Creature.grounded):
					Creature.velocity[1] += 0.5
				
			if(Creature.Response["Point"]): Creature.pointdir = Creature.Response["Point"]
			
			if(Creature.is_player): Creature.lastFrame = Creature.Response
			for i in Creature.Response: Creature.Response[i] = 0

	def Learn(self): return

	def Dialogue(self,pause=1):
		if(pause == 1):
			pass


class Creature:
	def __init__(self,Sim,Head=Soviet_Head,Body=Trenchcoat,Legs=Generic_Pants,is_player = False):
		self.Sim = Sim
		self.is_player = is_player
		
		self.lmaxes = self.lmins = [0,0]
		
		self.Response = {	"LR": 0,
				   			"UD": 0,
				   			"Move": 0,
				   			"Item": 0,
				   			"Point": 0,
				   			"Signal": 0,
				   			"Itemch": 0,
						}
		
		self.Items = {
			"Primary-Equipped": Items.GameItems["Grenade-Launcher"]()
		}
		
		#self.ActiveItems = [Items.Item(["Grenade"])]

		if(self.is_player): self.lastFrame = self.Response
		
		self.spriteLayers = [Head,Body,Legs]
		
		self.HP = 1.0
		
		self.dims = [0.5,1.5]
		self.sprOffset = [-0.2,-0.3]
		
		self.pos = [50,50]
		self.lastPos = self.pos
		self.velocity = [0,0]
		self.accel = [0,0]
		
		self.frm = self.idx = self.qidx = self.qidx2 = 0
		
		self.maxWalkVelo = 16.0
		self.maxRunVelo = 32.0
		self.maxAirVelo = 0.95
		
		self.accelLR = 1.8
		self.Slippery = 0.5
		self.airDense = 0.98
		
		self.grounded = False
		self.latched = False
		
		self.Offense_Coeff = 0.5
		self.Combative_Coeff = 0.5
		self.Lethal_Coeff = 0.5
		self.Careful_Coeff = 0.5
		
	def Query(self):
		if(self.is_player):
			if(pygame.K_LEFT in self.Sim.keysDown):
				if(pygame.K_RIGHT in self.Sim.keysDown): self.Response["LR"] = 0
				else: self.Response["LR"] = -1
			elif(pygame.K_RIGHT in self.Sim.keysDown): self.Response["LR"] = 1
			else: self.Response["LR"] = 0
			if(pygame.K_LSHIFT in self.Sim.keysDown): self.Response["LR"] *= 2
			
			if(pygame.K_UP in self.Sim.keysDown):
				print("Boing",self.velocity)
				if(pygame.K_DOWN in self.Sim.keysDown): self.Response["UD"] = 0
				else: self.Response["UD"] = 1
			elif(pygame.K_DOWN in self.Sim.keysDown): self.Response["UD"] = -1
			
			if(pygame.K_a in self.Sim.keysDown):
				if(pygame.K_d in self.Sim.keysDown): self.Response["Point"] = 0
				elif(pygame.K_s in self.Sim.keysDown): self.Response["Point"] = 6
				elif(pygame.K_w in self.Sim.keysDown): self.Response["Point"] = 4
				else: self.Response["Point"] = 5			
			elif(pygame.K_s in self.Sim.keysDown):
				if(pygame.K_w in self.Sim.keysDown): self.Response["Point"] = 0
				elif(pygame.K_a in self.Sim.keysDown): self.Response["Point"] = 6
				elif(pygame.K_d in self.Sim.keysDown): self.Response["Point"] = 8
				else: self.Response["Point"] = 7			
			elif(pygame.K_d in self.Sim.keysDown):
				if(pygame.K_a in self.Sim.keysDown): self.Response["Point"] = 0
				elif(pygame.K_s in self.Sim.keysDown): self.Response["Point"] = 8
				elif(pygame.K_w in self.Sim.keysDown): self.Response["Point"] = 2
				else: self.Response["Point"] = 1			
			elif(pygame.K_w in self.Sim.keysDown):
				if(pygame.K_s in self.Sim.keysDown): self.Response["Point"] = 0
				elif(pygame.K_d in self.Sim.keysDown): self.Response["Point"] = 2
				elif(pygame.K_a in self.Sim.keysDown): self.Response["Point"] = 4
				else: self.Response["Point"] = 3
			elif(pygame.K_1 in self.Sim.keysDown): self.Response["Item"] = 1
			else: self.Response["Point"] = 0
				
			
			
			
	def Move(self): return 0
	def itemAction(self): return 0
	def Point(self): return 0
	def Aerial(self): return 0
	def Signal(self): return 0

	def AnimControl(self):
		pass

class Player(Creature):
	def Move(self):
		return 0
	def itemAction(self): return 0
	def Point(self): return 0
	def Aerial(self): return 0
	def Signal(self): return 0



F = Sim()
