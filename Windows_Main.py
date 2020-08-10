import pygame, threading, random, time, sys

Trenchcoat = pygame.image.load("Trenchcoat.png")
Generic_Pants = pygame.image.load("Generic_pants.png")
Soviet_Head = pygame.image.load("Head.png")

def shDiv(a,b): return int(float(a)/float(b))

class saveFile:
	def __init__(self,Sim,configFile = None):
		self.Sim = Sim
		if(configFile):
			self.Source = open(configFile,'r').read()
			print(time.time())

	def loadMap(self,map):
		rawData = open(".\\maps\\"+map,'r').read().split("\n\n")
		exec("self.Sim.Map = " + rawData[1])
		print(rawData[2])
		self.Sim.Sprites = [".\\sprites\\"+i for i in rawData[2].split("\n")]
		print(self.Sim.Sprites)
		for i in range(len(self.Sim.Sprites)):
			try: self.Sim.Sprites[i] = pygame.image.load(self.Sim.Sprites[i])
			except: pass
		self.Sim.Sprites.pop(-1)
		print(self.Sim.Sprites)
		self.Sim.Background = self.Sim.Sprites.pop(-1)
		#self.Sim.Foreground = self.Sim.Sprites.pop(-1)

class spriteSheet:
	def __init__(self,pyGLayer,sRes = [1920,1080]):
		self.sRes = sRes
		self.Sheet = pygame.image.load(pyGLayer)
		
class HumanoidSprites(spriteSheet):
	def __init__(self, pyGLayer,sRes = [1920,1080]):
		self.Sheet = pygame.image.load(pyGLayer)
		self.sRes = sRes
		self.Animations = {
		"Walk": 0,
		"Run" : 1,
		"bw_Walk": 2,
		"bw_Run": 3,
		"climb": 4,
		"call": 5,
		"idle": 6,
		"light_flinch": 7,
		"medium_flinch_1": 8,
		"medium_flinch_2": 9,
		"heavy_flinch_1": 10,
		"heavy_flinch_2": 11,
		"heavy_flinch_3": 12,
		"shot_dead": 13,
		"dissolved": 14,
		"transmutation": 15,
		"dismembered": 16,
		"swim": 17,
		"dive": 18,
		"spellcast_light": 19,
		"spellcast_heavy": 20,
		"spellcast_heavy_2"
		"spellcast_master": 21,
		"melee_light": 22,
		"melee_heavy": 23,
		"melee_heavy_2": 24,
		"melee_master": -1,
		"shielded_light": 25,
		"shielded_heavy": 26,
		"shielded_heavy_2":27,
		"shielded_master": 27,
		"ranged_AOE": 28,
		"ranged_laser": 29,
		"other": 30
		}

Trenchcoat = HumanoidSprites("Trenchcoat.png")
Generic_Pants = HumanoidSprites("Generic_pants.png")
Soviet_Head = HumanoidSprites("Head.png")

#class Game

