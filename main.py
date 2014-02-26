#/usr/bin/python
from __future__ import division
from sys import exit
import time

from PIL import Image
import pygame
from pygame.locals import *

import utils


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    pygame.init()
    pygame.display.set_caption('Dennis Test')
    screen = pygame.display.set_mode((800, 600), 0, 16)

    # dennis_bmp = Image.open('sprites/dennis_0.bmp')
    dennis_bmp = Image.open('0.bmp')
    dennis_bmp = utils.transparent(dennis_bmp, (-1, -1, -1))
    # dennis = pygame.image.frombuffer(
    #     dennis_bmp.tostring(),
    #     dennis_bmp.size,
    #     dennis_bmp.mode
    # )

    N_MIN = 5
    N_MAX = 7
    n = 0
    n_step = 0
    time_sleep = 0

    s_x, s_y = 0, 0
    s_step = 10

    color_fill = BLACK
    
    def update_dennis(x, y):
        cropped = utils.get_crop(dennis_bmp, (79, 79), (x, y))
        dennis = pygame.image.frombuffer(
            cropped.tostring(),
            cropped.size,
            cropped.mode
        )
        screen.fill(color_fill)
        screen.blit(dennis, (0, 0))
        pygame.display.update()


    crop_x, crop_y = 0, 0
    update_dennis(crop_x, crop_y)


    while True:
        event = pygame.event.poll()

        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                time_sleep = 1/6
                n = N_MIN
                n_step = 1
        elif event.type == KEYUP:
            n = 0
            n_step = 0

        if n_step > 0 and n >= N_MAX:
            n_step = -1
        elif n_step < 0 and n <= N_MIN:
            n_step = 1

        n = n + n_step
        crop_x = n * 80

        time.sleep( time_sleep )
        update_dennis(crop_x, crop_y)


if __name__ == '__main__':
    main()
