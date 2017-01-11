


# Imports
from DungeonGenerator import DungeonGenerator
from App import *


# Main Function
def main():

	# Create the dungeon
	dg = DungeonGenerator()
	dg.generate_dungeon()

	# Create the GUI
	root = Tk()

if __name__ == "__main__":
    
	main()
	