import constants as c


class Dimension:
    dimension = {
        c.AXIS_X: 0,
        c.AXIS_Y: 0
    }

    def __init__(self, x, y):
        self.dimension = {
            c.AXIS_X: x,
            c.AXIS_Y: y
        }

    def get(self, axis):
        return self.dimension[axis]


def create_dimension(x, y):
    dimension = Dimension(x, y)
    return dimension


DIMENSIONS = create_dimension(c.WIDTH, c.HEIGHT)
