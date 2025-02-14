# файл для хранения классов, отвественных за частицы
import pygame
from settings import SIZE

pygame.init()
pygame.display.set_mode(SIZE)


class Smoke(pygame.sprite.Sprite):  # партикл дыма
    IMAGES = (pygame.image.load('images/particles/smoke/smoke0.png').convert_alpha(),
              pygame.image.load('images/particles/smoke/smoke1.png').convert_alpha(),
              pygame.image.load('images/particles/smoke/smoke2.png').convert_alpha(),
              pygame.image.load('images/particles/smoke/smoke3.png').convert_alpha(),
              pygame.image.load('images/particles/smoke/smoke4.png').convert_alpha(),)

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.delay = 5
        self.counter = 0
        self.texture = 0

        self.image = self.IMAGES[self.texture]
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, *args, **kwargs):
        if self.counter == self.delay:
            self.counter = 0
            self.texture += 1
            if self.texture < 5:
                self.image = self.IMAGES[self.texture]
                self.rect = self.image.get_rect(center=self.pos)
            else:
                self.kill()
        self.counter += 1


class Explosion(pygame.sprite.Sprite):  # партикл взрыва
    IMAGES = (pygame.image.load('images/particles/explosion/explosion0.png').convert_alpha(),
              pygame.image.load('images/particles/explosion/explosion1.png').convert_alpha(),
              pygame.image.load('images/particles/explosion/explosion2.png').convert_alpha(),
              pygame.image.load('images/particles/explosion/explosion3.png').convert_alpha(),
              pygame.image.load('images/particles/explosion/explosion4.png').convert_alpha(),
              pygame.image.load('images/particles/explosion/explosion5.png').convert_alpha(),
              pygame.image.load('images/particles/explosion/explosion6.png').convert_alpha(),)
    EXPLODE_SOUND = pygame.mixer.Sound('audio/sounds/explode.wav')

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.delay = 2
        self.counter = 0
        self.texture = 0

        self.image = self.IMAGES[self.texture]
        self.rect = self.image.get_rect(center=self.pos)

        self.EXPLODE_SOUND.play()

    def update(self, *args, **kwargs):
        if self.counter == self.delay:
            self.counter = 0
            self.texture += 1
            if self.texture < 7:
                self.image = self.IMAGES[self.texture]
                self.rect = self.image.get_rect(center=self.pos)
            else:
                self.kill()
        self.counter += 1
