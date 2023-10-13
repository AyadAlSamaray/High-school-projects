import pygame.time
from spritesheet import Spritesheet
from Entity import Entity
from Entity import Actor
import pygame

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 810
FRAME_RATE = 60
white = (255, 255, 255)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    level_1(screen)
    # more levels go here

    return


def update_animation(player, animation_num, animations):
    player.surface = animations[animation_num]
    player.mask = pygame.mask.from_surface(player.surface)
    return


def scale_all_images(images, scale_x, scale_y):
    scaled_images = []
    for image in images:
        scaled_images += [pygame.transform.scale(image, (scale_x, scale_y))]
    return scaled_images


def level_1(screen):
    # set up level
    surface = pygame.image.load("map.png")
    surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    level_map = Entity(surface, screen, 0, 0)
    level_map.surface.set_colorkey(white)

    # we need a way to represent regardless of whether the key has been found

    #

    # a key for the player to grab
    key_image = pygame.image.load("key.png")
    key_image = pygame.transform.scale(key_image, (50, 50))
    key = Entity(key_image, screen, 0, 0)
    key.rect.center = 199, 772

    # the player
    player_image = pygame.image.load("image1.png")
    player_image = pygame.transform.scale(player_image, (75, 75))
    player = Actor(player_image, screen, 5, 5, 10, 10)
    player.rect.center = (10, 10)
    moving_animation_num = 0
    idle_animation_num = 0
    moving_animations = [pygame.image.load("moving_image0.png"), pygame.image.load("moving_image1.png"),
                         pygame.image.load("moving_image2.png"), pygame.image.load("moving_image3.png"),
                         pygame.image.load("moving_image5.png"), pygame.image.load("moving_image6.png"),
                         pygame.image.load("moving_image7.png")]

    idle_animations = [pygame.image.load("image0.png"), pygame.image.load("image1.png")]
    moving_animations = scale_all_images(moving_animations, 152, 120)
    idle_animations = scale_all_images(idle_animations, 152, 120)

    entities = []

    left = False
    right = False
    up = False
    down = False
    # run the level
    clock = pygame.time.Clock()
    frame_count = 0
    running = True
    while running:
        clock.tick(FRAME_RATE)
        frame_count += 1
        screen.fill(white)
        # update entities
        level_map.draw()
        key.draw()
        player.draw()

        # update the screen
        pygame.display.update()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                left = True
            else:
                left = False
            if keys[pygame.K_RIGHT]:
                right = True
            else:
                right = False
            if keys[pygame.K_UP]:
                up = True
            else:
                up = False
            if keys[pygame.K_DOWN]:
                down = True
            else:
                down = False
            if event.type == pygame.QUIT:
                running = False

        # move player

        if left or right or up or down:
            if frame_count % 5 == 0:
                moving_animation_num += 1
            update_animation(player, moving_animation_num % len(moving_animations), moving_animations)
        else:
            if frame_count % 10 == 0:
                idle_animation_num += 1
            update_animation(player, idle_animation_num % len(idle_animations), idle_animations);
        if left:
            player.move_left()
        if right:
            player.move_right()
        if up:
            player.move_up()
        if down:
            player.move_down()
    return


def print_mouse_position():
    print(pygame.mouse.get_pos())
    return


if __name__ == '__main__':
    main()
