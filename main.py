#!/usr/bin/python
#
# Date: 2015-02-09
#
# Authors: (add yourself if you contribute)
#   Justin Brown
#
# Contributing: Please use a ridiculous, obscene, or repugnant number of
# accurate comments. Docstring all the things. To work on issue 14 you
# should create a branch named branch_name-14 and if possible request or
# assign yourself to the issue in the github tracker. When making commits
# on your branch use a #refs 14 on one of the lines in the commit message.
#
# Description: Pysnake - a snake implementation using pygame
# Use python 2.7.x but conform to 3.x if possible
#

"""
Docstring all the things.
"""

from __future__ import print_function
# in python 3.x range is removed and xrange is renamed to range
range = xrange

import sys
import os
import time
import random
from collections import deque

import pygame
import pygame.locals

# tell pygame to center the game window location
# on your screen when it gets created.
os.environ['SDL_VIDEO_CENTERED'] = "1"

class Color(object):
    """
    A container object for color definitions
    """
#   name           r    g    b
    RED       = (215, 000, 000)
    BLUE      = (000, 000, 220)
    GREEN     = (000, 185, 000)
    BLACK     = (000, 000, 000)

class Pause():
    """
    Holds the pause state of the game, that can be shared amongst all classes. Beats global variables all day every day!
    """
    pause = False


class Board(object):
    """
    A board for Pysnake, implemented using a deque and a tuple.
    The deque represents the snake's body positions (the right end
    of the deque is its head, while the left is its tail). The tuple
    represents the apple's location on the board.

    |tail|   |    |    |    |    | head |

    The origin (0,0) is the top left of the screen where positive x
    is rightwards and positive y is downwards.
    """

    def __init__(self, size):
        """
        Declare (and comment) the data types used on the board.
        
        Spawn a player and an apple object to start off the game.
        """
        # the left end of the deque is the tail (x,y) position
        # the right end of the deque is the head
        self.snake = deque()

        # a tuple (x,y) coordinates for current apple's location
        self.apple = tuple()
        
        self.size = size  # the number of board locations for both dimensions
        # when an apple spawns some blue rings spawn like ripples around
        # it for a few frames
        self.droplets = list() # TODO : Add this visual effect

        # player starts by moving downward by default
        self.last_direction = 'D'

        self.spawn_player()
        self.spawn_apple()

    def spawn_player(self):
        """
        Spawns the player somewhere in the middle of the board.
        """
        # Careful order of operations with a python 2.7 int.
        xpos = random.randint(self.size/4, self.size*3/4)
        ypos = random.randint(self.size/4, self.size*3/4)

        # Spawn the snake body (issue )
        self.snake.append((xpos, ypos))        # the snake's head
        self.snake.appendleft((xpos-1, ypos))  # center of body
        self.snake.appendleft((xpos-2, ypos))  # the snake's tail

        # TODO : make the snake start with n>2 number of body parts by making
        # it move outwards from it's start place as if it's body exists in the
        # third dimension and is coming onto the game plane.

    def spawn_apple(self):
        """
        Finds an empty position to spawn an apple, and then places it there.
        """

        # Get a random location on the board
        xpos = random.randint(0, self.size-1)
        ypos = random.randint(0, self.size-1)

        # Remember this location.
        original_xpos, original_ypos = xpos, ypos

        # While that location is inside an object that we do not wish to spawn
        # apples inside of (such as snake's body) :
        while (xpos, ypos) in self.snake:
            # Increment through board positions
            xpos, ypos = self.next_pos(xpos, ypos)
            # If we checked all positions and wrapped around to the original
            if xpos == original_xpos and ypos == original_ypos:
                print("Checked the entire board, found no empty spots!")
                stop_game()

        # Place the apple at the chosen location.
        self.apple = (xpos, ypos)

    def next_pos(self, xpos, ypos):
        """
        Find the next position given a board position, or wrapping around to
        (0, 0) if we are already at the last position (size-1, size-1)
        """
        if Pause.pause == False:
            if xpos + 1 >= self.size:
                xpos = 0
                if ypos + 1 >= self.size:
                    return 0, 0
                else:
                    return xpos, ypos + 1
            else:
                return xpos + 1, ypos

    def move_player(self, direction):
        """
        Move the player in the chosen direction.

        Updates the snake's new head position, or if the snake's head
        is located off the board or runs into itself then the game will end.

        Also spawns a new apple when one is eaten. If an apple was not eaten,
        the snake's tail is removed to preserve it's length.
        """
        if Pause.pause == False:
            length = len(self.snake)
            head = self.snake[length-1]
            xpos, ypos = head[0], head[1]  # get the location of the head
     
            # get new pos: note that video coordinate systems have the origin
            # start in the top left of the monitor, positive y is downward and
            # positive x is to the right.
            if direction == 'D':
                if self.last_direction == 'U':
                    # If snake tries to move back in on itself, ignore it
                    self.move_player(self.last_direction)
                    return
                ypos += 1
            elif direction == 'U':
                if self.last_direction == 'D':
                    #snake tries to move up and into itself, ignore
                    self.move_player(self.last_direction)
                    return
                ypos -= 1
            elif direction == 'L':
                if self.last_direction == 'R':
                    #snake tries to move left into itself, ignore
                    self.move_player(self.last_direction)
                    return
                xpos -= 1
            elif direction == 'R':
                if self.last_direction == 'L':
                    #snake tries to move right into itself, ignore
                    self.move_player(self.last_direction)
                    return
                xpos += 1

            #if position is off the board, end the game
            if (xpos >= self.size) \
            or (ypos >= self.size) \
            or (xpos < 0) \
            or (ypos < 0):
                print("Pysnake traveled abroad!")
                stop_game()

            # if we run into ourselves, then we lose the game
            if (xpos, ypos) in self.snake:
                print("Pysnake hugged itself!")
                stop_game()

            #if not apple remove tail
            if (xpos, ypos) != self.apple:
                self.snake.popleft()

            #else it was an apple, so spawn a new one
            else:
                self.spawn_apple()
                # TODO : also increase the game level (up the speed)

            #add a new body part at the location
            self.snake.append((xpos, ypos))

            # save this direction so we dont allow reverse direction later
            self.last_direction = direction


