import Effects, loadedDefaults

DefaultItemParams = {
		"Weight": 1.0,
		"Pos": None,
		"velocity": None,
		"holdSprites": None,
		"Sheet" : None,
		"objBound": None,
		"Interact": {
			"Throw": lambda f: exec("""

f[0]["self"].Pos = f["Holder"].pos
f[0]["Holder"].Items.remove(f[0]["self"])
f[0]["self"].velocity = f[1]

			"""),
			"Take": None,
			"Release": None,
			"Clobber": None,
			"Recharge": None,
			"Equip": None,
			"Put-away": None,
			"Unique-action-0": None,
			"action-1": None,
			"Unique-action-2": None,
			"Unique-action-3": None
		}
}

class Item:
	def __init__(self,ItemParams=DefaultItemParams):
			self.Params = ItemParams
			print(self.Params)
			self.Params["self"] = self
			self.velocity = [0,0]
			self.accel = [0,0]
			self.airDense = self.Params["airDense"]
			self.grounded = self.latched = False
			self.dims = self.Params["dims"]
			self.spriteLayers = self.Params["spriteLayers"]
			self.sprOffset = self.Params["sprOffset"]
			self.frm = self.Params["frm"]
			self.idx = self.Params["idx"]

		
GameItems = {
	"Grenade": 	lambda:Item({
		"Interact": {
			"Throw": lambda f: exec("""
#f[1]["Sim"]
#f[0].objBound = True
f[0].velocity = [f[1]["Holder"].Strength * f[2] * math.cos(math.pi * ["Holder"].Point),
				f[1]["Holder"].Strength * f[2] * math.sin(math.pi * f["Holder"].Point)]
f[0].pos = f[1]["Holder"].pos


			"""),
			
		},
		"Effects": [],
		"self": None,
		"airDense": 0.97,
		"dims": [0.25,0.25],
		"sprOffset": [0,0],
		"frm": 0,
		"idx": 0,
		"spriteLayers": [loadedDefaults.spriteSheet("Grenade.png",frmDims = [10,10])]
	}),
	"Grenade-Launcher": lambda:Item({
		"Weight": 0.35,
		"Interact": {
			"action-1": lambda f:exec("""
f[1].itemQueue.append([GameItems["Grenade"],[300,250]])
#f[1].itemQueue[-1].pos = [300,250]
			"""),
		},
			
		"Effects": [],
		"self": None,
		"airDense": 0.97,
		"dims": [0.25,0.25],
		"sprOffset": [0,0],
		"spriteLayers": [loadedDefaults.spriteSheet("Grenade.png",frmDims = [10,10])],
		"frm": 0,
		"idx": 0
	})
}
