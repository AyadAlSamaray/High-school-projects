import pygame
import random
import math


class Entity:
    def __init__(self, surface, screen: pygame.display, x_vel: float, y_vel: float):

        # Assign fields from parameters
        self.surface = surface
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.screen = screen

        # Generate the rest of the fields
        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.from_surface(self.surface)
        return

    def is_colliding_with(self, other):
        # returns True if this Entity is colliding with other Entity, False otherwise
        offset_x = other.rect[0] - self.rect[0]
        offset_y = other.rect[1] - self.rect[1]

        are_overlapping = self.mask.overlap(other.mask, (offset_x, offset_y))
        return are_overlapping

    def move_randomly(self):
        x_change = random.randint(int(-self.x_vel), int(self.x_vel))
        y_change = random.randint(int(-self.y_vel), int(self.y_vel))

        # try to move, only if it won't go off of the screen
        if not (self.rect.bottom + y_change >= self.screen.get_height() or self.rect.top + y_change <= 0
                or self.rect.right + x_change >= self.screen.get_width() or self.rect.left + x_change <= 0):
            self.rect.move_ip(x_change, y_change)

    def move_towards_point(self, x, y):
        delta_x = x - self.rect.center[0]
        delta_y = y - self.rect.center[1]

        if delta_x == 0:
            delta_x = 1

        if delta_y == 0:
            delta_y = 1

        theta = math.atan(delta_y / delta_x)

        x_move = self.x_vel * math.cos(theta)
        y_move = self.y_vel * math.sin(theta)

        if delta_x < 0:
            x_move *= -1
            y_move *= -1

        self.rect.move_ip(x_move, y_move)
        return

    def move_towards_entity(self, other):
        self.move_towards_point(other.rect.center[0], other.rect.center[1])
        return

    def move_left(self):
        self.rect.move_ip(-self.x_vel, 0)

    def move_right(self):
        self.rect.move_ip(self.x_vel, 0)

    def move_up(self):
        self.rect.move_ip(0, -self.y_vel)

    def move_down(self):
        self.rect.move_ip(0, self.y_vel)

    def draw(self):
        self.screen.blit(self.surface, self.rect)
        return

    def distance_to(self, target):
        delta_x = target.rect.center[0] - self.rect.center[0]
        delta_y = target.rect.center[1] - self.rect.center[1]

        return math.sqrt((delta_x ** 2) + (delta_y ** 2))


class Actor(Entity):
    def __init__(self, surface, x_vel: float, y_vel: float, screen: pygame.display,
                 base_health, attack_damage):
        super().__init__(surface, x_vel, y_vel, screen)
        self.base_health = base_health
        self.attack_damage = attack_damage
        return

    def attack(self, other):
        other.health -= self.attack_damage
        return

    def take_damage(self, damage_amount):
        self.base_health -= damage_amount
        return
