from random import *

#for easier reading
row = 0
col = 1
EMPTY = 0
snake_body = 1
apple = 2

board_size = 20
apple = []

class snake_board():
    """ for board, 0 for EMPTY, 1 for snake, 2 for apple
            """
    def __init__():
        self.board = []
        for _ in range(board_size):
            self.board.append(range(board_size))

        for row in board:
            for col in board[row]:
            self.board[row][col].append(EMPTY)

    def generate_apple():
       EMPTY_space = False
       apple_x = random(board_size)
       apple_y = random(board_size)
       while EMPTY_space = False:
           if self.board[apple_x, apple_y] == snake_body \
        or self.board[apple_x, apple_y] == apple:
              continue
           else:
          self.board[apple_x,apple_y] = apple
                    

class snake():
    def __init__():
        self.dead = False
        self.score = 0
        self.body_length = 3    
        self.head = [9,9]
        self.body = [[10,10], [11,11], [12,12]]

    def collide():
        if self.head in self.body:
            self.dead = True
        if self.head[row]<0 or self.head[row]>=board_size or self.head[col]<0 \          or self.head[col] >= board_size: 
            self.dead = True
        if 	 

    def move():
        pass
