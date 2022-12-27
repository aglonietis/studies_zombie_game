import creature
import pygame
import constants as c
import random
import os


def get_random_bool():
    return random.SystemRandom().randint(0, 100) > 50


class Zombie(creature.Creature):
    level = c.ZOMBIE_LEVEL_START

    default_icon = pygame.image.load('resources/default/zombieIcon.png')

    zombie_stages = [
        pygame.image.load('resources/default/zombieIcon.png'),
        pygame.image.load('resources/default/zombieIcon_medium.png'),
        pygame.image.load('resources/default/zombieIcon_fast.png')
    ]

    max_stage = len(zombie_stages) - 1

    ticksPerAct = c.ZOMBIE_TICKS_PER_ACT
    currentTick = 0

    upgradeTick = 0

    changingDirection = 0

    ticksPerImage = int(c.ZOMBIE_TICKS_PER_ACT / len(zombie_stages))

    movement_x = False
    movement_y = False

    def __init__(self, x, y):
        super(Zombie, self).__init__(
            self.default_icon.get_width(),
            self.default_icon.get_height(),
            x,
            y,
            self.default_icon)
        self.currentTick = 0
        self.changingDirection = 0
        self.movement_x = False
        self.movement_y = False

    def act(self, player):

        self.upgradeTick += 1
        self.currentTick += 1

        if int(self.upgradeTick / c.ZOMBIE_LEVEL_UP_TICK_COUNT) > self.level \
                and self.ticksPerAct > 1 \
                and random.random() > (1 - c.ZOMBIE_LEVEL_UP_CHANCE):
            self.level += 1

        self.ticksPerAct = c.ZOMBIE_TICKS_PER_ACT - self.level

        self.update_image_for_zombie(self.level)

        if self.currentTick >= self.ticksPerAct:
            self.currentTick = 0

            if self.position.distance(player.position) < c.ZOMBIE_DETECTION_DISTANCE:
                if self.position.get(c.AXIS_X) > player.position.get(c.AXIS_X):
                    self.move_left(True)
                    self.move_right(False)
                else:
                    self.move_left(False)
                    self.move_right(True)

                if self.position.get(c.AXIS_Y) > player.position.get(c.AXIS_Y):
                    self.move_up(True)
                    self.move_down(False)
                else:
                    self.move_up(False)
                    self.move_down(True)
            else:
                if self.changingDirection >= c.ZOMBIE_CHANGE_DIRECTION_TICK_COUNT:
                    self.movement_y = get_random_bool()
                    self.movement_x = get_random_bool()
                    self.changingDirection = 0
                else:
                    self.changingDirection += 1

                if self.movement_x:
                    self.move_left(True)
                    self.move_right(False)
                else:
                    self.move_left(False)
                    self.move_right(True)
                if self.movement_y:
                    self.move_up(True)
                    self.move_down(False)
                else:
                    self.move_up(False)
                    self.move_down(True)
        else:
            self.move_left(False)
            self.move_right(False)
            self.move_up(False)
            self.move_down(False)

    def update_image_for_zombie(self, level):

        zombie_stage = int(level / self.ticksPerImage)
        if zombie_stage > self.max_stage:
            zombie_stage = self.max_stage

        if self.image != self.zombie_stages[zombie_stage]:
            new_image = self.zombie_stages[zombie_stage]
            self.update_image(new_image)
