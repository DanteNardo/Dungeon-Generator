


class Room(object):

	# ===================================
	# ============ Variables ============
	# ===================================
	width  = 0
	height = 0
	edges  = []
	pos    = (0, 0)	# Topleft corner


	# ===================================
	# ============ Functions ============
	# ===================================

	# Constructor
	def __init__(self, w, h, pos):
		self.width  = w
		self.height = h
		self.pos    = pos
		self.edges  = []

	# This function generates a list of tuple coordinates
	# The list contains coordinates for the edges of the room
	def generate_edges(self):

		# Top and Bottom row
		for i in range(0, self.width):
			self.edges.append((self.pos[0], self.pos[1]+i))
			self.edges.append((self.pos[0]+self.height-1, self.pos[1]+i))

		# Left and Right side
		for i in range(1, self.height-1):
			self.edges.append((self.pos[0]+i, self.pos[1]))
			self.edges.append((self.pos[0]+i, self.pos[1]+self.width-1))