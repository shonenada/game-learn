#/usr/bin/python
from __future__ import division
from sys import exit
import time

from PIL import Image
import pygame
from pygame.locals import *

import utils

# Settings
CAPTION = 'Dennis Walking'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MODE = 0
COLOR_DEPTH = 32

# Sprite
SPRITE_WIDTH = 80
SPRITE_HEIGHT = 80
SPRITE_CROP_WIDTH = 79
SPRITE_CROP_HEIGHT = 79

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Parameters
INIT_CROP_X_SEED = 4
MIN_CROP_X_SEED = 5
MAX_CROP_X_SEED = 7

STAY_CROP_SEED_STEP = 0
WALK_CROP_SEED_STEP = 1

STAY_SLEEP = 0
WALK_SLEEP = 1 / 12

SPRITE_STAY_STEP = 0
SPRITE_WALK_STEP = 10

INIT_ACTION = set()

# Calculate lambdas
crop_x = lambda seed: seed * SPRITE_WIDTH
crop_y = lambda seed: seed * SPRITE_HEIGHT

# Image lambdas
LEFT_WALK = lambda c: c.transpose(Image.FLIP_LEFT_RIGHT)


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        MODE,
        COLOR_DEPTH
    )

    background = BLACK

    clr_screen = lambda: screen.fill(background)

    dennis_bmp = Image.open('0.bmp')
    dennis_bmp = utils.transparent(dennis_bmp, (-1, -1, -1))

    # Initialize Params
    runtime_params = {
        'crop_seed_x': INIT_CROP_X_SEED,
        'crop_seed_step_x': STAY_CROP_SEED_STEP,
        'time_sleep': STAY_SLEEP,
        'crop_pos_x': 0,
        'crop_pos_y': 0,
        'sprite_pos_x': 0,
        'sprite_pos_y': 0,
        'sprite_step_x': SPRITE_STAY_STEP,
        'sprite_step_y': SPRITE_STAY_STEP,
    }

    actions = INIT_ACTION

    pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])
    
    def move_dennis():
        cropped = utils.get_crop(dennis_bmp, (79, 79), (runtime_params['crop_pos_x'], runtime_params['crop_pos_y']))

        for action in actions:
            cropped = action(cropped)

        dennis = pygame.image.frombuffer(
            cropped.tostring(),
            cropped.size,
            cropped.mode
        )
        clr_screen()
        screen.blit(dennis, (runtime_params['sprite_pos_x'], runtime_params['sprite_pos_y']))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                runtime_params['time_sleep'] = WALK_SLEEP
                runtime_params['crop_seed_x'] = MIN_CROP_X_SEED
                runtime_params['crop_seed_step_x'] = WALK_CROP_SEED_STEP

                if event.key == K_RIGHT:
                    runtime_params['sprite_step_x'] = SPRITE_WALK_STEP
                    actions.discard(LEFT_WALK)

                elif event.key == K_LEFT:
                    runtime_params['sprite_step_x'] = SPRITE_WALK_STEP * (-1)
                    actions.update([LEFT_WALK])

                elif event.key == K_UP:
                    runtime_params['sprite_step_y'] = SPRITE_WALK_STEP * (-1)

                elif event.key == K_DOWN:
                    runtime_params['sprite_step_y'] = SPRITE_WALK_STEP

            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    runtime_params['sprite_step_x'] = SPRITE_STAY_STEP
                
                elif event.key == K_UP or event.key == K_DOWN:
                    runtime_params['sprite_step_y'] = SPRITE_STAY_STEP
                
                if runtime_params['sprite_step_x'] + runtime_params['sprite_step_y'] == 0:
                    runtime_params['time_sleep'] = STAY_SLEEP
                    runtime_params['crop_seed_x'] = 0
                    runtime_params['crop_seed_step_x'] = 0

        if runtime_params['crop_seed_step_x'] > 0 and runtime_params['crop_seed_x'] >= MAX_CROP_X_SEED:
            runtime_params['crop_seed_step_x'] = WALK_CROP_SEED_STEP * (-1)
        elif runtime_params['crop_seed_step_x'] < 0 and runtime_params['crop_seed_x'] <= MIN_CROP_X_SEED:
            runtime_params['crop_seed_step_x'] = WALK_CROP_SEED_STEP

        runtime_params['crop_seed_x'] = runtime_params['crop_seed_x'] + runtime_params['crop_seed_step_x']
        runtime_params['crop_pos_x'] = runtime_params['crop_seed_x'] * SPRITE_WIDTH

        runtime_params['sprite_pos_x'] = runtime_params['sprite_pos_x'] + runtime_params['sprite_step_x']

        runtime_params['sprite_pos_y'] = runtime_params['sprite_pos_y']  + runtime_params['sprite_step_y']

        runtime_params['sprite_pos_x'] = min(runtime_params['sprite_pos_x'], SCREEN_WIDTH - 79)
        runtime_params['sprite_pos_x'] = max(runtime_params['sprite_pos_x'], 0)
        runtime_params['sprite_pos_y'] = min(runtime_params['sprite_pos_y'], SCREEN_HEIGHT - 90)
        runtime_params['sprite_pos_y'] = max(runtime_params['sprite_pos_y'], 0)
        time.sleep ( runtime_params['time_sleep'] )
        move_dennis()


if __name__ == '__main__':
    main()
