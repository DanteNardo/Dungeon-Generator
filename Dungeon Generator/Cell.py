


class Cell(object):

	# ===================================
	# ============ Variables ============
	# ===================================
	cell_string = '.'
	grid_size   = 0
	cell_x      = 0
	cell_y      = 0
	neighbors	= []


	# ===================================
	# ============ Functions ============
	# ===================================

	# Constructor
	def __init__(self, grid_size, cell_y, cell_x):

		self.grid_size = grid_size
		self.cell_x    = cell_x
		self.cell_y    = cell_y
		self.neighbors = []
	
	# Generate a list of tuples that store neighboring cell positions
	def generate_neighbors(self):

		# Checks all four adjacent squares
		if self.cell_x+1 < self.grid_size:
			self.neighbors.append((self.cell_y, self.cell_x+1))
		if self.cell_x-1 >= 0:
			self.neighbors.append((self.cell_y, self.cell_x-1))
		if self.cell_y+1 < self.grid_size:
			self.neighbors.append((self.cell_y+1, self.cell_x))
		if self.cell_y-1 >= 0:
			self.neighbors.append((self.cell_y-1, self.cell_x))