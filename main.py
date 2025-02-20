import pygame
from settings import SIZE, WIDTH, HEIGHT, FPS
from gui import Text, Button
from tile import Obstacle, BreakableObstacle
from entity import Tank, Enemy
import csv
import os

pygame.init()
surface = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Танки 2025')
pygame.display.set_icon(pygame.image.load('images/tanks/t34/t34_0.png'))
clock = pygame.time.Clock()
# переменная отвечает за окно, которое будет прогруженно следующим
# window = 0 - завершение программы
# window = 1 - стартовый экран
# window = 2 - окно запуска уровня и самого уровня
window = 1


def start_screen(surface):  # стартовый экран
    # логотип стартового экрана
    logo = Text(surface, (WIDTH // 2, HEIGHT // 4), 'Танки 2025', (4, 189, 59), (0, 125, 52), 100)
    # кнопки играть и выйти
    play_button = Button(surface, (WIDTH // 2, HEIGHT // 2), 'Играть', (250, 183, 0), (255, 210, 60), (180, 120, 0))
    quit_button = Button(surface, (WIDTH // 2, HEIGHT // 1.5), 'Выход', (204, 0, 0), (255, 0, 0), (120, 0, 0))

    background = pygame.image.load("images/menu.png").convert_alpha()
    back_rect = background.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    running = True
    while running:
        global window
        clock.tick(FPS)
        # отрисовка заднего фона
        surface.fill((0, 0, 0))
        surface.blit(background, back_rect)
        # отрисовка логотипа и кнопок
        logo.draw()
        play_button.draw(pygame.mouse.get_pos())
        quit_button.draw(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                window = 0
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            # перенаправляет на экран выбора уровня
            if play_button.is_click():
                running = False
                window = 2
            # завершает работу программы
            elif quit_button.is_click():
                running = False
                window = 0

        pygame.display.update()


def load_level(level_name, game_surface):  # загрузка уровня - формирует и возвращает группы спрайтов
    # группа для снарядов
    missiles_group = pygame.sprite.Group()
    # группа для спрайтов препятствий
    obstacles_group = pygame.sprite.Group()
    # группа для танков
    tanks_group = pygame.sprite.Group()
    # группа для частиц
    particles_group = pygame.sprite.Group()
    # указатель на игрока
    player = None
    # загружает уровень из csv файла в папке levels
    with open(f'levels/{level_name}', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar="'")
        for i, row in enumerate(reader):
            for j, col in enumerate(row):
                match col:
                    case 'm':
                        pos = j * 32, i * 32
                        obstacles_group.add(Obstacle(pos, missiles_group))
                    case 'l':
                        pos = j * 32, i * 32
                        obstacles_group.add(Obstacle(pos, missiles_group, 1))
                    case 'b':
                        pos = j * 32, i * 32
                        obstacles_group.add(BreakableObstacle(pos, missiles_group))
                    case 'w':
                        pos = j * 32, i * 32
                        obstacles_group.add(BreakableObstacle(pos, missiles_group, 1))
                    case 'p1':
                        pos = j * 32, i * 32
                        player = Tank(pos, game_surface, missiles_group, particles_group,
                                      obstacles_group)
                        tanks_group.add(player)
                    case 'p2':
                        pos = j * 32, i * 32
                        player = Tank(pos, game_surface, missiles_group, particles_group,
                                      obstacles_group, 1)
                        tanks_group.add(player)
                    case 'e1':
                        pos = j * 32, i * 32
                        tanks_group.add(Enemy(pos, game_surface, missiles_group, particles_group, obstacles_group,
                                              0, 2))
                    case 'e2':
                        pos = j * 32, i * 32
                        tanks_group.add(Enemy(pos, game_surface, missiles_group, particles_group, obstacles_group,
                                              1, 2))
    if player is None:
        raise FileNotFoundError('Ошибка при чтении сохранения')
    return missiles_group, obstacles_group, tanks_group, particles_group, player


def open_level(surface):  # экран выбора уровня
    global window
    # стрелки для выбора уровня и кнопка загрузки выбранного уровня
    left_button = Button(surface, (50, HEIGHT // 2), '<', (250, 183, 0), (255, 210, 60), (180, 120, 0))
    right_button = Button(surface, (WIDTH - 50, HEIGHT // 2), '>', (250, 183, 0), (255, 210, 60), (180, 120, 0))
    open_button = Button(surface, (WIDTH // 2, HEIGHT - 50), 'Запустить', (250, 183, 0), (255, 210, 60), (180, 120, 0))
    # список уровней в папке levels
    levels_list = os.listdir('levels')
    # индекс списка levels_list
    level_pointer = 0

    game_size = (704, 704)
    game_surface = pygame.surface.Surface(game_size)
    # загрузка групп спрайтов выбранного уровня
    missiles_group, obstacles_group, tanks_group, particles_group, player = load_level(
        levels_list[level_pointer], game_surface)
    # задний фон уровня
    background = pygame.image.load('images/tiles/asphalt.png').convert()

    running = True
    while running:
        clock.tick(FPS)

        surface.fill('black')
        surface.blit(game_surface, (288, 8))
        # отрисовка заднего фона выбранного уровня
        for x in range(0, 22):
            for y in range(0, 22):
                game_surface.blit(background, (x * 32, y * 32))
        # отрисовка нужных групп спрайтов
        tanks_group.draw(game_surface)
        obstacles_group.draw(game_surface)
        # отрисовка кнопок
        left_button.draw(pygame.mouse.get_pos())
        right_button.draw(pygame.mouse.get_pos())
        open_button.draw(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                window = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # выбирает следующий уровень, т.е. увеличивает индекс level_pointer на 1
                if left_button.is_click():
                    level_pointer = (level_pointer - 1) % len(levels_list)
                    missiles_group, obstacles_group, tanks_group, particles_group, player = load_level(
                        levels_list[level_pointer], game_surface)
                # выбирает предыдущий уровень, т.е. уменьшает индекс level_pointer на 1
                elif right_button.is_click():
                    level_pointer = (level_pointer + 1) % len(levels_list)
                    missiles_group, obstacles_group, tanks_group, particles_group, player = load_level(
                        levels_list[level_pointer], game_surface)
                # открывает выбранный уровень
                elif open_button.is_click():
                    running = False
                    level(surface, game_surface, missiles_group, obstacles_group, tanks_group, particles_group, player)

        pygame.display.update()


def level(surface, game_surface, missiles_group, obstacles_group, tanks_group, particles_group, player):  # уровень
    global window
    background = pygame.image.load('images/tiles/asphalt.png').convert()
    # таймер
    end_screen_delay = 0

    w, h = game_surface.get_size()
    pos = (w // 2, h // 2)
    # конечные заставки победы и поражения
    end_victory_text = Text(game_surface, pos, 'ПОБЕДА', (25, 255, 25), (0, 179, 0))
    end_defeat_text = Text(game_surface, pos, 'ПОРАЖЕНИЕ', (255, 0, 0), (153, 0, 0))

    help_movement = Text(surface, (150, 100), 'Управление:WASD', (255, 255, 255), (100, 100, 100), 30)
    help_shoot = Text(surface, (150, 150), 'Стрельба:SPACE', (255, 255, 255), (100, 100, 100), 30)
    # счетчик оставшихся противников
    enemy_counter = Text(surface, (WIDTH - 150, 100), f'Враги: {str(len(tanks_group) - 1)}', (255, 255, 255),
                         (100, 100, 100), 30, (-3, -3))
    hp_counter = Text(surface, (WIDTH - 150, 200), f'Жизни: {player.get_hp()}', (255, 0, 0),
                      (153, 0, 0), 30, (-3, -3))

    running = True
    while running:
        clock.tick(FPS)

        surface.fill('black')
        surface.blit(game_surface, (288, 8))
        # отрисовка заднего фона уровня
        for x in range(0, 22):
            for y in range(0, 22):
                game_surface.blit(background, (x * 32, y * 32))
        # отрисовка спрайтов
        tanks_group.draw(game_surface)
        obstacles_group.draw(game_surface)
        missiles_group.draw(game_surface)
        particles_group.draw(game_surface)
        help_movement.draw()
        help_shoot.draw()
        enemy_counter.draw()
        hp_counter.draw()
        # обновление спрайтов
        tanks_group.update()
        obstacles_group.update()
        missiles_group.update()
        particles_group.update()
        # обновление счетчика врагов
        enemy_counter.change_text(f'Враги: {str(len(tanks_group) - 1)}')
        hp_counter.change_text(f'Жизни: {player.get_hp()}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                window = 0

        keys = pygame.key.get_pressed()
        if player.is_alive():
            # движение танка
            if keys[pygame.K_w]:
                player.move(pygame.K_w)
            elif keys[pygame.K_a]:
                player.move(pygame.K_a)
            elif keys[pygame.K_s]:
                player.move(pygame.K_s)
            elif keys[pygame.K_d]:
                player.move(pygame.K_d)
            if keys[pygame.K_SPACE]:
                player.shoot()
        # заканчивает уровень, если игрок умер или все враги были повержены
        if not player.is_alive():
            # если игрок умер, отрисовывает текст о поражении и через время возвращает на главный экран
            if end_screen_delay < 100:
                end_defeat_text.draw()
                end_screen_delay += 1
            else:
                running = False
                window = 1
        elif len(tanks_group) < 2:
            # если все враги были повержены, отрисовывает текст о победе и через время возвращает на главный экран
            if end_screen_delay < 100:
                end_victory_text.draw()
                end_screen_delay += 1
            else:
                running = False
                window = 1

        pygame.display.update()


def main():  # главная функция, идея взята из C
    while window:
        if window == 1:
            start_screen(surface)
        elif window == 2:
            open_level(surface)
    pygame.quit()


if __name__ == '__main__':
    main()
