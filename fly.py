import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
import random
import config

from classes.player import Player
from classes.enemy import Enemy
from classes.cloud import Cloud

# set up for sounds. initialize only when defaults need to be changed
# pygame.mixer.init()
pygame.init()
# set up a game window
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.CAPTION)

# load and play background music
# sound source: http://ccmixter.org/files/Apoxode/59262
# license: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# load all sound files
# sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("sounds/Collision.ogg")

# custom event to create enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# custom event to create cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 1000)

# sprite group to hold enemies
enemies = pygame.sprite.Group()

# sprite group to hold all sprites, used for rendering
all_sprites = pygame.sprite.Group()

# sprite group to hold clouds
clouds = pygame.sprite.Group()

# set up clock to configure frame rate
clock = pygame.time.Clock()

player = Player()
all_sprites.add(player)

# flag to keep window running
keepRunning = True

while keepRunning:
    for event in pygame.event.get():
        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                keepRunning = False

        elif event.type == QUIT:
            keepRunning = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    # fill the screen with sky blue color
    screen.fill((135, 206, 250))

    # draw all sprites
    for entity in all_sprites:
        # blit/copy (Block Transfer) surf to screen, place it at the center
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        # move_up_sound.stop()
        # move_down_sound.stop()
        collision_sound.play()
        keepRunning = False

    # update the display
    pygame.display.flip()

    # ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# stop all sounds
pygame.mixer.music.stop()
pygame.mixer.quit()
