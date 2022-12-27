import creature
import pygame
import constants as c


class Bullet (creature.Creature):

    default_icon = pygame.image.load('resources/default/bulletIcon.png')

    moved = True

    def __init__(self, x, y):
        super(Bullet, self).__init__(
            self.default_icon.get_width(),
            self.default_icon.get_height(),
            x,
            y,
            self.default_icon)
        self.moved = True

    def run(self, screen):
        self.moved = self.tick()
        self.draw(screen)

    def set_direction(self, direction):
        if direction == c.MOVEMENT_DOWN:
            self.move_down(True)
        if direction == c.MOVEMENT_UP:
            self.move_up(True)
        if direction == c.MOVEMENT_LEFT:
            self.move_left(True)
        if direction == c.MOVEMENT_RIGHT:
            self.move_right(True)

