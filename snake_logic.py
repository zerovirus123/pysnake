from random import *

#for easier reading
row = 0
col = 1
empty = 0
snake_body = 1
apple = 2

board_size = 20
apple = []

class snake_board():
	""" for board, 0 for empty, 1 for snake, 2 for apple
			"""
	def __init__():
		board = []
		for _ in range(board_size):
		    board.append(range(board_size))

		for row in board:
		    for col in board[row]:
			board[row][col].append(empty)

	def generate_apple():
	   empty_space = False
	   apple_x = random(board_size)
	   apple_y = random(board_size)
	   while empty_space = False:
	       if board[apple_x, apple_y] == snake_body \
		or board[apple_x, apple_y] == apple:
	          continue
	       else:
		  board[apple_x,apple_y] = apple
			    	

class snake():
	def __init__():
	    dead = False
	    score = 0
	    body_length = 3	
	    head = [9,9]
	    body = [[10,10], [11,11], [12,12]]


	def collide():
	    if head in body:
		snake.dead = True
	    if head[row]<0 or head[row]>=board_size or head[col]<0 \
	        or head[col] >= board_size: 
		snake.dead = True

	def move():
	    pass


