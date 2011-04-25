class Game_error(Exception):
	"""Errors related to the game in general"""
	pass

class Illegal_move(Game_error):
	"""Errors from illegal moves"""
	pass

class Game_rule_error(Game_error):
	"""Errors that arise from rule issues"""
	pass


class Reversi (object):
	"""
	0 = Empty
	1 = White (player 1)
	2 = Black (player 2)
	"""
	
	def __init__(self):
		super(Reversi, self).__init__()
		
		self.turn = 1
		self.player = 1
		
		self.board = [[0 for x in range(8)] for x in range(8)]
		
		self.board[3][3] = 1
		self.board[3][4] = 2
		self.board[4][3] = 2
		self.board[4][4] = 1
		
		self.has_changed = True
	
	def perform_move(self, x, y):
		# First check that the tile is empty
		if self.board[x][y] != 0:
			raise Illegal_move("Player {0} tried to place a tile at {1},{2} but it is already occupied by {3}".format(
				self.player,
				x, y,
				self.board[x][y]
			))
		
		# # Is it next to an existing piece?
		# next_to = False
		# # Left
		# if x > 0:
		# 	if self.board[x-1][y] > 0: next_to = True
		# 
		# # Right
		# if x < 7:
		# 	if self.board[x+1][y] > 0: next_to = True
		# 
		# # Up
		# if y > 0:
		# 	if self.board[x][y-1] > 0: next_to = True
		# 
		# # Down
		# if y < 7:
		# 	if self.board[x][y+1] > 0: next_to = True
		# 
		# if not next_to:
		# 	raise Illegal_move("Player {0} tried to place a tile at {1},{2} but it is not next to any other tiles".format(
		# 		self.player,
		# 		x, y,
		# 	))
		
		# Place it and work out the flips
		self.place_piece(x, y)
		
		# Does this end the game?
		all_tiles = [item for sublist in self.board for item in sublist]
		
		empty_tiles = len([0 for tile in all_tiles if tile == 0])
		white_tiles = len([0 for tile in all_tiles if tile == 1])
		black_tiles = len([0 for tile in all_tiles if tile == 2])
		
		# No moves left to make, end the game
		if white_tiles < 1 or black_tiles < 1 or empty_tiles < 1:
			self.end_game()
		
		# Alternate between player 1 and 2
		self.player = 3 - self.player
		self.has_changed = True
	
	def end_game(self):
		raise Exception("END GAME")
	
	def place_piece(self, x, y):
		self.board[x][y] = self.player
		change_count = 0
		
		# Get a reference to the row and column that we just placed a piece on
		column = self.board[x]
		row = [self.board[i][y] for i in range(0,8)]
		
		# First can we travel up?
		if self.player in column[:y]:
			changes = []
			search_complete = False
			
			for i in range(y-1,-1,-1):
				if search_complete: continue
				
				counter = column[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i in changes:
					self.board[x][i] = self.player
		
		# Down?
		if self.player in column[y:]:
			changes = []
			search_complete = False
			
			for i in range(y+1,8,1):
				if search_complete: continue
				
				counter = column[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i in changes:
					self.board[x][i] = self.player
		
		# Left?
		if self.player in row[:x]:
			changes = []
			search_complete = False
			
			for i in range(x-1,-1,-1):
				if search_complete: continue
				
				counter = row[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i in changes:
					self.board[i][y] = self.player
		
		# Right?
		if self.player in row[x:]:
			changes = []
			search_complete = False
			
			for i in range(x+1,8,1):
				if search_complete: continue
				
				counter = row[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i in changes:
					self.board[i][y] = self.player
		
		# Diagonals are a little harder
		xy_sum = x + y
		i, j = 0, xy_sum
		bl_tr_diagonal = []
		
		for q in range(0, xy_sum):
			if 0 <= i < 8 and 0 <= j < 8:
				bl_tr_diagonal.append(self.board[i][j])
			
			i += 1
			j -= 1
		
		i, j = x-min(x,y), y-min(x,y)
		br_tl_diagonal = []
		for q in range(0, xy_sum):
			if 0 <= i < 8 and 0 <= j < 8:
				br_tl_diagonal.append(self.board[i][j])
			
			i += 1
			j += 1
		
		# Up Right
		if self.player in bl_tr_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx += 1
				ly -= 1
				
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i, j in changes:
					self.board[i][j] = self.player
		
		# Down Right
		if self.player in bl_tr_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx -= 1
				ly += 1
				
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i, j in changes:
					self.board[i][j] = self.player
		
		
		# Up Left
		if self.player in br_tl_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx -= 1
				ly -= 1
				
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i, j in changes:
					self.board[i][j] = self.player
		
		# Down Right
		if self.player in br_tl_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx += 1
				ly += 1
				
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				for i, j in changes:
					self.board[i][j] = self.player
		
		if change_count == 0:
			self.board[x][y] = 0
			raise Illegal_move("Player {0} tried to place a tile at {1},{2} but that will result in 0 flips".format(
				self.player,
				x, y,
			))
			
	
	def ascii_board(self):
		for r in self.board:
			print("".join([str(t) for t in r]))
		print("")
	
