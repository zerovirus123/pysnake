from random import *
import sys

#for easier reading
row = 0
col = 1
EMPTY = 0
SNAKE_BODY = 1
APPLE = 2
BOARD_SIZE = 20

#list of apple coordinates
apple_list = []

#snake vector
MOVE_UP = [0,-1]
MOVE_DOWN = [0,1]
MOVE_LEFT = [-1,0]
MOVE_RIGHT = [1,0]

class snake_board():
    """ for board, 0 for EMPTY, 1 for snake, 2 for APPLE
            """
    def __init__():
        self.board = []
        for _ in range(BOARD_SIZE):
            self.board.append(range(BOARD_SIZE))

        for row in board:
            for col in board[row]:
                self.board[row][col].append(EMPTY)

     #generates apple. called when snake eats apple (also once during start)
    def generate_apple():
       empty_space = False
       app_x = random(BOARD_SIZE)
       app_y = random(BOARD_SIZE)
       while empty_space is False:
           if self.board[app_x, app_y] == SNAKE_BODY:
	       continue
	   if self.board[APPLE_x, app_y] == APPLE:
               continue
           else: #adds apple
              self.board[app_x,app_y] = APPLE
	      apple_list.append([app_x, app_y])
	      empty_space = True

      #updates the board for every event cycle
    def update_board():
        for ROW in board:
	    for COL in board[ROW]:
	        if board[ROW][COL] == 0:
		    pass #update with empty grid
		elif board[ROW][COL] == 1: 
		    pass #update with snake body
		elif board[ROW][COL] == 2:
		    pass #update with apple
		else:
		    pass #try exception
                    
class Snake():
    def __init__():
        self.dead = False
        self.score = 0
        self.head = [9,9]
        self.body = [[10,10], [11,11], [12,12]]
        self.vector = MOVE_LEFT
        #vector indicates xy direction: 0 for negative direction 
        #and 1 for positive direction
 
    def move():
	#if no input within designated time limit snake moves on its own
	#otherwise move head and body
        #need some form of pivot that the snake body turns about

	#it seems that the arrow keys each have ANSI escape codes that 
        #are specific to the systems used. Not sure how to go on from here	
        pass

    def grow():
	tail = self.body[len(self.body)-1]
        if self.vector == MOVE_UP:
	    newTail = [tail[0], tail[1]+1]
	    self.body.append(newTail)
        if self.vector == MOVE_DOWN:
	    newTail = [tail[0], tail[1]-1]
	    self.body.append(newTail)	
	if self.vector == MOVE_LEFT:
	    newTail = [tail[0]+1, tail[1]]
	    self.body.append(newTail)
	if self.vector == MOVE_RIGHT:
	    newTail = [tail[0]-1, tail[1]]
	    self.body.append(newTail)

def collision(snake, board):
    if snake.head in snake.body:
        snake.dead = True
    for coordinates in snake.head:
	if coordinates < 0 or coordinates >= BOARD_SIZE:     
            snake.dead = True

    #see if snakes eat apple
    for apples in apple_list:
	if snake.head in apple_list:
            apple_list.remove(apples)
            snake.score+=1
	    board[apples[0]][apples[1]] = EMPTY
            board.generate_apple()
            snake.grow()

def main():
    #initializes board and snake object
    #wait for user moves. if not the snake moves in a straight line
    #test for collisions
    #repeat
    game_board = snake_board()
    snake = Snake()
    game_board.generate_apple() #first apple
    while(snake.dead == False):
	snake.move()
        collision(snake, game_board)

    print "Oh noes. Game over.\n"
    sys.exit() 
main
