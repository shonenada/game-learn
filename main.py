#/usr/bin/python
from __future__ import division
from sys import exit
import time

from PIL import Image
import pygame
from pygame.locals import *

import utils

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
N_MIN = 5
N_MAX = 7
STAY_STEP = 0
WALK_STEP = 10
STAY_SLEEP = 0
WALK_SLEEP = 1 / 8

LEFT_WALK = lambda c: c.transpose(Image.FLIP_LEFT_RIGHT)


def main():
    pygame.init()
    pygame.display.set_caption('Dennis Test')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 16)

    # dennis_bmp = Image.open('sprites/dennis_0.bmp')
    dennis_bmp = Image.open('0.bmp')
    dennis_bmp = utils.transparent(dennis_bmp, (-1, -1, -1))
    # dennis = pygame.image.frombuffer(
    #     dennis_bmp.tostring(),
    #     dennis_bmp.size,
    #     dennis_bmp.mode
    # )

    x_seed = 0
    x_seed_step = 0
    time_sleep = STAY_SLEEP

    s_x, s_y = 0, 0
    s_step_x = WALK_STEP
    s_step_y = WALK_STEP

    color_fill = BLACK
    crop_x, crop_y = 0, 0

    update_action = set()

    pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])
    
    def update_dennis():
        cropped = utils.get_crop(dennis_bmp, (79, 79), (crop_x, crop_y))

        for action in update_action:
            cropped = action(cropped)

        dennis = pygame.image.frombuffer(
            cropped.tostring(),
            cropped.size,
            cropped.mode
        )
        screen.fill(color_fill)
        screen.blit(dennis, (s_x, s_y))
        pygame.display.update()

    s_step_y = 0
    s_step_x = 0

    while True:
        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                time_sleep = WALK_SLEEP
                x_seed = N_MIN
                x_seed_step = 1

                if event.key == K_RIGHT:
                    s_step_x = WALK_STEP
                    if LEFT_WALK in update_action:
                        update_action.remove(LEFT_WALK)
                elif event.key == K_LEFT:
                    update_action.update([LEFT_WALK])
                    s_step_x = -1 * WALK_STEP

                elif event.key == K_UP:
                    s_step_y = -1 * WALK_STEP

                elif event.key == K_DOWN:
                    s_step_y = WALK_STEP

            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    s_step_x = 0
                elif event.key == K_UP or event.key == K_DOWN:
                    s_step_y = 0
                if s_step_x + s_step_y == 0:
                    time_sleep = STAY_SLEEP
                    x_seed_step = 0
                    x_seed = 0

        if x_seed_step > 0 and x_seed >= N_MAX:
            x_seed_step = -1
        elif x_seed_step < 0 and x_seed <= N_MIN:
            x_seed_step = 1

        x_seed = x_seed + x_seed_step
        crop_x = x_seed * 80
        s_x = s_x + s_step_x
        s_y = s_y + s_step_y

        time.sleep ( time_sleep )
        s_x = min(s_x, SCREEN_WIDTH - 79)
        s_x = max(s_x, 0)
        s_y = min(s_y, SCREEN_HEIGHT - 90)
        s_y = max(s_y, 0)
        update_dennis()


if __name__ == '__main__':
    main()
