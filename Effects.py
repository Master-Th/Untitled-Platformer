import numpy

class Item:
	def __init__(self,Weight,HP,interactEffect,Effects):
		self.Weight = Weight
		self.Actions = Actions
		
class Effect: # Within the context of creature and weapon interactions with each other and the environment
	def __init__(self,Sim,itemSpawns,effect,zone,splash=0,stack=1,boundToObject=None,endCondition=None,effectConfig=None,setup=None):
		self.Sim = Sim
		self.itemSpawns = itemSpawns
		self.effect = lambda args: effect(args)
		self.zone = lambda a: zone(self,a)
		self.endCondition = lambda self: endCondition
		self.splash = splash
		self.stack = stack
		self.boundToObject = boundToObject
		self.endCondition = endCondition
#		self.powerString = powerString
		self.setup = setup
		
	def Effect(self, args): self.effect([self]+args)

def Explode_map(a,b=None):
	if(not B):
		if(not a.effectConfig):
			a.effectConfig = {"Damage":"idk"}
		self.Animation = "Detonation"
		for i in range(0,a.effectConfig["bRange"] - 1):
			for j in range(0,a.effectConfig["bRange"]-1):
				try:
					pass
#					a.Sim.effectMap[i][j].append(a.)
				except: pass
	else:
		if(((b[0]-a[0])**2+(b[1]-a[1])**2) < a.effectConfig["sqRange"]**2):
			self.Sim.adjudicate(b,a.effect)
			
def Explode(a,b):
	if(b): return



#Explode_distance = "F"
#Explode_Effect = Effect(None,Explode_map,Explode_distance,1,None,None,None,splash=numpy.inf)

#def grenadeLaunch(a):
	#if(a == 1):
		#self.Sim.items.add(Item(0.1,0.01,lambda b: Explode))

#Grenade_launcher = Item(0.35,4.8,{"Primary": lambda a: grenadeLaunch})
