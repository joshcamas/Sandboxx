import numpy as np
import random
import time
import logging

import sandboxx.tiletypes as tiletypes

class World():
	"""
	The physical representation of the game. Holds the actual "tiledata"
	
	"""
	def __init__(self,gamescene):
		self.gamescene = gamescene
		self.size = self.gamescene.application.screensize
		self.checkerboard = np.row_stack(self.size[1]*(np.r_[ self.size[0]*[0,1] ], np.r_[self.size[0]*[1,0]]))
		
	def create(self):
		"""
		Initializes world buffer
		"""
		
		self._buildtiletypes()
		self.tiledata = np.zeros(self.size,np.int8)
		
		#SAND BLOCK
		self.drawblock(10,10,10,10,1)
		
		#STEEL
		self.drawfloor(40,3,self.tiledata)
		self.drawwall(0,3,self.tiledata)
		self.drawwall(self.size[0]-1,3,self.tiledata)
	
	def drawblock(self,x,y,width,height,id,tiledata=None):
		"""
		Draws a block onto the world
		"""
		if tiledata is None:
			tiledata = self.tiledata
		
		for tx in range(width):
			for ty in range(height):
				
				xx = x+tx
				yy = y+ty
				
				if xx >= 0 and xx < self.size[0] and yy >= 0 and yy < self.size[1]:
					tiledata[x+tx][y+ty] = id
		
	def drawfloor(self,y,id,tiledata=None):
		"""
		Draws a floor onto the world
		"""
		if tiledata is None:
			tiledata = self.tiledata
		
		for i in range(0,self.size[0]):
			
			if i >= 0 and i < self.size[0] and y >= 0 and y < self.size[1]:
				tiledata[i][y] = id
		
	def drawwall(self,x,id,tiledata=None):
		
		if tiledata is None:
			tiledata = self.tiledata
		
		for i in range(0,self.size[1]):
			
			if x >= 0 and x < self.size[0] and i >= 0 and i < self.size[1]:
				tiledata[x][i] = id
	
	def get_tile_type_id(self,name):
		for i in range(len(self.names)):
			if self.names[i] == name:
				return i
				
		return -1
		
	def _buildtiletypes(self):
		"""
		Hard coded list of tile types
		"""
		
		self.tiletypes = []
		self.names = []
		self.keys = [-1 for x in range(10)]
		self.shiftkeys = [-1 for x in range(10)]
		
		self._addtile(tiletypes.AirTile(),"air")
		self._addtile(tiletypes.SandTile(),"sand", key=3)
		self._addtile(tiletypes.SmokeTile(),"smoke")
		self._addtile(tiletypes.SolidTile((100,100,100)),"steel", key=1)
		self._addtile(tiletypes.OilTile(),"oil", key=6)
		self._addtile(tiletypes.FireTile(),"fire", key = 1,keyshift=True) 
		self._addtile(tiletypes.WaxTile(),"wax", key=4) 
		self._addtile(tiletypes.MeltedWaxTile(),"meltedwax") 
		self._addtile(tiletypes.ElectricTile(),"electricity", key = 2,keyshift=True) 
		self._addtile(tiletypes.WireTile(),"wire", key = 5) 
		self._addtile(tiletypes.PoweredWireTile(),"poweredwire") 
		self._addtile(tiletypes.SeedTile(),"seed", key = 3,keyshift=True) 
		self._addtile(tiletypes.PlantTile(),"plant") 
		self._addtile(tiletypes.DeadPlantTile(),"deadplant")
		self._addtile(tiletypes.WaterTile(),"water", key = 7)
		self._addtile(tiletypes.WoodTile(),"wood", key = 2)
		self._addtile(tiletypes.BurningWoodTile(),"burningwood")
		self._addtile(tiletypes.CloudTile(),"cloud", key = 4,keyshift=True)
		
		for i in range(0,len(self.tiletypes)):
			self.tiletypes[i].setup(i,self.tiletypes,self,self.size)
		
		self.nulltile = tiletypes.NullTile()
		self.nulltile.setup(-1,self.tiletypes,self,self.size)
		
	def _addtile(self,tile,name,key = -1,keyshift= False):
		self.names.append(name)
		
		tile.key = key
		tile.keyshift = keyshift
		
		self.tiletypes.append(tile)
		
		if key is not -1 and key >= 0 and key <= 9:
			
			if keyshift:
				self.shiftkeys[key] = len(self.tiletypes)-1
			else:
				self.keys[key] = len(self.tiletypes)-1
		
	def tick(self):
		"""
		Triggers a world "tick", which updates all tiles
		"""
		
		#Generate random direction
		if random.randint(0,1) == 0:
			self.randdir = -1
		else:
			self.randdir = 1
			
		newtiledata = np.zeros(self.size,np.int8)
		
		for y in range(self.size[1]):
			
			for x in range(self.size[0]):

				yy = self.size[1] - y - 1
				
				#Flip x direction
				if self.randdir == -1:
					xx = self.size[0] - x - 1
				else:
					xx = x
				
				id = self.tiledata[xx][yy]
				
				if id != 0:
					self.tiletypes[id].preupdatetile(xx,yy,self.tiledata,newtiledata)
					self.tiletypes[id].updatetile(xx,yy,self.tiledata,newtiledata)
			
			#Flip random direction
			self.randdir = -self.randdir
			
		del self.tiledata
		#Apply new tiledata
		self.tiledata = newtiledata