class Pysnake(object):
    """
    The Pysnake class uses pygame to handle input, create windows, and handle
    setting up the game by declaring constants. The board handles most of the
    game logic. Pysnake renders the board for us. You can think of Pysnake
    as the view/controller and Board is the model in the MVC pattern.
    """

    def __init__(self):
        """
        Defines constants and calls the other initialization methods.

        Change these settings to personalize the game to your liking.
        """
        # all board locations are basically defined by a square where
        # the top left of the square is the x,y coordinates of a tuple.

        # the edge size of each square in the game
        self.BOARD_ELEMENT_SIZE = 16

        # this is the number of positions, x and y, on the board
        self.BOARD_ELEMENTS = 32

        # determines the base game speed (higher value is slower pace)
        # for a given tick rate x, the FPS is 1/x
        self.BASE_TICK_RATE = 0.1 #0.075

        # TODO : Allow for blasphemous rectangular dimensioned games to be set

        self.init_pygame()
        self.board = Board(self.BOARD_ELEMENTS)

        # pysnake on drugs
        self.skew = [0,0]
        self.on_drugs = False


    def init_pygame(self):
        """
        Handles pygame initialization and ensuring the game settings will work
        with the player's monitor resolution.

        The game settings are defined in this class's __init__ method.
        """
        pygame.init()

        # get the user's current screen resolution
        screen_info = pygame.display.Info()
        screen_x = screen_info.current_w
        screen_y = screen_info.current_h

        min_resolution = self.BOARD_ELEMENT_SIZE * self.BOARD_ELEMENTS

        if (screen_x == -1 or screen_y == -1):
            print("display info error, or your version of pygame is too old")
            stop_game()

        if (screen_x < min_resolution) \
        or (screen_y < min_resolution):
            print("The board settings are too large for your monitor")
            print("You would need a %dp," % min_resolution,
                  "or greater, resolution to play at these settings.")
            print("Lower the game settings or raise your desktop resolution.")
            stop_game()

        self.window = pygame.display
        self.screen = self.window.set_mode((min_resolution, min_resolution))
        self.window.set_caption("pysnake")

    def start(self):
        """
        This begins Pysnake.
        """
        self.player_direction = 'D'

        while True:
            self.game_tick()

    def game_tick(self):
        """
        Gathers user input and updates the game accordingly.
        """
        self.get_input()
        self.board.move_player(self.player_direction)
        self.draw_board()
        if Pause.pause == False:
            self.window.update()
        time.sleep(self.BASE_TICK_RATE)

    def get_input(self):
        """
        Gets input to the game window.
        """

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                stop_game()
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    stop_game()
                elif event.key == pygame.K_DOWN \
                or   event.key == pygame.K_s:
                    self.player_direction = 'D'
                elif event.key == pygame.K_UP \
                or   event.key == pygame.K_w:
                    self.player_direction = 'U'
                elif event.key == pygame.K_LEFT \
                or   event.key == pygame.K_a:
                    self.player_direction = 'L'
                elif event.key == pygame.K_RIGHT \
                or   event.key == pygame.K_d:
                    self.player_direction = 'R'
                    self.on_drugs = not self.on_drugs
                    self.skew = [0, 0]

                elif event.key == pygame.K_SPACE:
                    # TODO : This should pause the game until pressed again
                    if Pause.pause == False:
                        Pause.pause = True
                        print("Game Paused\n")
                    else:
                        Pause.pause = False
                        print("Resume game\n")
                    
                        
                # admin/debug commands, etc
                elif event.key == pygame.K_q:
                    self.BASE_TICK_RATE -= 0.01
                    if self.BASE_TICK_RATE < 0.01:
                        # dont go below 0.01 tick speed, thats too fast
                        # 0.01 seconds / 1 frame -> 100 frames / 1 second
                        self.BASE_TICK_RATE = 0.01
                    print(self.BASE_TICK_RATE)
                elif event.key == pygame.K_e:
                    self.BASE_TICK_RATE += 0.01
                    print(self.BASE_TICK_RATE)

    def draw_board(self):
        """
        Renders the game board based on its current state.
        """

        # pysnake on drugs
        if self.on_drugs:
            for i in range(2):
                R = random.choice([-1, 0, 0, 1])
                self.skew[i] += R

        SIZE = self.BOARD_ELEMENT_SIZE

        # paint the screen black
        self.screen.fill(Color.BLACK)

        # draw the apple
        self.draw_rect(self.board.apple, Color.RED, self.skew)

        snake = self.board.snake
        for body in snake:
            # draw a snake body part
            self.draw_rect(body, Color.GREEN, self.skew)

    def draw_rect(self, board_location, color, skew=(0,0)):
        """
        Takes a board (x,y) tuple location and determines the pixel coordinate
        for the top-left pixel. With that and the size of board elements,
        pygame can create a rectangle object for us (a square) and draw it.
        """
        size = self.BOARD_ELEMENT_SIZE

        # pysnake on drugs
        x_skew = skew[0]
        y_skew = skew[1]

        topleft_pixel = (board_location[0]*size,
                         board_location[1]*size)
        width_height = (size + x_skew, size + y_skew)
        rect = pygame.Rect(topleft_pixel, width_height)
        pygame.draw.rect(self.screen, color, rect)




def stop_game():
    pygame.quit()
    sys.exit()


def main():
    app = Pysnake()
    app.start()


if __name__ == "__main__":
    main()
