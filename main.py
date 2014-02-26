#/usr/bin/python
from __future__ import division
from sys import exit
import time

from PIL import Image
import pygame
from pygame.locals import *

import utils

SPRITE_FOLDER = 'sprites/sys/'

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
INIT_CROP_X_SEED = 0

MIN_WALK_CROP_X_SEED = 4
MAX_WALK_CROP_X_SEED = 7
MIN_WALK_CROP_Y_SEED = 0
MAX_WALK_CROP_Y_SEED = 0

MIN_ATTCK_CROP_X_SEED = 0
MAX_ATTCK_CROP_X_SEED = 1
MIN_ATTCK_CROP_Y_SEED = 1
MAX_ATTCK_CROP_Y_SEED = 1


STAY_CROP_SEED_STEP = 0
WALK_CROP_SEED_STEP = 1
ATTCK_CROP_SEED_STEP = 1

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

# Control Keys
UP_KEY = K_w
DOWN_KEY = K_s
LEFT_KEY = K_a
RIGHT_KEY = K_d
ATTACK_KEY = K_j


MOVE_KEYS = (UP_KEY, DOWN_KEY, LEFT_KEY, RIGHT_KEY)


def main():

    def calculate_crop():
        rtp['crop_seed_x'] = rtp['crop_seed_x'] + rtp['crop_seed_step_x']
        rtp['crop_pos_x'] = crop_x(rtp['crop_seed_x'])
        rtp['crop_seed_y'] = rtp['crop_seed_y'] + rtp['crop_seed_step_y']
        rtp['crop_pos_y'] = crop_x(rtp['crop_seed_y'])

    def transform_walking():
        rtp['loop_actions'].update([move_dennis])
        rtp['time_sleep'] = WALK_SLEEP
        rtp['crop_seed_x'] = MIN_WALK_CROP_X_SEED
        rtp['crop_seed_step_x'] = WALK_CROP_SEED_STEP

    def walk_left():
        rtp['sprite_step_x'] = SPRITE_WALK_STEP * (-1)
        actions.update([LEFT_WALK])

    def walk_right():
        rtp['sprite_step_x'] = SPRITE_WALK_STEP
        actions.discard(LEFT_WALK)

    def walk_up():
        rtp['sprite_step_y'] = SPRITE_WALK_STEP * (-1)

    def walk_down():
        rtp['sprite_step_y'] = SPRITE_WALK_STEP

    def stop():
        rtp['time_sleep'] = STAY_SLEEP
        rtp['crop_seed_x'] = 0
        rtp['crop_seed_step_x'] = 0


    def walking_crop_seed_step():
        rtp['crop_seed_y'] = 0
        if rtp['crop_seed_step_x'] > 0 and rtp['crop_seed_x'] >= MAX_WALK_CROP_X_SEED:
            rtp['crop_seed_step_x'] = WALK_CROP_SEED_STEP * (-1)
        elif rtp['crop_seed_step_x'] < 0 and rtp['crop_seed_x'] <= MIN_WALK_CROP_X_SEED:
            rtp['crop_seed_step_x'] = WALK_CROP_SEED_STEP

    def attcking_crop_seed_step():
        if rtp['crop_seed_step_x'] > 0 and rtp['crop_seed_x'] >= MAX_ATTCK_CROP_X_SEED:
            rtp['crop_seed_step_x'] = ATTCK_CROP_SEED_STEP * (-1)
        elif rtp['crop_seed_step_x'] < 0 and rtp['crop_seed_x'] <= MIN_ATTCK_CROP_X_SEED:
            rtp['crop_seed_step_x'] = ATTCK_CROP_SEED_STEP


    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        MODE,
        COLOR_DEPTH
    )

    background = BLACK

    clr_screen = lambda: screen.fill(background)

    dennis_bmp = Image.open(SPRITE_FOLDER + 'louis_0.bmp')
    dennis_bmp = utils.transparent(dennis_bmp, (-1, -1, -1))

    # Initialize Params
    runtime_params = {
        'crop_seed_x': INIT_CROP_X_SEED,
        'crop_seed_step_x': STAY_CROP_SEED_STEP,
        'crop_seed_y': 0,
        'crop_seed_step_y': 0,
        'time_sleep': STAY_SLEEP,
        'crop_pos_x': 0,
        'crop_pos_y': 0,
        'sprite_pos_x': 0,
        'sprite_pos_y': 0,
        'sprite_step_x': SPRITE_STAY_STEP,
        'sprite_step_y': SPRITE_STAY_STEP,
        'crop_seed_step_func': walking_crop_seed_step,
        'loop_actions': set(),
    }
    rtp = runtime_params

    actions = INIT_ACTION

    pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])

    def move_dennis():
        rtp['crop_seed_step_func']()
        calculate_crop()
        rtp['sprite_pos_x'] = rtp['sprite_pos_x'] + rtp['sprite_step_x']
        rtp['sprite_pos_y'] = rtp['sprite_pos_y']  + rtp['sprite_step_y']
        rtp['sprite_pos_x'] = min(rtp['sprite_pos_x'], SCREEN_WIDTH - 79)
        rtp['sprite_pos_x'] = max(rtp['sprite_pos_x'], 0)
        rtp['sprite_pos_y'] = min(rtp['sprite_pos_y'], SCREEN_HEIGHT - 90)
        rtp['sprite_pos_y'] = max(rtp['sprite_pos_y'], 0)
        cropped = utils.get_crop(
            img=dennis_bmp,
            size=(79, 79),
            xy=(rtp['crop_pos_x'], rtp['crop_pos_y'])
        )
        for action in actions:
            cropped = action(cropped)

        dennis = pygame.image.frombuffer(
            cropped.tostring(),
            cropped.size,
            cropped.mode
        )
        clr_screen()
        screen.blit(
            dennis,
            (rtp['sprite_pos_x'], rtp['sprite_pos_y'])
        )
        time.sleep ( rtp['time_sleep'] )


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:

                if event.key in MOVE_KEYS:
                    transform_walking()

                if event.key == RIGHT_KEY:
                    walk_right()

                elif event.key == LEFT_KEY:
                    walk_left()

                if event.key == UP_KEY:
                    walk_up()

                elif event.key == DOWN_KEY:
                    walk_down()

                if event.key == ATTACK_KEY:
                    do_attck()

            elif event.type == KEYUP:
                if event.key == RIGHT_KEY or event.key == LEFT_KEY:
                    rtp['sprite_step_x'] = SPRITE_STAY_STEP
                
                elif event.key == UP_KEY or event.key == DOWN_KEY:
                    rtp['sprite_step_y'] = SPRITE_STAY_STEP
                
                if rtp['sprite_step_x'] + rtp['sprite_step_y'] == 0:
                    stop()

        for action in rtp['loop_actions']:
            action()
        pygame.display.update()


if __name__ == '__main__':
    main()
