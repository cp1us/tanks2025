# файл для хранения классов интерфейса
import pygame
from settings import SIZE

pygame.init()
pygame.display.set_mode(SIZE)


class Text:  # класс создает и отображает текст и его тень
    def __init__(self, surface, pos, string, text_colour, shadow_colour, size=50, shadow=(-5, -5)):
        # размер текста
        self.size = size
        # ссылка объект класса surface для отрисовки текста
        self.surface = surface
        # позиция центра текста
        self.pos_x, self.pos_y = pos
        # позиция центра тени текста
        self.shadow_pos = self.pos_x + shadow[0], self.pos_y + shadow[1]
        # цвет самого текста и его тени
        self.text_colour = text_colour
        self.shadow_colour = shadow_colour

        self.font = pygame.font.Font('fonts/HomeVideo-Regular.otf', self.size)

        self.text = self.font.render(string, True, self.text_colour)
        self.text_shadow = self.font.render(string, True, self.shadow_colour)
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        self.shadow_rect = self.text.get_rect(center=self.shadow_pos)

    def draw(self):  # метод для отрисовки текста
        self.surface.blit(self.text_shadow, self.shadow_rect)
        self.surface.blit(self.text, self.text_rect)

    def change_text(self, string):  # метод для изменения текста
        self.text = self.font.render(string, True, self.text_colour)
        self.text_shadow = self.font.render(string, True, self.shadow_colour)
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        self.shadow_rect = self.text.get_rect(center=self.shadow_pos)


class Button:  # класс, создает кнопку.
    FONT = pygame.font.Font('fonts/HomeVideo-Regular.otf', 50)

    def __init__(self, surface, pos, string, text_colour, aim_colour, shadow_colour, shadow=(-3, -3)):
        self.surface = surface
        # позиция центра текста
        self.pos_x, self.pos_y = pos
        # флаг, показывающий, навелись ли на тект курсором мыши.
        self.is_aim = False
        # позиция центра тени
        shadow_pos = self.pos_x + shadow[0], self.pos_y + shadow[1]

        self.text_aim = self.render(string, aim_colour)
        self.text = self.render(string, text_colour)
        self.text_shadow = self.render(string, shadow_colour)

        self.aim_rect = self.text_aim.get_rect(center=(self.pos_x, self.pos_y))
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        self.shadow_rect = self.text.get_rect(center=shadow_pos)

    @classmethod
    def render(cls, string, colour):  # метод для удобного рендера текста
        text = cls.FONT.render(string, True, colour)
        return text

    def draw(self, mouse_pos):  # отрисовка кнопки
        self.surface.blit(self.text_shadow, self.shadow_rect)
        if self.text_rect.collidepoint(mouse_pos):
            self.surface.blit(self.text_aim, self.aim_rect)
            # ставит флаг равным True, если пользователь навелся мышкой на кнопку.
            self.is_aim = True
        else:
            self.surface.blit(self.text, self.text_rect)
            self.is_aim = False

    def is_click(self):  # возвращает значение self.is_aim
        return self.is_aim
