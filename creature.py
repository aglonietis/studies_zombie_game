import constants as c
import object


class Creature (object.Object):
    def __init__(self, width, height, x, y, image):
        super(Creature, self).__init__(width, height, x, y, image)

    def run(self, screen):
        self.tick()
        self.draw(screen)

    def move_left(self, is_moving):
        self.directionalMovements[c.MOVEMENT_LEFT].is_moving = is_moving

    def move_right(self, is_moving):
        self.directionalMovements[c.MOVEMENT_RIGHT].is_moving = is_moving

    def move_up(self, is_moving):
        self.directionalMovements[c.MOVEMENT_UP].is_moving = is_moving

    def move_down(self, is_moving):
        self.directionalMovements[c.MOVEMENT_DOWN].is_moving = is_moving
