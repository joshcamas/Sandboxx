import random

class TileType():
	"""
	A specific 'material type' for a tile
	"""
	
	def __init__(self):
		
		self.is_air = False
		self.is_solid = False
		self.is_electric = False
		self.is_burn = False
		self.is_meltable = False
	
	def setup(self,id,tiletypes,world,worldsize):
		"""
		Set important variables, runs automatically
		"""
		
		self.id = id
		self.tiletypes = tiletypes
		self.worldsize = worldsize
		self.world = world
		
		self.width = self.worldsize[0]
		self.height = self.worldsize[1]
    
	def preupdatetile(self,x,y,read,write):
		self._x = x
		self._y = y
		self._read = read
		self._write = write
        
	def updatetile(self,x,y,old,new):
		"""
		Updates a specific tile
		"""
		
		new[x][y] = old[x][y]
		pass
	
	def color(self,x,y,tiledata):
		"""
		Returns color of tile. Return 0 for no color
		"""
		
		return 0
	
	def _foreach_neighbor(self,x,y,read,function):
		"""
		Loops neighbors
		
		PARAMETERS
		----------
		x: x position of tile
		y: y position of tile
		read: read tiledata
		function: function to run: function(x,y,id,type)
		"""
		
		#DOWN
		if y < self.height-1:
			function(x,y+1,read[x][y+1],self.gettype(x,y+1,read))

		#UP
		if y > 0 and self.gettype(x,y-1,read).is_burn == True:
			function(x,y-1,read[x][y-1],self.gettype(x,y-1,read))
			
		#RIGHT
		if x < self.width-1 and self.gettype(x+1,y,read).is_burn == True:
			function(x+1,y,read[x+1][y],self.gettype(x+1,y,read))
			
		#LEFT
		if x > 0 and self.gettype(x-1,y,read).is_burn == True:
			function(x-1,y,read[x-1][y],self.gettype(x-1,y,read))
		
	
	def _bool_neighbor_id(self,x,y,id,read,ignore_down=False,ignore_up=False,ignore_left=False,ignore_right=False):
		"""
		Returns if at least one neighbor is a certain id
		"""
		
		hit,xx,yy = self._check_neighbor_id(x,y,id,read,ignore_down,ignore_up,ignore_left,ignore_right)
		
		return hit
		
	def _check_neighbor_id(self,x,y,id,read,ignore_down=False,ignore_up=False,ignore_left=False,ignore_right=False):
		"""
		Returns if at least one neighbor is a certain id,alongside x and y coordinates
		
		RETURNS
		--------
		Success,neighbor x, neighbor y
		"""
		
		#DOWN
		if y < self.height-1 and read[x][y+1] == id and ignore_down == False:
			return True,x,y+1

		#UP
		if y > 0 and read[x][y-1] == id and ignore_up == False:
			return True,x,y-1
			
		#RIGHT
		if x < self.width-1 and read[x+1][y] == id and ignore_right == False:
			return True,x+1,y
			
		#LEFT
		if x > 0 and read[x-1][y] == id and ignore_left == False:
			return True,x-1,y
		
		return False,0,0
		
	def _check_flammable(self,x,y,read):
		"""
		Checks if any neighbors are flammable, returns the value,x,y coordinates
		"""
		
		#DOWN
		if y < self.height-1 and self.gettype(x,y+1,read).is_burn == True:
			return True,x,y+1

		#UP
		elif y > 0 and self.gettype(x,y-1,read).is_burn == True:
			return True,x,y-1
			
		#RIGHT
		elif x < self.width-1 and self.gettype(x+1,y,read).is_burn == True:
			return True,x-1,y
			
		#LEFT
		elif x > 0 and self.gettype(x-1,y,read).is_burn == True:
			return True,x+1,y
		else:
			return False,0,0
		
	def _check_electric(self,x,y,read):
		"""
		Checks if any neighbors are electric, returns the value,x,y coordinates
		"""
		
		#DOWN
		if y < self.height-1 and self.gettype(x,y+1,read).is_electric == True:
			return True,x,y+1

		#UP
		elif y > 0 and self.gettype(x,y-1,read).is_electric == True:
			return True,x,y-1
			
		#RIGHT
		elif x < self.width-1 and self.gettype(x+1,y,read).is_electric == True:
			return True,x-1,y
			
		#LEFT
		elif x > 0 and self.gettype(x-1,y,read).is_electric == True:
			return True,x+1,y
		else:
			return False,0,0
			
	def gettype(self,x,y,tiledata):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return self.world.nulltile
		
		return self.tiletypes[tiledata[x][y]]

