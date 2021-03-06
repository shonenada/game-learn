from sys import exit
import time

import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2


def main():
    pygame.init()

    background = (0, 0, 0)
    screen = pygame.display.set_mode((640, 480), 0, 32)
    sprite = pygame.image.load('dennis_0.bmp').convert()

    script = [
        4, 5, 6, 7, 6, 5, 0
    ]
    idx = 0.0
    index = 0

    clock = pygame.time.Clock()

    pos = (Vector2(*screen.get_size()) - Vector2(*(80, 80))) / 2

    heading = Vector2()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        screen.fill(background)
        screen.blit(sprite, pos, (script[index] * 80, 0, 80, 80))
        pygame.display.update()


        if pygame.mouse.get_pressed()[0]:
            target = Vector2( *pygame.mouse.get_pos() ) - Vector2( *(80, 80) ) / 2
            idx += 1 / 4.
            index = int(idx) % (len(script)-1)
        else:
            target = pos
            idx = 0
            index = len(script) - 1 
        params_vector = Vector2.from_points(pos, target)


        ## Averagely
        params_vector.normalize()
        pos += params_vector * 150 * time_passed_seconds
        
        ## kind2
        # pos += params_vector * time_passed_seconds

        ## king3
        # params_vector.normalize()
        # heading = heading + (params_vector * 5)
        # pos += heading * time_passed_seconds

        pygame.display.update()


main()