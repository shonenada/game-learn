from __future__ import division

from sys import exit
import time
from random import randint

import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    sprite = pygame.image.load('dennis_0.bmp').convert_alpha()

    walk_script = [
        4, 5, 6, 7, 6, 5
    ]
    idx = 0
    x, y = 640 / 2 - 40, 480 / 2 - 40
    step = 7
    target_x, target_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == MOUSEMOTION:
                target_x, target_y = event.pos
                target_x -= 40
                target_y -= 40

        screen.fill((0, 0, 0))
        screen.blit(sprite, (x, y), (walk_script[idx%len(walk_script)] * 80, 0, 80, 80))
        pygame.display.update()
        time.sleep(1 / 12)
        idx += 1
        if not target_x - x == 0:
            x += (target_x - x) / abs(target_x - x) * step
        if not target_y - y == 0:
            y += (target_y - y) / abs(target_y - y) * step



main()