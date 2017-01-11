


# Imports
from tkinter import *
from DungeonGenerator import DungeonGenerator

class Map(object):

	# ===================================
	# ============ Variables ============
	# ===================================
	dg    = DungeonGenerator()
	mpos  = (0, 0)
	msize = 10

	# ===================================
	# ============ Functions ============
	# ===================================

	# Constructor
	def __init__(self, pos):

		self.dg.generate_dungeon()
		self.mpos = pos