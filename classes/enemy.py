import pygame
from pygame.locals import RLEACCEL
import random
import config


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/enemy.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(config.SCREEN_WIDTH + 20, config.SCREEN_WIDTH + 100),
                random.randint(0, config.SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()
