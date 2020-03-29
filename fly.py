import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random

# set up for sounds. initialize only when defaults need to be changed
# pygame.mixer.init()

pygame.init()
pygame.display.set_caption("This Is A Flying Game")

# set up clock to configure frame rate
clock = pygame.time.Clock()

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

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 300


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        # move_ip = move in place
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            # move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            # move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/enemy.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)

        if self.rect.right < 0:
            self.kill()


# custom event to create enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# custom event to create cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 1000)

# set up a game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player()

# sprite group to hold enemies
enemies = pygame.sprite.Group()

# sprite group to hold all sprites, used for rendering
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# sprite group to hold clouds
clouds = pygame.sprite.Group()

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
