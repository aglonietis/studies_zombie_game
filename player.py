import creature
import pygame
import numpy as np
import constants as c
import bullet


class Player(creature.Creature):
    health = c.HEALTH
    points = 0
    movement_keys = (
        pygame.K_DOWN,
        pygame.K_UP,
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_SPACE
    )
    bullets = None

    currentTick = 0

    keys = np.array(movement_keys).flatten()

    default_icon = pygame.image.load('resources/default/characterIcon.png')
    default_x = c.WIDTH / 2 - default_icon.get_width()
    default_y = c.HEIGHT / 2 - default_icon.get_height()

    def __init__(self):
        super(Player, self).__init__(
            self.default_icon.get_width(),
            self.default_icon.get_height(),
            self.default_x,
            self.default_y,
            self.default_icon
        )
        self.health = c.HEALTH
        self.points = 0
        self.bullets = []
        self.direction = c.MOVEMENT_UP

    def act(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.movement_keys:
                self.start_move(event.key)
            if event.key == pygame.K_SPACE:
                self.fire()
        if event.type == pygame.KEYUP:
            if event.key in self.movement_keys:
                self.stop_move(event.key)

    def start_move(self, key):
        self.move(key, True)

    def stop_move(self, key):
        self.move(key, False)

    def move(self, key, is_moving):
        if key == pygame.K_DOWN:
            self.move_down(is_moving)
            self.set_direction(c.MOVEMENT_DOWN,is_moving)
        if key == pygame.K_UP:
            self.move_up(is_moving)
            self.set_direction(c.MOVEMENT_UP, is_moving)
        if key == pygame.K_LEFT:
            self.move_left(is_moving)
            self.set_direction(c.MOVEMENT_LEFT, is_moving)
        if key == pygame.K_RIGHT:
            self.move_right(is_moving)
            self.set_direction(c.MOVEMENT_RIGHT,is_moving)

    def injure(self, health_to_substract):
        self.health -= health_to_substract

    def set_direction(self, direction, is_moving):
        if is_moving:
            self.direction = direction

    def draw_info(self, screen, my_font):
        textPoints = my_font.render("Current Points: %d" % (self.points,), False, c.TEXT_COLOR)
        textHealth = my_font.render("Current Health: %d" % (self.health,), False, c.TEXT_COLOR)
        screen.blit(textHealth, (0, 0))
        screen.blit(textPoints, (0, 30))

    def run(self, screen):
        self.currentTick += 1
        if self.currentTick >= c.PLAYER_TICKS_PER_ACT:
            self.currentTick = 0
            self.tick()

        self.draw(screen)
        for old_bullet in self.bullets:
            old_bullet.run(screen)
            if old_bullet.moved == False:
                self.bullets.remove(old_bullet)

    def fire(self):
        new_bullet = bullet.Bullet(self.position.get(c.AXIS_X), self.position.get(c.AXIS_Y))
        direction_set = False
        if self.directionalMovements[c.MOVEMENT_DOWN].is_moving and not self.directionalMovements[c.MOVEMENT_UP].is_moving:
            new_bullet.set_direction(c.MOVEMENT_DOWN)
            direction_set = True
        if not self.directionalMovements[c.MOVEMENT_DOWN].is_moving and self.directionalMovements[c.MOVEMENT_UP].is_moving:
            new_bullet.set_direction(c.MOVEMENT_UP)
            direction_set = True
        if self.directionalMovements[c.MOVEMENT_LEFT].is_moving and not self.directionalMovements[c.MOVEMENT_RIGHT].is_moving:
            new_bullet.set_direction(c.MOVEMENT_LEFT)
            direction_set = True
        if not self.directionalMovements[c.MOVEMENT_LEFT].is_moving and self.directionalMovements[c.MOVEMENT_RIGHT].is_moving:
            new_bullet.set_direction(c.MOVEMENT_RIGHT)
            direction_set = True
        if not direction_set:
            new_bullet.set_direction(self.direction)

        self.bullets.append(new_bullet)

    def calculate_killed(self, zombies):
        zombies_killed = []
        for old_zombie in zombies.zombies:
            for old_bullet in self.bullets:
                if old_zombie.position.distance(old_bullet.position) < c.MOVEMENT_TOUCH_INDEX * c.MOVEMENT:
                    self.bullets.remove(old_bullet)
                    self.points += 1
                    zombies_killed.append(old_zombie)
                    break
        return zombies_killed
