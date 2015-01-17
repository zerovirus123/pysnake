import sys
import os

import pygame
import pygame.locals

import snake_logic


def main():
    pygame.init()
    window = pygame.display
    screen = window.set_mode((320, 320))
    window.set_caption("pysnake")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        window.update()


if __name__ == "__main__":
    main()