class Sim:
	def __init__(self):
		pygame.init()
		
		self.Sprites = [pygame.image.load("Block.png")]	# Hope to load from map data
		self.Res = [500,500]									# screen resolution
		self.cameraPos = [0,0]							# Camera scroll location
		self.zoom = [40,40]								# Block size
		self.SF = 4										# Scaling factor
		self.creatures = [Creature(self,is_player=True)]				# Intend to generate from map in future

		self.Processes =  [threading.Thread(target=i) for i in [self.Display, self.Compute, self.Learn]]	# Suitable for MMO adaptation?
		self.Finished = False	# To kill threads. Forgot about sys.exit(0). Might repurpose
		self.Modes = {	"Title": 1,
						"Main_Menu": 2,
						"Cutscene": 3,
						"In-game scene": 4,
						"In-game": 5,
						"Pause": 6}
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
		
		self.Background = pygame.image.load("test_BG.png")
		self.Res = [500,500]
		self.bg = [random.randint(0,255) for i in range(3)]
		self.Clock = pygame.time.Clock()
		try:	self.Window = pygame.display.set_mode(self.Res)
		except Exception as E: print(E+":P")
		while(True):
			if(self.Mode == self.Modes["Title"]):
				pass
				
			if(self.Finished): return


			self.Clock.tick(10)
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
					print(event)
					if(event.type == pygame.QUIT): pygame.quit()
					if(event.type == pygame.KEYDOWN):
					#self.Finished = True
						if(event.key == pygame.K_ESCAPE):
							self.Finished = True
							pygame.quit()
							print("?")
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
							print("?")
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
					self.Window.fill(self.bg)
					self.Window.blit(pygame.transform.scale(self.Background,[500,500]),[0,0])
					self.QueryAll()
					self.mapDraw()
					self.physUpdate()
					self.Clock.tick(10)

			elif(self.Mode == self.Modes["Pause"]): pass
					
			pygame.display.update()
				
	def mapDraw(self):
			for i in range(len(self.Map) - 2): assert(len(self.Map[i]) == len(self.Map[i+1]))
			for i in range(len(self.Map)):
				for j in range(len(self.Map[0])):
					if(self.Map[i][j]):
						self.Window.blit(pygame.transform.scale(self.Sprites[self.Map[i][j]-1],self.zoom),[self.zoom[1]*j,self.zoom[0]*i])
				
	def physUpdate(self):
		for Creature in self.creatures:
			Creature.pos = [Creature.pos[i] + Creature.velocity[i] for i in range(2)]
			Creature.velocity = [Creature.velocity[i] + Creature.accel[i] for i in range(2)]
			Creature.accel = [Creature.accel[i] * Creature.airDense for i in range(2)]
			if(not (Creature.grounded or Creature.latched)):
				Creature.velocity[1] += 4.0
			if(Creature.grounded): Creature.velocity[0] = Creature.accel[0] = 0.0
			if(Creature.latched): Creature.velocity = Creature.accel = [0.0,0.0]
		
			envelopedSquares = True
			if(True):
				
				envelopedSquares = [[shDiv(Creature.pos[0],self.zoom[0]),shDiv(Creature.pos[1],self.zoom[1])]]
				if(envelopedSquares[0][0] != int(float(Creature.pos[0]+float(self.zoom[0]*Creature.dims[0]))/float(self.zoom[0]))):
					envelopedSquares.append([int(float(Creature.pos[0]+float(self.zoom[0]*Creature.dims[0]))/float(self.zoom[0])),envelopedSquares[0][1]])
				if(envelopedSquares[0][1] != int(float(Creature.pos[1]+float(self.zoom[1]*Creature.dims[1]))/float(self.zoom[1]))):
					for k in range(len(envelopedSquares)):
						envelopedSquares.append([envelopedSquares[k][0],int(float(Creature.pos[1]+float(self.zoom[1]*Creature.dims[1]))/float(self.zoom[1]))])
				for square in envelopedSquares:
					if(self.Map[square[1]][square[0]] == 1):
						Creature.velocity = [Creature.velocity[i]/3 for i in range(2)]
						Creature.pos = [Creature.pos[i] - Creature.velocity[i] for i in range(2)]
				if(envelopedSquares == []): break
				
		for Creature in self.creatures:
			for layer in Creature.spriteLayers:
				self.Window.blit(pygame.transform.scale(layer.Sheet, [a*self.SF for a in layer.sRes]),
				 [Creature.pos[i] + self.zoom[i]*Creature.sprOffset[i] for i in range(2)],(self.SF*10*Creature.frm,20*Creature.idx,self.SF*10,self.SF*20))
			pygame.draw.rect(self.Window,(0,0,0,0),[Creature.pos[0],Creature.pos[1],self.zoom[0]*Creature.dims[0],self.zoom[1]*Creature.dims[1]],1)
			Creature.frm = (Creature.frm + 1) % 9
			
	def QueryAll(self):
		for Creature in self.creatures:
			if(Creature.is_player):
				for event in pygame.event.get():
					if(event.type == pygame.KEYDOWN):
						if(event.key == pygame.K_UP):
							Creature.Response["UD"] = 1
						elif(event.key == pygame.K_DOWN):
							Creature.Response["UD"] = -1
						elif(event.key == pygame.K_LEFT):
							if(Creature.Response == 3): Creature.Response["LR"] = -2
							else: Creature.Response["LR"] = -1
						elif(event.key == pygame.K_RIGHT):
							if(Creature.Response == 3): Creature.Response["LR"] = 2
							else: Creature.Response["LR"] = 1
						elif(event.key == pygame.K_z): Creature.Response["Item"] = 1
						elif(event.key == pygame.K_x): Creature.Response["Item"] = 2
						elif(event.key == pygame.K_c): Creature.Response["Item"] = 3
						elif(event.key == pygame.K_v): Creature.Response["Item"] = 4
						elif(event.key == pygame.K_b): Creature.Response["Item"] = 5
						
						elif(event.key == pygame.K_a):
							if(Creature.Response["Point"] == 3): Creature.response["Point"] = 4
							elif(Creature.Response["Point"] == 7): Creature.response["Point"] = 6
							elif(Creature.Response["Point"] == 1): Creature.response["Point"] = 0
							else: Creature.Response["Point"] = 5

						elif(event.key == pygame.K_s):
							if(Creature.Response["Point"] == 5): Creature.response["Point"] = 6
							elif(Creature.Response["Point"] == 1): Creature.response["Point"] = 9
							elif(Creature.Response["Point"] == 3): Creature.response["Point"] = 0
							else: Creature.Response["Point"] = 8

						elif(event.key == pygame.K_d):
							if(Creature.Response["Point"] == 8): Creature.response["Point"] = 9
							elif(Creature.Response["Point"] == 3): Creature.response["Point"] = 2
							elif(Creature.Response["Point"] == 5): Creature.response["Point"] = 0
							else: Creature.Response["Point"] = 1

						elif(event.key == pygame.K_w):
							if(Creature.Response["Point"] == 5): Creature.response["Point"] = 4
							elif(Creature.Response["Point"] == 1): Creature.response["Point"] = 2
							elif(Creature.Response["Point"] == 8): Creature.response["Point"] = 0
							else: Creature.Response["Point"] = 3

						
						
			else: Creature.Query()
			Move = Creature.Response
			
			if(not (-2 <= Move["LR"] and Move["LR"] <= 2)): Move["LR"] = 0
			if(Move["LR"] == 2):	# Run right
				if(Creature.grounded): Creature.velocity[0] = (Creature.accelLR * Creature.maxRunVelo + Creature.velocity[0]) / 3.0
			if(Move["LR"] == 1):	# Walk right
				if(Creature.grounded): Creature.velocity[0] = (Creature.accelLR * Creature.maxWalkVelo + Creature.velocity[0]) / 3.0
				else: Creature.velocity[0] = (Creature.accelLR * Creature.maxAirVelo)
			if(Move["LR"] == 0):	# Idle
				if(Creature.grounded): Creature.velocity[0] = (Creature.velocity[0] * self.Slippery)
				else: Creature.velocity[0] = Creature.velocity[0] * Creature.airDense
			if(Move["LR"] == -1):	# Walk left
				if(Creature.grounded): Creature.velocity[0] = (-1 * Creature.accelLR * Creature.maxWalkVelo + Creature.velocity[0]) / 3.0
				else: Creature.velocity[0] = (-1 * Creature.accelLR * Creature.maxAirVelo)
			if(Move["LR"] == -2):	# Run left
				if(Creature.grounded): Creature.velocity[0] = (-1 * Creature.accelLR * Creature.maxRunVelo + Creature.velocity[0]) / 3.0
				
				
			if(Move["Item"] != 0):
				if(Move["Item"] == 1): self.effectQueue.append(self.weapons[0].primary)		# Primary attack with active weapon; usually a heavier attack
				if(Move["Item"] == 2): self.effectQueue.append(self.weapons[0].secondary)	# Secondary attack with active weapon; usually a quick jab
				if(Move["Item"] == 3):
					self.effectQueue.append(self.weapons[1].secondary) # Quick attack with secondary weapon when the primary weapon is two-handed; if both are one-handed or it is hybrid, a primary attack. If a focus weapon, it is the tertiary attack.
				if(Move["Item"] == 4):
					pass	# Secondary attack from second weapon when dual-wielding or hybridized. If focus, slot 4.
				if(Move["Item"] == 5):
					pass # For using your active utility gear: wings, industrial battery, climbing gear, et cetera.
				if(Move["Item"] == 6): # For using some trinket currently active. A magic gem, grenade, or network packet capturer, something of the sort.
					pass
				if(Move["Item"] == 7):
					pass # If the square has a creature or item on it, you can interact with it.
				if(Move["Item"] == 8):
					pass # Moving items around.
				
			if(Creature.Response["Point"]): Creature.pointdir = Creature.Response["Point"]
			

	def Learn(self): return

	def Dialogue(self,pause=1):
		if(pause == 1):
			pass


