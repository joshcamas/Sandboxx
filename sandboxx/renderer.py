import pygame
from pygame.locals import *
from pygame import surfarray
from pygame import Color

import logging

class Renderer():
	"""
	Game Renderer, which handles the actual blitting
	"""
	
	def __init__(self,gamescene):
		
		self.gamescene = gamescene
		self.application = self.gamescene.application
		self.screen = self.gamescene.screen
		
	def update_textinfo(self):
		logging.info("Updating text info surface")
		
		text = "     Keys:"
		
		#Draw list of keyed tiles
		for i in range(len(self.gamescene.world.keys)):
			
			id = self.gamescene.world.keys[i]
			
			if id == -1:
				continue
			
			if self.gamescene.paint_id == id:
				text += " [" + str(i) + " " + self.gamescene.world.names[id] + "]"
			else:
				text += "  " + str(i) + " " + self.gamescene.world.names[id] + " "
			 
		self.infosurf_keys = self.application.render_simplefont(text,(255,255,255))
		
		text = " Alt Keys:"
		
		#Draw list of shiftkeyed tiles
		for i in range(len(self.gamescene.world.shiftkeys)):
			
			id = self.gamescene.world.shiftkeys[i]
			
			if id == -1:
				continue
			
			if self.gamescene.paint_id == id:
				text += " [a" + str(i) + " " + self.gamescene.world.names[id] + "]"
			else:
				text += "  a" + str(i) + " " + self.gamescene.world.names[id] + " "
			 
		self.infosurf_shiftkeys = self.application.render_simplefont(text,(255,255,255))
		
	def render(self):
		"""
		Renders based on world data
		"""
		
		#Build pixel array
		pixelarray = pygame.PixelArray(self.application.surface)
		
		#Copy tiledata to pixel array
		for x in range(self.application.screensize[0]):
			for y in range(self.application.screensize[1]):
				
				id = self.gamescene.world.tiledata[x][y]
				
				pixelarray[x][y] = self.gamescene.world.tiletypes[id].color(x,y,self.gamescene.world.tiledata)
			
		surfarray.blit_array(self.application.surface, pixelarray)
		
		#Be sure to delete pixelarray, unlocking the surface
		del pixelarray

		#Apply scaled surface
		self.application.apply_surface()
		
		#Blit info text AFTER scale
		self.application.screen.blit(self.infosurf_keys,(20,0))
		self.application.screen.blit(self.infosurf_shiftkeys,(20,25))
		
		#Finalize render
		self.application.complete_render()