class NullTile(TileType):
	"""
	A tile type that counts as null
	"""
	
	def __init__(self):
		TileType.__init__(self)
		self.nullcolor = (1,1,1)
		
	def color(self,x,y,tiledata):
		return self.nullcolor;
		
class AirTile(TileType):
	"""
	A tile type that is absolutely nothing
	"""
	
	def __init__(self):
		TileType.__init__(self)
		self.aircolor = (0,0,0)
		
		self.is_air = True
		
	def color(self,x,y,tiledata):
		return self.aircolor;
		
class SolidTile(TileType):
	"""
	A tile type that does nothing in particular
	"""
	
	def __init__(self,color):
		TileType.__init__(self)
		self.tilecolor = color
		
		self.is_solid = True
		
	def color(self,x,y,tiledata):
		return self.tilecolor

class SandTile(TileType):
	"""
	A tile type that falls and reacts to solid objects, piling up
	"""
	
	def __init__(self):
		TileType.__init__(self)
		self.tilecolor = (150,145,91)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		"""
		Updates a specific tile
		"""
		
		if y < self.height-1:
				
			#DOWN
			if self.gettype(x,y+1,read).is_solid == False:
				#MOVE 
				write[x][y+1] = self.id

			#LEFT DIAGONAL
			elif x < self.width-1 and self.gettype(x+1,y+1,read).is_solid == False:
				#MOVE 
				write[x+1][y+1] = self.id
		
			#RIGHT DIAGONAL
			elif x > 0 and self.gettype(x-1,y+1,read).is_solid == False:
				#MOVE 
				write[x-1][y+1] = self.id
				
			else:
				write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor

class OilTile(SandTile):
	"""
	A tile type that is essentially flammable sand
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (100,0,100)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		burn,xx,yy = self._check_flammable(x,y,read)
		
		#Turn into fire
		if burn:
			write[x][y] = self.world.get_tile_type_id("fire")
			
		#Otherwise we act like sand
		else:
			SandTile.updatetile(self,x,y,read,write)
		
	def color(self,x,y,tiledata):
		return self.tilecolor
		
class WoodTile(TileType):
	"""
	A solid tile type that turns into burning wood when touching burners
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (39,28,16)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		#Chance
		burn,xx,yy = self._check_flammable(x,y,read)
		
		#Turn into burningwood
		if burn:
			write[x][y] = self.world.get_tile_type_id("burningwood")
			return
			
		write[x][y] = self.id
		
	def color(self,x,y,tiledata):
		return self.tilecolor
		
class BurningWoodTile(TileType):
	"""
	A solid tile type has a chance of turning into fire
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (29,18,6)
		
		self.is_flammable = True
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		#Chance
		if random.randint(0,4) == 0:
			write[x][y] = self.world.get_tile_type_id("fire")
			return
				
		write[x][y] = self.id
		
	def color(self,x,y,tiledata):
		return self.tilecolor
		
		
class WaxTile(TileType):
	"""
	A tile type that is solid, and then turns into MeltedWaxTile when heated
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (130,130,100)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		burn,xx,yy = self._check_flammable(x,y,read)
		
		#Turn into melted wax
		if burn:
			write[x][y] = self.world.get_tile_type_id("meltedwax")
			
		#Otherwise do nothing
		else:
			write[x][y] = self.id
		
	def color(self,x,y,tiledata):
		return self.tilecolor

