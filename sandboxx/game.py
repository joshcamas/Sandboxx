# INF360 - Programming in Python
# Joshua Steinhauer
# Final Assignment

"""
	----------[ SANDBOXX ]----------
	
	A simple simulation game, where you can spawn
	sand and other materials that interact with each other
	
	REQUIREMENTS: pygame, numpy
	
	CONTROLS: 
		Left click: Paint material
		Right click: Erase material
		Number keys (1-8): Change paint material
	
	PAINTABLE MATERIALS:
		1: Wood
		2: Steel
		3: Sand
		4: Wax
		5: Wire
		6: Electricity
		7: Wire
		8: Seed
		9: Water
	
	FEATURES:
		- Solids and semi-liquids (steel vs sand)
		- Fire turns into smoke
		- Fire, Smoke, Electricity die over time
		- Wax melts when heated
		- Electricity sparks oil, and activates wire
		- Seeds grow into plants, which will die without support
		
		- Extendable engine
		- Upscale renderer + smart render waiter
	
	TODO:
		- Optimize world updater (it's slow)
		- Redesign ticker to allow liquid water
		- Add sound engine
	
"""

import logging
from sandboxx.application import Application
from sandboxx.gamescene import GameScene

SCREEN_SIZE = (100, 60)
SCREEN_SCALE = 8

def ongamecomplete():
	pass
	
if __name__ == "__main__":
	
	logging.basicConfig(filename='logoutput.log',level=logging.DEBUG)
	
	application = Application(SCREEN_SIZE,SCREEN_SCALE)
	gamescene = GameScene(application,ongamecomplete)
	application.startscene(gamescene)
