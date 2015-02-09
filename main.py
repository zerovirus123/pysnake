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


class Board(object):
    """
    A board for Pysnake, implemented using a deque and a tuple.
    The deque represents the snake's body positions (the right end
    of the deque is its head, while the left is its tail). The tuple
    represents the apple's location on the board.

    The origin (0,0) is the top left of the screen where positive x
    is rightwards and positive y is downwards.
    """

    def __init__(self, size):
        """
        Declare (and comment) the data types used on the board.
        
        Spawn a player and an apple object to start off the game.
        """
        # deque of tuples describing the snake
        # the left end of the deque is the tail (x,y) position
        # the right end of the deque is the head
        self.snake = deque()

        # a tuple (x,y) coordinates for current apple's location
        self.apple = tuple()
        self.size = size  # the number of board locations for both dimensions
        # when an apple spawns some blue rings spawn like ripples around
        # it for a few frames
        self.droplets = list() # TODO : Add this visual affect

        # TODO : Add enemy snakes
        # TODO : Add enemy snake A.I. that seeks other apples randomly
        # and grows in length

        # player starts by moving downward by default
        self.last_direction = 'D'

        self.spawn_player()
        self.spawn_apple()

    def spawn_player(self):
        """
        Spawns the player somewhere in the middle of the board.
        """
        # This is some sketchy arithmetic but it is okay as long
        # as long as you dont put parantheses around (3/4)
        # otherwise it is self.size*(0) in python2.x while *(0.75) in 3.x
        xpos = random.randint(self.size/4, self.size*3/4)
        ypos = random.randint(self.size/4, self.size*3/4)
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
        xpos = random.randint(0, self.size-1)
        ypos = random.randint(0, self.size-1)

        # Loop through board positions until we return to where we started or
        # find an empty position to place the apple
        original_xpos, original_ypos = xpos, ypos

        # When adding more objects than only a snake, this will need to be
        # changed to `while pos in game_objects` (some union of all objects)
        # This could probably be done using a set, it may be a duplicate of
        # the information already stored in the board data. A similar method
        # as adding an apple will need to be implemented when adding any other
        # object that cannot spawn in another.
        while (xpos, ypos) in self.snake:
            xpos, ypos = self.next_pos(xpos, ypos)
            if xpos == original_xpos and ypos == original_ypos:
                print("Checked the entire board, found no empty spots!")
                stop_game()  # TODO : don't consider this an error?
                # The snake and/or other objects would need to occupy the
                # entire board for there to be no room to spawn an apple.
                # Maybe make this a victory condition.

        self.apple = (xpos, ypos)

    def next_pos(self, xpos, ypos):
        """
        Find the next position given a board position, or wrapping around to
        (0, 0) if we are already at the last position (size-1, size-1)
        """
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
        head = self.snake.pop()  # pop the head off and look at it
        self.snake.append(head)  # put the head back on
        xpos, ypos = head[0], head[1]  # get the location info from the head

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
                self.move_player(self.last_direction)
                return
            ypos -= 1
        elif direction == 'L':
            if self.last_direction == 'R':
                self.move_player(self.last_direction)
                return
            xpos -= 1
        elif direction == 'R':
            if self.last_direction == 'L':
                self.move_player(self.last_direction)
                return
            xpos += 1

        #if position is off the board, end the game
        if (xpos >= self.size) \
        or (ypos >= self.size) \
        or (xpos < 0) \
        or (ypos < 0):
            print("Snake went off the board!")
            stop_game()  # TODO : Maybe make this a non-error and
            # incur a penalty instead or something

        # if we run into ourselves, then we lose the game
        if (xpos, ypos) in self.snake:
            print("Snake ran into its body!")
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
        # for a given tick rate x the fps is 1/x
        self.BASE_TICK_RATE = 0.1 #0.075

        # TODO : Along with the snake increasing in length for each apple
        # eaten, there should be a level up system visually displayed.
        # The min_resolution calculation and other drawing logic should
        # be adapted to comepsnate for the new display area.

        # TODO : We should be able to draw text to the screen using a custom
        # image based font system.

        # TODO : Allow for blasphemous rectangular dimensioned games to be set

        self.init_pygame()
        self.board = Board(self.BOARD_ELEMENTS)

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
        self.window.update()
        time.sleep(self.BASE_TICK_RATE)

    def get_input(self):
        """
        Gets input to the game window.
        """

        # TODO : The input system is faulty because if the game
        # tick rate is slower than the user, directions will not
        # be changed quickly enough. This is probably the biggest
        # problem with the game currently.
        # - -- - -- - -- - -- - -- - -- - -- - -- - -- - -- - --
        # Example of problem:
        # 1. Game updates and player is moving downwards
        # 2. Player wants to turn around (180 degrees)
        # 3. Player presses d to turn right
        # 4. direction set to 'R', game still hasn't updated
        # 5. Player presses w to turn upwards
        # 6. direction overwritten to 'U', game ignored the 'R'
        # 7. game finally updates but ignores movement because game does not
        #    allow 180 degree turns in a single tick (see Board.move_player),
        #    otherwise the player would kill themselves.
        # 8. Player continues moving downwards as in step 1.
        # 9. Player runs into the bottom of screen, etc.

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

                elif event.key == pygame.K_SPACE:
                    # TODO : This should pause the game until pressed again
                    print("This should pause the game some day")
                    pass

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
        SIZE = self.BOARD_ELEMENT_SIZE

        # paint the screen black
        self.screen.fill(Color.BLACK)

        # draw the apple
        apple = self.board.apple
        apple = (apple[0]*SIZE, apple[1]*SIZE)
        apple = pygame.Rect(apple, (SIZE, SIZE))
        pygame.draw.rect(self.screen, Color.RED, apple)

        snake = self.board.snake
        for body in snake:
            # draw a snake body part
            body = pygame.Rect(body[0]*SIZE, body[1]*SIZE, SIZE, SIZE)
            pygame.draw.rect(self.screen, Color.GREEN, body)


def stop_game():
    pygame.quit()
    sys.exit()


def main():
    app = Pysnake()
    app.start()


if __name__ == "__main__":
    main()