class MeltedWaxTile(SandTile):
	"""
	A tile type that acts like sand, but has a chance to spread or turn into wax again
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (113,105,78)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		#Chance of spreading to another candle tile
		if random.randint(0,2) == 1:
			found,nx,ny = self._check_neighbor_id(x,y,self.world.get_tile_type_id("wax"),read)
			
			if found:
				write[nx][ny] = self.id
		
		#Chance of turning into back into wax if tile underneeth is solid
		"""
		under_mwax = y < self.height-1 and read[x][y+1] == self.id
		under_wax = y < self.height-1 and read[x][y+1] == self.world.get_tile_type_id("wax")
		under_solid = y < self.height-1 and self.gettype(x,y+1,read).is_solid
		
		if random.randint(0,5) == 1 and under_mwax == False and under_wax == False and under_solid:
			write[x][y] = self.world.get_tile_type_id("wax")
		"""
		#Chance of physics
		if random.randint(0,6) == 0:
			SandTile.updatetile(self,x,y,read,write)
		else:
			write[x][y] = self.id
				
	def color(self,x,y,tiledata):
		return self.tilecolor
		
		
class FireTile(TileType):
	"""
	A tile type that goes up, and turns into smoke if it has no floor
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (255,69,0)
		
		self.is_burn = True
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		nothing_under = y < self.height-1 and self.gettype(x,y+1,read).is_solid == False
		no_fire_above = y > 0 and self.gettype(x,y-1,read).id != self.id
		
		#Turn into smoke
		if nothing_under and no_fire_above:
			write[x][y] = self.world.get_tile_type_id("smoke")
			return
		
		#Clear
		if y == 0:
			write[x][y] = 0
			return
		
		#Chance to fade away
		if random.randint(0,8) == 1:
			write[x][y] = 0
			
		elif self.gettype(x,y-1,read).is_solid == False:
			write[x][y-1] = self.id
			
		else:
			write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor

class ElectricTile(TileType):
	"""
	A tile type that is electric and a burner and has a chance to move or die
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (255,255,0)
		
		self.is_burn = True
		self.is_electric = True
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		if random.randint(0,3) == 1:
			write[x][y] = 0
			
		else:
			write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor

class WireTile(TileType):
	"""
	A tile type that turns into a PoweredWireTile when electricity hits it
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (0,40,0)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		electric,xx,yy =  self._check_electric(x,y,read)
		
		if electric:
			write[x][y] = self.world.get_tile_type_id("poweredwire")
			
		else:
			write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor

class PoweredWireTile(TileType):
	"""
	A tile type that emits electricity, and has a chance to 
	turn back into wire, making a sparky look
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (0,100,0)
		
		self.is_electric = True
		self.is_burn = True
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		#Chance to fade away
		if random.randint(0,3) > 0:
			write[x][y] = self.world.get_tile_type_id("wire")
		
		else:
			write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor

class CloudTile(TileType):
	"""
	A tile type that drops rain sometimes
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (100,100,100)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		#Chance to rain
		if y < self.height-6 and random.randint(0,30) == 0:
			
			hit = False
			
			for i in range(5):
				if self.gettype(x,y+i+1,read).is_solid:
					hit = True
					break
			
			if not hit:
				write[x][y+i+1] = self.world.get_tile_type_id("water")
		
		#If alone, die
		if self._bool_neighbor_id(x,y,self.id,read) == False:
			return
		
		rand = random.randint(0,150)
		
		#Chance to move up
		if y > 0 and rand < 5:
			if self.gettype(x,y-1,read).is_solid == False:
				write[x][y-1] = self.id
				return
				
		#Chance to move down
		if y < self.height and rand > 5 and rand < 10:
			if self.gettype(x,y+1,read).is_solid == False:
				write[x][y+1] = self.id
				return
		
		#Chance to move left
		if x > 0 and rand > 10 and rand < 15:
			if self.gettype(x-1,y,read).is_solid == False:
				write[x-1][y] = self.id
				return
		
		#Chance to move right
		if x < self.width and rand > 15 and rand < 20:
			if self.gettype(x+1,y,read).is_solid == False:
				write[x+1][y] = self.id
				return
				
				
		write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor


class SeedTile(TileType):
	"""
	A tile type that turns into a plant
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (173,115,53)
		self.is_solid = True

	def updatetile(self,x,y,read,write):
		
		plantid = self.world.get_tile_type_id("plant")
		waterid = self.world.get_tile_type_id("water")
		
		#If on ground, do nothing until water touches
		if y < self.height-1 and y > 0 and self.gettype(x,y+1,read).is_solid and self.gettype(x,y+1,read).id != self.id:
			
			neighbor_is_seed = self._bool_neighbor_id(x,y,self.id,read)
			neighbor_is_plant = self._bool_neighbor_id(x,y,plantid,read)
			neighbor_is_water = self._bool_neighbor_id(x,y,waterid,read)
			
			if not neighbor_is_seed and not neighbor_is_plant:
				
				if neighbor_is_water:
					write[x][y] = plantid
				else:
					write[x][y] = self.id
				return
				
			"""
			neighbor_is_seed,xx,yy = self._check_neighbor_id(x,y,self.id,read)
			neighbor_is_plant,xx,yy = self._check_neighbor_id(x,y,plantid,read)
			
			#Make sure there are no plants or seeds nearby
			if neighbor_is_seed == False and neighbor_is_plant == False:
				#Random chance
				if random.randint(0,5) > 0:
					write[x][y] = plantid
					return
			"""
		
		#Chance to fade away
		if random.randint(0,6) == 0:
			write[x][y] = 0
			
			
		#Fall down
		elif y < self.height-1 and not self.gettype(x,y+1,read).is_solid:
			#MOVE 
			write[x][y] = 0
			write[x][y+1] = self.id
		else:
			write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor

class DeadPlantTile(SandTile):
	"""
	Tile that falls like sand and dies eventually
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (50,50,16)
		
		self.is_solid = True
	
	
	def updatetile(self,x,y,read,write):
		#Chance to fade away
		if random.randint(0,10) == 0:
			write[x][y] = 0
		else:
			SandTile.updatetile(self,x,y,read,write)
			