class Creature:
	def __init__(self,Sim,Head=Soviet_Head,Body=Trenchcoat,Legs=Generic_Pants,is_player = False):
		self.Sim = Sim
		self.is_player = is_player
		
		self.Response = {	"LR": 0,
				   			"UD": 0,
				   			"Move": 0,
				   			"Item": 0,
				   			"Point": 0,
				   			"Signal": 0,
				   			"Itemch": 0,
						}
		
		self.spriteLayers = [Head,Body,Legs]
		
		self.HP = 1.0
		
		self.dims = [0.5,1.5]
		self.sprOffset = [-0.2,-0.3]
		
		self.pos = [200,50]
		self.velocity = [0,0]
		self.accel = [0,0]
		
		self.frm = self.idx = 0
		
		self.maxWalkVelo = 8.0
		self.maxRunVelo = 32.0
		self.maxAirVelo = 0.8
		
		self.accelLR = 1.8
		self.Slippery = 0.8
		self.airDense = 0.95
		
		self.grounded = False
		self.latched = False
		
		self.Offense_Coeff = 0.5
		self.Combative_Coeff = 0.5
		self.Lethal_Coeff = 0.5
		self.Careful_Coeff = 0.5
		
	def Query(self): return [str(i) for i in [self.Move(),self.itemAction(),self.Point(),self.Aerial(),self.Signal()]]
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

