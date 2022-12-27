import zombie
import random
import dimension
import constants as c


class ZombieHorde:
    zombies = ()

    spawn_zombie_tick = 0

    def __init__(self):
        self.zombies = []
        random.seed(1)
        self.spawn_zombie_tick = 0

    def run(self, screen, player):
        if self.spawn_zombie_tick >= c.ZOMBIE_TICKS_TO_SPAWN:
            self.spawn_zombie_tick = 0
            self.spawn_random()
        else:
            self.spawn_zombie_tick += 1

        for activeZombie in self.zombies:
            activeZombie.act(player)
            activeZombie.run(screen)

    def spawn_random(self):
        cord_x = int(random.random() * dimension.DIMENSIONS.get(c.AXIS_X))
        cord_y = int(random.random() * dimension.DIMENSIONS.get(c.AXIS_Y))
        random_factor = int(random.random() * 4)
        if random_factor == 3:
            cord_x = 0
        elif random_factor == 2:
            cord_x = c.WIDTH
        elif random_factor == 1:
            cord_y = 0
        else:
            cord_y = c.HEIGHT


        if c.MAX_ZOMBIES > len(self.zombies):
            new_zombie = zombie.Zombie(cord_x, cord_y)
            self.zombies.append(new_zombie)

    def check(self, player):
        health_reduced = 0

        for old_zombie in self.zombies:
            if old_zombie.position.distance(player.position) < c.MOVEMENT * c.MOVEMENT_TOUCH_INDEX:
                self.zombies.remove(old_zombie)
                health_reduced += 1
        return health_reduced

    def remove_killed(self, zombies_to_remove):
        for zombie_to_remove in zombies_to_remove:
            self.zombies.remove(zombie_to_remove)





