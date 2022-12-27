import constants as c
import dimension as dim
import math

DIMENSIONS = dim.create_dimension(c.WIDTH, c.HEIGHT)


class Position:
    position = {
        c.AXIS_X: 0,
        c.AXIS_Y: 0
    }

    def __init__(self, x, y):
        self.position = {
            c.AXIS_X: x,
            c.AXIS_Y: y
        }

    def move(self, axis, value, dimensions):
        moved = False
        new_value = self.position[axis] + value
        max_value = dim.DIMENSIONS.get(axis) - dimensions.get(axis) / 2
        min_value = dimensions.get(axis) / 2
        if max_value >= new_value >= min_value:
            self.position[axis] += value
            moved = True
        if self.position[axis] >= new_value >= max_value:
            self.position[axis] += value
            moved = True
        if min_value >= new_value >= self.position[axis]:
            self.position[axis] += value
            moved = True
        return moved

    def coordinates(self):
        return self.position[c.AXIS_X], self.position[c.AXIS_Y]

    def screen_coordinates(self, dimensions):

        return (
            self.position[c.AXIS_X] - dimensions.get(c.AXIS_X) / 2,
            self.position[c.AXIS_Y] - dimensions.get(c.AXIS_Y) / 2
        )

    def get(self, axis):
        return self.position[axis]

    def distance(self, position):
        return int(math.sqrt(
            pow(self.get(c.AXIS_X) - position.get(c.AXIS_X), 2) +
            pow(self.get(c.AXIS_Y) - position.get(c.AXIS_Y), 2)
        ))


class DirectionalMovement:
    is_moving = False
    axis = c.AXIS_X
    value = 0

    def __init__(self, axis, value):
        self.is_moving = False
        self.axis = axis
        self.value = value


class Object:
    image = None
    dimensions = None
    position = None
    directionalMovements = None

    def __init__(self, width, height, x, y, image):
        self.position = Position(x, y)
        self.dimensions = dim.create_dimension(width, height)
        self.image = image
        self.directionalMovements = {
            c.MOVEMENT_LEFT: DirectionalMovement(c.AXIS_X, -c.MOVEMENT),
            c.MOVEMENT_RIGHT: DirectionalMovement(c.AXIS_X, c.MOVEMENT),
            c.MOVEMENT_UP: DirectionalMovement(c.AXIS_Y, -c.MOVEMENT),
            c.MOVEMENT_DOWN: DirectionalMovement(c.AXIS_Y, c.MOVEMENT)
        }

    def change_movement(self, movement, is_moving):
        self.directionalMovements[movement].is_moving = is_moving

    def tick(self):
        moved = False
        for directionalMovement in self.directionalMovements.values():
            if directionalMovement.is_moving:
                moving = self.position.move(directionalMovement.axis, directionalMovement.value, self.dimensions)
                if moving:
                    moved = True
        return moved

    def draw(self, screen):
        screen.blit(self.image, self.position.screen_coordinates(self.dimensions))

    def draw_image(self,screen,image):
        screen.blit(image, self.position.screen_coordinates(self.dimensions))

    def update_image(self, image):
        print('updating image')
        self.image = image