"""
This is how every frame decision is to be made. The decisions made will be abstracted to higher level decisions to target a creature, avoid dangers, et cetera. The goals chosen will be what the neural network is taught to recognize and therefore the specific creature's approach to any given goal will be trained, but their temperament, values, and situational awareness will affect these decisions, giving every individual in this game a unique personality and fighting style, instead of a world of hats situation.

Category: common

0	->	Idle/no new action

Category: Attack/item interaction

1	->	Melee attack
2	->	Ranged attack
3	->	Shield attack
4	->	Misc attack
5	->	Open items/configure items
6	->	Wall latch, bar hang, anchor, etc.; requires that a creature has the ability either through equipment or a class feature, for which a check will be made.
7	->	Environment interaction

Category: Movement L/R

1	->	Lean/glide/crawl L/R
2	->	Accelerated/assisted motion L/R

Category: Movement U/D

1	->	Normal jump/float
2	->	Item-assisted lift/descend
2	->	Descend/crouch

Category: Point

1	->	Point item
2	->	Look
3	->	Look and point


Category: Communication:

1	->	Sub-category: Communication/signal: General
_________________________
	1	->	Signal 1
	2	->	Signal message 2
	. . .
	n	->	Signal n

2	->	Sub-category: Communication/signal: Kin-exclusive
_________________________
	1	->	Signal 1
	2	->	Signal message 2
	. . .
	n	->	Signal n

3	->	Sub-category: Communication/signal: Environment trigger
_________________________
	1	->	#TRIGGER 1
	2	->	#TRIGGER 2
	. . .
	n	->	Signal n
_________________________

Category: Evaluate Creature
1	->	Increase reward for Kill/Protection of creature X
2	->	Increase reward for Capture/Preservation of creature X
3	->	Increase perception of danger/safety for creature X

===============================================================
===============================================================
===============================================================

Now the goals. If these change during the game, as they will based on new information they get, they may be trained to ignore the change, or to plan to adapt and be indecisive.

However, these are mostly static. The changes might be when a creature realizes a so-called ally turns out to be hostile or traitorous, vice versa, if their leader signals to surrender, or they realize their death is imminent and so decide to maximize destruction of the enemy.

Tactical attributes:

Pacifist --- Conflict-assertive spectrum
	1.0: Kill the enemy, cut up and freeze their children, eat their pets, and shoot the messenger
	0.9: Kill the enemy
	0.8: Kill the enemy, but spare those worthy of it
	0.7: Kill the enemy if reason otherwise exists to do so
	0.6: Use force to defuse conflicts and protect your interests
	0.5: Defer to the other tactical aspects of the situation
	0.4: Compromise to disarm opponents initially
	0.3: Try to resolve the conflict without killing if possible, but prioritize the innocent.
	0.2: De-escalate the situation if it can be salvaged, even at great personal cost.
	0.1: Only kill the specific individuals responsible for the conflict
	0.0: Kill no one, even if they ate your cat and are swinging an axe at you
	
The attack mechanics and weapons will allow for lethal and nonlethal fighting techniques. If an enemy is hated more than the pacifistic threshold of this creature, the creature's attacks will attempt to kill.

Collateral damage admission: High --- Low

	1.0: Let me cut you a deal: your king's severed head for our king's heart and liver... it's getting time for revolution anyway...
	0.0: Just because I'm a bit schizophrenic doesn't mean my friends are any less important.

Just as you might imagine. Allies are always important. Sometimes you have to choose between launching an AOE that can take out seven enemies and one ally at once, and that's a judgment call you have to make.



	
This skews the creature to prefer either mounting an assault or defending allies/weak points when called to participate in the fight. In general, defense will be incentivized to keep damage from valued entities, though keeping damage from teammates or allies in any capacity counts as well, and even aggressive creatures assist attackers when convenient.

Pragmatic --- Unfettered

	1.0: Being possessed is no excuse to be somewhere you aren't supposed to be... smh
	0.9: Let the police handle this. Your life is more valuable.
	0.8: Would anything important break if we lose? ... No, I said something IMPORTANT.
	0.7: Am I necessary here?
	0.6: Am I useful here?
	0.5: This wasn't part of the job description! What am I supposed to do?
	0.4: Sigh... I sure hope this will be worth it.
	0.3: My buddies rely on me to help them.
	0.2: I wouldn't give my credit card and laptop to a mugger as soon as asked for them. Perhaps size them up first... and check if they actually have weapons on them. Even if so, perhaps I can use my belt to gain the upper hand. Oh well, I'll figure it out.
	0.1: Terrorism and war thrives on people giving in to threats. Better to die for a greater cause than to save your life enabling evil.
	0.0: Did you just assume my gender?!

This describes, when called upon, whether aggressive or defensive, how strongly their assault or protective instincts go, pit against the impulse to retreat. In other words, if a defensive target is valuable enough, or the object of the conflict valuable enough, it will involve even the more pragmatic creatures, who only care about bettering their own situation, whereas less high stakes conflicts will generally only take hold on the hard-headed among them.

So, let's imagine a creature has:
Pacifist (0.2)
Unfettered (0.1)
Assault (0.8)

This creature would generally use nonlethal means to subdue an adversary, to the bitter end, with great offensive energy. If the adversary, however, turns out to make a great effort to extend a truce, the situation is extremely hopeless, or the only thing the creature has to do right now is defensive in nature, they would take on different behaviours to fit that.

Now comes the assessment of a goal. The following are examples of goals:

-- Attack target
-- Make sure attack misses target
-- Defend target
-- Evade target
-- Move to location
-- Area denial

With few exceptions, friendly fire does not exist. This brings us to the inverted equivalent of goals: constraints. These are penalties for something that happens which is to be used in training.

-- Ally/target dies
-- Ally/target is attacked
-- Ally/target begins to turn on you

-- Creature takes damage
-- Creature dies

-- Attack misses target

-- Mission objective regresses

So naturally, the temperament scores will factor into goals. for example, if an attack misses, the attacking target goal will penalize actions leading up to it, but not by much if, for example, the creature was defensive to begin with, their primary goal assigned to them was area denial (thus may have been successful), et cetera.


Due to how many parameters exist, it is tempting to wonder whether this will be an issue when training. However, the machine learning of a platformer is necessarily slow due to the real-time simulation slowing generation of training data. Higher specificity of training takes advantage of this effect, so more learning occurs per frame of runtime.

When the game is run, only a few important goals will actually be chosen at a time per creature, and may periodically choose random side goals to check up on; additionally, communication can occur when a creature notices a significant assistance or hindrance due to an ally's action, which may not necessarily have served the creature's primary interest but had a serendipidous effect.

The inputs to these problems should be simple as possible while encompassing all relevant information. Therefore, all creatures and blocks within view of a creature may be factored into a creature 

To avoid overtraining, a creature may be placed in different environments or with different weapons, et cetera, to successfully navigate variance. However, overtraining may be also used strategically, as for a creature to be unfamiliar with certain fighting styles, environments, and dangers, may be intentionally added to provide fallibility.

Another aspect of the training may be for the creature to be aware of specific weapons and effects affect their course of action, perhaps how to aim guns with different bullet patterns and trajectories.

"""
