


# Imports
from Cell import Cell
from Room import Room
from random import randint
from random import shuffle

class DungeonGenerator(object):

	# ===================================
	# ============ Variables ============
	# ===================================

	player_pos = (0, 0)
	grid_size  = 50
	grid       = []
	rooms      = []

	# ===================================
	# ============ Utilities ============
	# ===================================

	# Checks to see if a given cell's neighbors have neighboring cells 
	# That are already part of rooms, 
	# If so return true since this cell is neighboring a room
	def room_neighbor(self, y, x):

		if len(self.grid[y][x].neighbors) == 0:
			pass
		for neighbor in self.grid[y][x].neighbors:
			for loc in self.grid[neighbor[0]][neighbor[1]].neighbors:
				if self.grid[loc[0]][loc[1]].cell_string == '#':
					return True
		return False

	# Checks to see if a given cell's neighbors are already part of rooms
	# If so return true since this cell is near neighboring a room
	def room_nearneighbor(self, y, x):

		for neighbor in self.grid[y][x].neighbors:
			if self.grid[neighbor[0]][neighbor[1]].cell_string == '#':
				return True
		return False

	# Updates player position in grid
	def update_playerPos(self, ny, nx):

		self.grid[self.player_pos[0]][self.player_pos[1]].set_string('.')
		self.grid[ny][nx].set_string('0')
		self.player_pos = (ny, nx)

	# Determines if a square's position is a valid board position
	# Returns True if valid square
	def valid_square(self, y, x):

		if (y < 0 or x < 0) or (y >= self.grid_size or x >= self.grid_size):
			return False
		return True

	# Determines if a cell is valid (prim's algorithm conditions)
	def valid_mazecell(self, cell):

		# Check if the cell is already opened
		if cell.cell_string == 'o':
			return False

		# Counting variable
		count = 0

		# Iterate through own neighbors
		for neighbor in cell.neighbors:

			# Check to make sure not too many are closed
			if self.grid[neighbor[0]][neighbor[1]].cell_string == 'o':
				count += 1

		# If the count is less than 2, return true
		# Else						   return False
		if count < 2:
			return True
		else:
			return False

	# Finds the x and y location of pockets
	def find_pockets(self):

		# Necessary for counting stuff
		count = 0

		# Iterate through entire dungeon
		for i in range(0, self.grid_size):
			for j in range(0, self.grid_size):

				# If the cell is valid and does not neighbor a room
				if (self.valid_mazecell(self.grid[i][j]) 
				and self.room_nearneighbor(i, j) == False):

					# Select new starting coordinates
					# ie We found a pocket
					# (y, x, count)
					return (i, j, count)
					
				# Increment count
				count += 1
		
		# Default return
		return (0, 0, -1)

	# Returns true if position is a dead end
	def dead_end(self, pos):

		# Check to make sure that the square you are checking is maze
		if self.grid[pos[0]][pos[1]].cell_string != 'o':
			return False

		# Count for how many neighbors exist
		count = 0

		# Iterate through neighbors
		for neighbor in self.grid[pos[0]][pos[1]].neighbors:

			# Increment count if the neighbor is not empty
			if (self.grid[neighbor[0]][neighbor[1]].cell_string == 'o'
			or  self.grid[neighbor[0]][neighbor[1]].cell_string == '#'):
				count += 1

		# One neighbor or less in maze == dead end
		if count <= 1:
			return True
		else:
			return False

	# Prints out the entire dungeon to the screen
	def print_dungeon(self):

		for i in range(0, self.grid_size):
			for j in range(0, self.grid_size):
				print(self.grid[i][j].cell_string + ' ', end='')
			print('')

				
	# ===================================
	# =========== Generation ============
	# ===================================


	# Generates the grid structure
	def generate_grid(self):

		# Iterate through two dimensional array
		# Create each cell and init position
		# Generate that cell's neighbors

		for i in range(0, self.grid_size):
			self.grid.append([])
			for j in range(0, self.grid_size):
				
				c = Cell(self.grid_size, i, j)
				c.generate_neighbors()
				self.grid[i].append(c)

	# First step of generate_maze()
	# Generate rooms of random size in the empty maze throughout
	def generate_rooms(self, attempts):

		# Generate rooms until attempts are over
		while (attempts > 0):

			# Generate width and height (3, 7)
			w = randint(3, 7)
			h = randint(3, 7)

			# Generate x and y position (0, grid_size)
			x = randint(0, self.grid_size)
			y = randint(0, self.grid_size)

			valid_room = True

			# Iterate through maze and see if room is valid
			for i in range(y, y + h):
				for j in range(x, x + w):
				
					# If it isn't a valid square
					# If it isn't empty
					# If its neighbor is part of a room
					if (not self.valid_square(i, j) 
						or self.grid[i][j].cell_string != '.' 
						or self.room_neighbor(i, j) == True):		
						attempts -= 1
						valid_room = False
						break

			# If valid_room is true then we place the room
			# Iterate through maze and create room
			if valid_room:

				# Create room object
				r = Room(w, h, (y, x))
				r.generate_edges()
				self.rooms.append(r)

				for i in range(y, y + h):
					for j in range(x, x + w):
						self.grid[i][j].cell_string = '#'

			# Decrement
			attempts -= 1

	# Second step of generate_maze()
	# Fill the gaps between rooms with random passageways
	# Does not connect the passageways to the rooms
	def fill_maze(self):

		# Necessary variables
		startx = 0
		starty = 0
		
		# Iterate until we have a valid starting square
		while True:

			# Select a random starting spot
			startx = randint(0, self.grid_size-1)
			starty = randint(0, self.grid_size-1)

			# Location must not have a room nearby
			if self.room_neighbor(starty, startx) == False:
				break
			
		# ======================================
		# Generate a maze using prim's algorithm
		# ======================================

		# Add an exception: 
		# Cells with neighbors that are '#' cannot be opened

		# Rerun maze algorithm for each pocket in dungeon
		# Without this the maze may be blocked by certain rooms
		# Pockets of nothing will fill the dungeon instead of maze
		while True:

			cells = []
			count = 0

			# Select starting cell
			cc = self.grid[starty][startx]
			cells.append((cc.cell_y, cc.cell_x))
		
			# Add current cell's neighbors to cell list
			for cell in cc.neighbors:
				cells.append(cell)

			# While we still have walls in our list
			while len(cells) > 0:

				# Select a random cell from cell list
				rcell = randint(0, len(cells)-1)
				cc = self.grid[cells[rcell][0]][cells[rcell][1]]

				# If the cell is valid and does not neighbor a room
				if (self.valid_mazecell(cc) and 
					self.room_nearneighbor(cc.cell_y, cc.cell_x) == False):
				
					# Mark Cell
					self.grid[cc.cell_y][cc.cell_x].cell_string = 'o'

					# Add current cell's neighbors to cell list
					for cell in cc.neighbors:
						cells.append(cell)

				# At the end, remove the current cell from cell list
				cell = (cc.cell_y, cc.cell_x)
				cells.remove(cell)

			# Enable these for procedural view or editing
			# self.print_dungeon()
			# print('')
			
			# ============================================
			# ========== End of Maze Algorithm ===========
			# ============================================
			# Search for pockets and repeat maze algorithm
			
			# Find pocket, save pocket data
			pocket = self.find_pockets()
			starty = pocket[0]
			startx = pocket[1]
			count  = pocket[2]

			# Check to see if we have checked every square
			# Condition: count == -1 when we can't find a pocket
			# If we have then break out of the loop (no pockets)
			# Else reset count
			if count == -1:
				break
			else: 
				count = 0

	# In-Between step where we clean up the maze (1)
	def clean_maze_1(self):

		# Remove all instances of '.' and replace with ' '
		for i in range(0, self.grid_size):
			for j in range(0, self.grid_size):
				if self.grid[i][j].cell_string == '.':
					self.grid[i][j].cell_string = ' '

		# FOR TESTING ROOM EDGES
		# Change all room edges to *
		#for r in self.rooms:
		#	for e in r.edges:
		#		self.grid[e[0]][e[1]].cell_string = '*'
		pass

	# In-Between step where we clean up the maze (2)
	def clean_maze_2(self):

		# Remove all instances of '.' and replace with ' '
		for i in range(0, self.grid_size):
			for j in range(0, self.grid_size):
				if self.grid[i][j].cell_string == 'o':
					self.grid[i][j].cell_string = '.'

	# Third step of generate_maze()
	# Connect the random passageways to the rooms
	def generate_corridors(self):

		# Iterate through all rooms
		for r in self.rooms:

			# Randomize edge list
			shuffle(r.edges)

			# Necessary variable to break out of loops
			connected    = False
			connectcount = 0

			# Iterate through all edges
			for edge in r.edges:
				
				# Try to connect it with a 1 cell away section of maze
				for n in self.grid[edge[0]][edge[1]].neighbors:

					# For breaking out of loops
					if connected == True:
						break

					# If neighbor cell is empty then it is valid
					if self.grid[n[0]][n[1]].cell_string == ' ':

						# Determine the direction to check for maze
						dir = (n[0] - edge[0], n[1] - edge[1])

						# Check to see if marking it would connect to passageway
						# Make sure connections are not placed next to each other
						if (self.valid_square(n[0]+dir[0], n[1]+dir[1]) and 
							self.valid_square(n[0]+dir[1], n[1]+dir[0]) and
							self.valid_square(n[0]-dir[1], n[1]+dir[0]) and
							self.grid[n[0]+dir[0]][n[1]+dir[1]].cell_string == 'o' and
							self.grid[n[0]+dir[1]][n[1]+dir[0]].cell_string != 'o' and
							self.grid[n[0]-dir[1]][n[1]+dir[0]].cell_string != 'o'):

							# Connect the corridor to the room
							self.grid[n[0]][n[1]].cell_string = 'o'
							
							# Increment connect count and check for connections
							connectcount += 1
							if connectcount >= 3:
								connected = True
								break

	# Fourth step of generate_maze()
	# Remove all dead ends from the maze
	def remove_ends(self):

		# Necessary function to determine looping
		cannotbreak = True
		
		# Run function until no maze left
		while cannotbreak:

			# Set to breaking unless told not to
			cannotbreak = False

			# Iterate through maze
			for i in range(0, self.grid_size):
				for j in range(0, self.grid_size):

					# If it is a dead end
					# Delete from maze
					# We cannot break because we must continue
					# until there are no more dead ends
					if self.dead_end((i, j)):

						self.grid[i][j].cell_string = ' '
						cannotbreak = True

	# Generates the entire dungeon
	# Calls all four parts of the algorithm
	def generate_dungeon(self):
	
		# Instantiate the grid data structure
		self.generate_grid()

		# Generate rooms of random size in the empty maze throughout
		self.generate_rooms(1000)
		self.print_dungeon()
	
		# Fill the gaps between rooms with random passageways
		# Does not connect the passageways to the rooms
		self.fill_maze()
		print('')
		print('')
		print('')
		self.print_dungeon()

		# Clean the maze and make it easier to understand
		self.clean_maze_1()

		# Connect the random passageways to the rooms
		self.generate_corridors()
		print('')
		print('')
		print('')
		self.print_dungeon()

		# Remove all dead ends from the maze
		self.remove_ends()

		# Clean maze again
		self.clean_maze_2()

		# Prints out the result
		print('')
		print('')
		print('')
		self.print_dungeon()
		pass