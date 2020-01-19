import logging
import time

import pygame
from pygame.locals import *
from pygame import surfarray
from pygame import Color

from sandboxx.world import World
from sandboxx.scene import Scene
from sandboxx.renderer import Renderer

class GameScene(Scene):
	
	def __init__(self,application,oncomplete):
		
		Scene.__init__(self,application,oncomplete)
		self.renderer = Renderer(self)
		
		#Events that kill the game
		self.stopevents = QUIT
		
		#List of keys
		self.numberkeys = [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
		
	def startscene(self):
		"""
		Initializes update loop for scene
		"""
		
		logging.info("Starting GAME scene")
		
		self.running = True
		self.world = World(self)
		self.world.create()
		
		#DEFAULT: SAND
		self.paint_id = 1
		self.paint_size = 5
		
		self.renderer.update_textinfo()
		
		while self.running:
			
			starttime = time.time()
			
			self.update()
			
			#Wait a bit per update, if we didn't spend that time rendering
			waittime = starttime - time.time() + 0.01
			
			if waittime > 0:
				time.sleep(waittime)
	
	def check_input(self):
		"""
		Updates mouse and keyboard input
		"""
		
		leftmouse = pygame.mouse.get_pressed()[0]
		rightmouse = pygame.mouse.get_pressed()[2]
		
		#Input
		if(leftmouse or rightmouse):
			mpos = pygame.mouse.get_pos()
			
			x = int(mpos[0] / self.application.scale)
			y = int(mpos[1] / self.application.scale)
			
			if leftmouse:
				self.paint(x,y,self.paint_id)
			else:
				self.paint(x,y,0)
			
		for i in range(len(self.numberkeys)):
			if pygame.key.get_pressed()[self.numberkeys[i]]:
				
				if pygame.key.get_pressed()[K_LALT]:
					id = self.world.shiftkeys[i]
				else:
					id = self.world.keys[i]
					
				if id == -1:
					continue
				
				if self.paint_id != id:
					
					self.paint_id = id
					self.renderer.update_textinfo()
					logging.info("Detected Key," + str(i+1) + " switched to " + self.world.names[id])
					
	def update(self):
		"""
		Run every frame: updates and renders game
		"""
		
		#Detect pygame event triggering end of game
		for e in pygame.event.get():
			if e.type is QUIT:
				self.stopscene()
				self.oncomplete()
				return
		
		self.check_input()
		
		#Update world
		self.world.tick()
		
		#Render
		self.renderer.render()
	
	def paint(self,x,y,id):
		"""
		Paints a block onto a area
		
		PARAMETERS
		----------
		x: x position
		y: y position
		id: tile ID
		"""
		
		self.world.drawblock(x,y,self.paint_size,self.paint_size,id)
		
	def stopscene(self):
		"""
		Stops scene
		"""
		
		self.running = False
		
		logging.info("Stopping scene")
		
		
