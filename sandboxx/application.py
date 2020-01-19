import logging

import pygame
from pygame.locals import *
from pygame import surfarray
from pygame import Color

class Application():
	"""
	Thin wrapper that handles pygame window 
	and scene management
	"""
	def __init__(self,screensize,scale=1):
		"""
		Application constructor
		
		PARAMETERS
		----------
		screensize: 2d tuple, dimensions of screen
		scale: the scale of the screensize for the window
		"""
		
		logging.info("Initializing Application")
		
		if scale <= 0:
			logging.critical("Application cannot utilize a negative scale")
			return
			
		pygame.init()
		
		self.screensize = screensize
		self.scaled_screensize = (screensize[0]*scale,screensize[1]*scale)
		self.scale = scale
		
		logging.info("Building screensize of (" + str(self.screensize[0]) + "," + str(self.screensize[1]) + ") with a scale of " + str(scale) + "x")
		
		#Create full size screen
		self.screen = pygame.display.set_mode(self.scaled_screensize, HWSURFACE|DOUBLEBUF|RESIZABLE)
		
		#Create lowres surface
		self.surface = pygame.Surface(screensize)
		
		#Intialize font
		pygame.font.init()
		self.simplefont = pygame.font.Font('sandboxx/data/font.ttf',38)
		
		self.scene = None
	
	def render_simplefont(self,text,color):
		"""
		Renders font onto surface
		"""
		return self.simplefont.render(text, False, color)
		
	def startscene(self,scene):
		"""
		Run a specified scene
		
		PARAMETERS
		----------
		scene: Scene to start
		"""
		
		if self.scene is not None:
			self.scene.stopscene()
		
		if scene is None:
			logging.critical("Cannot start a scene that is NONE")
			return
		
		self.scene = scene
		self.scene.startscene()
	
	def apply_surface(self):
		"""
		Blits surface to screen after scaling it
		"""
		
		self.screen.blit(pygame.transform.scale(self.surface, self.scaled_screensize), (0, 0))
	
	def complete_render(self):
		pygame.display.flip()
        
