
class Scene():
	
	def __init__(self,application,oncomplete):
		"""
		Constructor
		
		PARAMETERS
		----------
		application: Owning application
		oncomplete: function to run when scene is stopped
		"""
		
		self.application = application
		self.oncomplete = oncomplete
		
		#Helpful shortcuts
		self.screen = self.application.screen
		self.screensize = self.application.screensize
		
	def stopscene(self):
		"""
		Run when scene is stopped
		"""
		
		pass
		
	def startscene(self):
		"""
		Run when scene is started
		"""
		pass
		