class PlantTile(TileType):
	"""
	A tile type that grows up
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (0,100,0)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		burn,xx,yy = self._check_flammable(x,y,read)
		
		#Turn into fire
		if burn:
			write[x][y] = self.world.get_tile_type_id("fire")
			return
		
		#No support, so turn into dead plant
		if self.gettype(x,y+1,read).is_solid == False:
			leftair = self.gettype(x-1,y+1,read).is_solid == False
			rightair = self.gettype(x+1,y+1,read).is_solid == False
			
			if leftair and rightair:
				write[x][y] = self.world.get_tile_type_id("deadplant")
				return
		
		#Suck up nearby water
		
		nearbywater,wx,wy = self._check_neighbor_id(x,y,self.world.get_tile_type_id("water"),read)
		
		if nearbywater:
			write[wx][wy] = 0
		
		
		#Cannot grow anymore
		if y == 0:
			write[x][y] = self.id
			return
		
		#Grow Up
		if random.randint(0,30) == 0:
			if self.gettype(x,y-1,read).is_solid == False:
				
				#Area around this spot should be plant free, except under
				n,xx,yy = self._check_neighbor_id(x,y-1,self.id,read,ignore_down=True)
				
				if n == False:
					write[x][y-1] = self.id
					write[x][y] = self.id
					return
				
		#Grow diagonal left
		elif random.randint(0,90) == 0:
			if self.gettype(x-1,y-1,read).is_solid == False:
				
				#Area around this spot should be plant free
				n,xx,yy = self._check_neighbor_id(x-1,y-1,self.id,read)
				
				if n == False:
					write[x-1][y-1] = self.id
					write[x][y] = self.id
					return
		
		#Grow diagonal right
		elif random.randint(0,90) == 0:
			if self.gettype(x+1,y-1,read).is_solid == False:
				
				#Area around this spot should be plant free
				n,xx,yy = self._check_neighbor_id(x+1,y-1,self.id,read)
				if n == False:
					write[x+1][y-1] = self.id
					write[x][y] = self.id
					return
				
		write[x][y] = self.id


	def color(self,x,y,tiledata):
		return self.tilecolor
		
		
class SmokeTile(TileType):
	"""
	A tile type that goes up and eventually fades
	"""
	
	def __init__(self):
		SandTile.__init__(self)
		self.tilecolor = (50,50,50)
		
		self.is_solid = True
	
	def updatetile(self,x,y,read,write):
		
		#Clear
		if y == 0:
			write[x][y] = 0
			return
		
		#Chance to fade away
		if random.randint(0,5) == 1:
			write[x][y] = 0
			
		#UP
		elif self.gettype(x,y-1,read).is_solid == False:
			write[x][y-1] = self.id
			
		#LEFT DIAGONAL
		elif x > 0 and self.gettype(x-1,y-1,read).is_solid == False:
			write[x-1][y-1] = self.id
			
		#RIGHT DIAGONAL
		elif x < self.width and self.gettype(x+1,y-1,read).is_solid == False:
			write[x+1][y-1] = self.id
			
		else:
			write[x][y] = self.id

	def color(self,x,y,tiledata):
		return self.tilecolor
		
class WaterTile(TileType):
	"""
	A tile type that falls and reacts to solid objects, piling up in the horizontal
	"""
	
	def __init__(self):
		TileType.__init__(self)
		self.tilecolor = (0,0,255)
		
		self.is_solid = True
		
		self.MAXWIDTH = 15
	
	def updatetile(self,x,y,read,write):
		"""
		Updates a specific tile
		"""
		
		#Turn fire into smoke
		hasfire,fx,fy = self._check_neighbor_id(x,y,self.world.get_tile_type_id("fire"),read)
		
		if hasfire:
			write[fx][fy] = self.world.get_tile_type_id("smoke")
		
		#DOWN DELETE
		if y == self.height-1:
			return
			
		#DOWN
		if y < self.height-1 and self.gettype(x,y+1,read).is_solid == False:
			#MOVE 
			write[x][y+1] = self.id
			return
			
		#LEFT DIAGONAL
		elif x < self.width-1 and y < self.height-1 and self.gettype(x+1,y+1,read).is_solid == False:
			#MOVE 
			write[x+1][y+1] = self.id
			return
	
		#RIGHT DIAGONAL
		elif x > 0 and y < self.height-1  and self.gettype(x-1,y+1,read).is_solid == False:
			#MOVE 
			write[x-1][y+1] = self.id
			return
		
		if y < self.height-2:
			
			dir = self.world.randdir
			
			#LEFT
			for i in range(self.MAXWIDTH):
				
				nx = x + dir*(i+1)
				
				if nx <= 1 or nx >= self.width-2:
					break
				
				if self.gettype(nx,y+1,read).is_solid and self.gettype(nx,y+1,read).id != self.id:
					break
					
				if self.gettype(nx,y+1,read).is_solid == False and self.gettype(x,y+1,read).id == self.id: # and self.gettype(nx + (-dir) * (2),y+2,read).id == self.id:
					write[nx][y+1] = self.id
					return
			
			dir = -dir
			
			#RIGHT
			for i in range(self.MAXWIDTH):
				
				nx = x + dir*(i+1)
				
				if nx <= 1 or nx >= self.width-2:
					break
				
				if self.gettype(nx,y+1,read).is_solid and self.gettype(nx,y+1,read).id != self.id:
					break
					
				if self.gettype(nx,y+1,read).is_solid == False and self.gettype(x,y+1,read).id == self.id: # and self.gettype(nx + (-dir) * (2),y+2,read).id == self.id:
					write[nx][y+1] = self.id
					return
		
		#If no left or right neighbors, then die
		if x > 0 and self.gettype(x-1,y,read).is_solid == False and x < self.width and self.gettype(x+1,y,read).is_solid == False:
			write[x][y] = 0
			return
		
		write[x][y] = self.id
		
		
	def color(self,x,y,tiledata):
		return self.tilecolor

class CurseTile(TileType):
	"""
	A tile type that spreads each tick
	"""
	
	def __init__(self):
		TileType.__init__(self)
		self.tilecolor =  (255, 0, 0)
		
	def updatetile(self,x,y,old,new):
		"""
		Updates a specific tile
		"""
		
		width = len(old)
		height = len(old[0])
		
		#Copy current
		new[x][y] = old[x][y]
		
		#LEFT
		if x > 0 and old[x-1][y] != self.id:
			new[x-1][y] = self.id
			
		#RIGHT
		if x < width-1 and old[x+1][y] != self.id:
			new[x+1][y] = self.id
			
		#UP
		if y > 0 and old[x][y-1] != self.id:
			new[x][y-1] = self.id
			
		#DOWN
		if y < height-1 and old[x][y+1] != self.id:
			new[x][y+1] = self.id
	
	def color(self,x,y,tiledata):
		return self.tilecolor
