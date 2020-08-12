import pygame, Effects,loadedDefaults, Items

class spriteSheet:
	def __init__(self,pyGLayer,sRes = [1920,1080],frmDims = [10,10]):
		self.sRes = sRes
		self.Sheet = pygame.image.load(pyGLayer)
		
class Item(spriteSheet):
	def __init__(self,pyGLayer,sRes = [1920,1080]):
		self,sRes = sRes
		self.Sheet = pygame.image.load(pyGLayer)

class HumanoidSprites(spriteSheet):
	def __init__(self, pyGLayer,sRes = [1920,1080],frmDims = [10,10]):
		self.Sheet = pygame.image.load(pyGLayer)
		self.sRes = sRes
		self.Animations = {
		"Walk": 0,
		"Jump" : 1,
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
		


def shDiv(a,b): return int(float(a)/float(b))

def step(x,a=1,b=-1):
	if(x > 0): return a
	return b

humanoidSprites = {
	"Trenchcoat": pygame.image.load("Trenchcoat.png"),
	"Generic_Pants": pygame.image.load("Generic_pants.png"),
	"Soviet_Head": pygame.image.load("Head.png")
}

a = [0,0]

DefaultTextbox = pygame.image.load("DF_TB.png")
NPC_MEME = pygame.image.load("NPC.jpg")
NPC_MEME_ANGRY = pygame.image.load("NPC_Angry.jpeg")
		
Trenchcoat = HumanoidSprites("Trenchcoat.png")
Generic_Pants = HumanoidSprites("Generic_pants.png")
Soviet_Head = HumanoidSprites("Head.png")

testEffect = Effects.Effect(None,False, lambda f:exec("""
f[1].Mode = f[1].Modes["Script"]
f[1].toggle0 = 0
f[1].Current = None
print(f)
f[1].activeScript = [
	["Talk",loadedDefaults.DefaultTextbox,loadedDefaults.NPC_MEME,"?"],
	["Talk",loadedDefaults.DefaultTextbox,loadedDefaults.NPC_MEME_ANGRY,"!"],
	["Action","Return"]]
	"""),None,endCondition = lambda f:1 )


Grenade = Items.GameItems["Grenade"]()
Grenade.pos = [300,250]
