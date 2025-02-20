# файл для хранения препятствий и декораций уровня
import pygame
from settings import SIZE

pygame.init()
pygame.display.set_mode(SIZE)


class Obstacle(pygame.sprite.Sprite):  # класс неразрушаемого препятствия
    IMAGES = (pygame.image.load('images/tiles/metalwall.png').convert_alpha(),
              pygame.image.load('images/tiles/water.png').convert_alpha())

    def __init__(self, pos, missiles_group, texture=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.IMAGES[texture]
        self.rect = self.image.get_rect(topleft=pos)
        # флаг отвечает за простреливаемость тайла
        self.hollow = True if texture == 0 else False

        # сохраняет ссылку на группу снарядов, чтобы разрушать снаряды при столкновении спрепятствием
        self.missiles_group = missiles_group

    def update(self, *args, **kwargs):  # уничтожает попавшие в объект снаряды
        if self.hollow:
            pygame.sprite.spritecollide(self, self.missiles_group, True)


class BreakableObstacle(pygame.sprite.Sprite):  # класс разрушаемого препятствия
    IMAGES = ((pygame.image.load('images/tiles/bricks_ruined.png').convert_alpha(),
               pygame.image.load('images/tiles/bricks.png').convert_alpha()),
              (pygame.image.load('images/tiles/wood2.png').convert_alpha(),
               pygame.image.load('images/tiles/wood1.png').convert_alpha()),
              )

    def __init__(self, pos, missiles_group, texture=0):
        pygame.sprite.Sprite.__init__(self)
        # тип текстуры объекта
        self.texture = texture
        # количество жизней объекта
        self.hp = 2
        # сохраняет ссылку на группу снарядов, чтобы разрушать снаряды при столкновении спрепятствием
        self.missiles_group = missiles_group

        self.image = self.IMAGES[texture][self.hp - 1]
        self.rect = self.image.get_rect(topleft=pos)

    def hit(self):  # отнимает у объекта 1 hp при попадании снаряда.
        self.hp -= 1
        self.image = self.IMAGES[self.texture][self.hp - 1]

    def update(self, *args, **kwargs):  # уничтожает попавшие в объект снаряды или уничтожается при hp < 1
        if pygame.sprite.spritecollideany(self, self.missiles_group):
            pygame.sprite.spritecollide(self, self.missiles_group, True)
            self.hit()
        if self.hp < 1:
            self.kill()
