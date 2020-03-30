import pygame
from pygame.locals import RLEACCEL
import random
import config


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(config.SCREEN_WIDTH + 20, config.SCREEN_WIDTH + 100),
                random.randint(0, config.SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)

        if self.rect.right < 0:
            self.kill()
