# файл для хранения классов подвижных объектов
import pygame
from settings import SIZE
from particle import Explosion, Smoke
import random

pygame.init()
pygame.display.set_mode(SIZE)


class Missile(pygame.sprite.Sprite):  # снаряд от танка
    IMAGE = pygame.image.load('images/tanks/missile.png').convert_alpha()

    def __init__(self, pos, move_way, surface_size, particle_group, by_player=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.IMAGE
        self.rect = self.image.get_rect(center=pos)
        # направление движение снаряда
        self.move_x, self.move_y = move_way
        # границы экрана
        self.WIDTH, self.HEIGHT = surface_size
        # группа для партиклов
        self.particle_group = particle_group
        # флаг, показывает, был ли снаряд выпущен игроком. нужен, чтобы вражеские танки друг друга не перестреляли
        self.by_player = by_player
        # скорость снаряда
        self.speed = 7

    def is_player(self):  # возвращает значение флага self.by_player
        return self.by_player

    def kill(self):  # перед самоликвидацией снаряд кидает в группу particle_group частицы дыма
        self.particle_group.add(Smoke(self.rect.center))
        super().kill()

    def update(self, *args, **kwargs):
        pos_x, pos_y = self.rect.center
        # проверка выхода снаряда за границы экрана surface
        if 0 > pos_x or pos_x > self.WIDTH or 0 > pos_y or pos_y > self.HEIGHT:
            self.kill()
        else:
            self.rect.move_ip(self.move_x * self.speed, self.move_y * self.speed)


class Tank(pygame.sprite.Sprite):  # класс танка игрока
    IMAGES = (
        (pygame.image.load('images/tanks/t34/t34_0.png').convert_alpha(),
         pygame.image.load('images/tanks/t34/t34_1.png').convert_alpha()),
        (pygame.image.load('images/tanks/kv1/kv1_0.png').convert_alpha(),
         pygame.image.load('images/tanks/kv1/kv1_1.png').convert_alpha())
    )
    SHOOT_SOUND = pygame.mixer.Sound('audio/sounds/shoot.wav')

    def __init__(self, pos, surface, missiles_group, particles_group, obstacles_group, model=0, rotate=0):
        super().__init__()
        self.surface = surface
        self.surface_rect = surface.get_rect()
        # ссылка на группу спрайтов препядствий
        self.obstacles_group = obstacles_group
        # ссылка на группу спрайтов партиклов
        self.particles_group = particles_group
        # ссылка на группу спрайтов снарядов
        self.missiles_group = missiles_group
        # модель танкка, отвечает за хп и текстуру
        self.model = model
        # отвечает за текстуру гусениц
        self.track = 0
        # поворот танка
        # 0 - 0 градусов
        # 1 - 90 градусов
        # 2 - 180 градусов
        # 3 - 270 градусов
        self.rotate = rotate
        # скорость танка
        self.speed = 3 if self.model == 0 else 2
        # количество жизней танка, зависит от его модели
        self.hp = 1 + self.model
        # переменная отвечает за время перезарядки
        self.reload_rate = 100 - self.model * 10
        # переменная отвечает за текущую перезарядку танка
        self.gun_reload = 100 - self.model * 10
        # флаг нужен при выстреле для передачи его классу Missile
        self.fl_player = True

        self.image = pygame.transform.rotate(self.IMAGES[self.model][self.track], rotate * -90)
        self.rect = self.image.get_rect(topleft=pos)

    def hit(self):  # отнимает 1 хп при попадании вражеского снаряда
        self.hp -= 1

    def is_alive(self):  # возращает True, если танк жив, т.е. его hp > 0
        return self.hp > 0

    def get_hp(self):
        return self.hp

    def get_way(self, key):  # принимает ключ клавиши и относительно него возвращает сторону движения танка
        match key:
            case pygame.K_w:
                rotate = 0  # 0 градусов
                return 0, -1 * self.speed, rotate
            case pygame.K_d:
                rotate = 1  # 90 градусов
                return 1 * self.speed, 0, rotate
            case pygame.K_s:
                rotate = 2  # 180 градусов
                return 0, 1 * self.speed, rotate
            case pygame.K_a:
                rotate = 3  # 270 градусов
                return -1 * self.speed, 0, rotate
            case _:
                return 0, 0, 0

    def move(self, key):
        move_x, move_y, rotate = self.get_way(key)
        # временное сохранение текущих параметров
        tmp_image = self.image
        tmp_rect = self.rect
        tmp_rotate = self.rotate

        self.rotate = rotate
        self.image = pygame.transform.rotate(self.IMAGES[self.model][self.track], self.rotate * -90)
        self.rect = self.image.get_rect(center=(self.rect.centerx + move_x, self.rect.centery + move_y))
        self.rect.clamp_ip(self.surface_rect)
        # инвертирует битовую переменную track для смены текстуры гусеницы
        self.track = not self.track

        tank_collide = False
        for sprite in pygame.sprite.spritecollide(self, self.groups()[0], False):
            if sprite != self:
                tank_collide = True
                break
        # возвращает танк в изначальное положение, если была обнаружена коллизия со спрайтами
        # из tank_group или/и obstacles_group
        if tank_collide or pygame.sprite.spritecollideany(self, self.obstacles_group):
            self.image = tmp_image
            self.rect = tmp_rect
            self.rotate = tmp_rotate

    def shoot(self):  # метод, отвечающий за стрельбу танков
        if self.gun_reload == self.reload_rate:
            match self.rotate:
                case 0:
                    pos_x = self.rect.centerx
                    pos_y = self.rect.top - 5
                    move_way = 0, -1
                case 1:
                    pos_x = self.rect.right + 5
                    pos_y = self.rect.centery
                    move_way = 1, 0
                case 2:
                    pos_x = self.rect.centerx
                    pos_y = self.rect.bottom + 5
                    move_way = 0, 1
                case 3:
                    pos_x = self.rect.left - 5
                    pos_y = self.rect.centery
                    move_way = -1, 0

            missile = Missile((pos_x, pos_y), move_way, self.surface.get_size(), self.particles_group, self.fl_player)
            self.missiles_group.add(missile)
            # проигрывает звук выстрела
            self.SHOOT_SOUND.play()
            self.gun_reload = 0

    def update(self, *args, **kwargs):
        # при попадании снаряда по танку отнимает у него 1 хп
        if pygame.sprite.spritecollideany(self, self.missiles_group):
            pygame.sprite.spritecollide(self, self.missiles_group, True)
            self.hit()
        if not self.is_alive():
            self.kill()
        else:
            # перезарядка орудия
            if self.gun_reload != self.reload_rate:
                self.gun_reload += 1

    def kill(self):
        # до своего уничтожения кидает партикл взрыва в particles_group
        self.particles_group.add(Explosion(self.rect.center))
        super().kill()


class Enemy(Tank):  # бот-враг с рандомным интеллектом
    IMAGES = (
        (pygame.image.load('images/tanks/pz4/pz4_0.png').convert_alpha(),
         pygame.image.load('images/tanks/pz4/pz4_1.png').convert_alpha()),
        (pygame.image.load('images/tanks/tiger1/tiger1_0.png').convert_alpha(),
         pygame.image.load('images/tanks/tiger1/tiger1_1.png').convert_alpha())
    )
    MOVE_ACTIONS = ('move_up', 'move_right', 'move_down', 'move_left')

    def __init__(self, pos, surface, missiles_group, particles_group, obstacles_group, model=0, rotate=0):
        super().__init__(pos, surface, missiles_group, particles_group, obstacles_group, model, rotate)
        self.fl_player = False
        # массив - стак команд, которые последовательно будут выполняться объектом класса
        self.actions_stack = []

    def get_way(self, key):  # принимает ключ из MOVE_ACTIONS и относительно него возвращает сторону движения танка
        match key:
            case 'move_up':
                rotate = 0  # 0 градусов
                return 0, -1 * self.speed, rotate
            case 'move_right':
                rotate = 1  # 90 градусов
                return 1 * self.speed, 0, rotate
            case 'move_down':
                rotate = 2  # 180 градусов
                return 0, 1 * self.speed, rotate
            case 'move_left':
                rotate = 3  # 270 градусов
                return -1 * self.speed, 0, rotate
            case _:
                return 0, 0, 0

    def do(self, action):  # выполняет команды рандомного интеллекта
        if action in self.MOVE_ACTIONS:
            self.move(action)
        else:
            self.shoot()

    def update(self, *args, **kwargs):
        # проверка на попадание снаряда в танк, вызывает self.hit() только если снаряд был выпущен игроком
        for sprite in pygame.sprite.spritecollide(self, self.missiles_group, False):
            if sprite.is_player():
                sprite.kill()
                self.hit()
                break
        # уничтожает танк при hp < 1
        if self.hp < 1:
            self.kill()
        else:
            # блок, отвественный за рандомный интеллект
            if self.actions_stack:  # выполняет команду из массива только если сам массив не пустой
                self.do(self.actions_stack[0])
                del self.actions_stack[0]
            # флаг, предотвращает переполнение массива командами
            is_stack_free = len(self.actions_stack) < 40
            # перезарядка орудия
            if self.gun_reload != self.reload_rate:
                self.gun_reload += 1
            # если орудие перезарядилось, кидает в массив команду стрельбы в самое начало для немедленного выполнения
            # срабатывает, если массив не переполнен, т.е. его длина < 40
            elif is_stack_free:
                self.actions_stack.insert(0, 'shoot')
            # рандомная команда движения танка
            # срабатывает, если массив не переполнен, т.е. его длина < 40
            if is_stack_free:
                action = random.choice(self.MOVE_ACTIONS)
                for _ in range(15):
                    self.actions_stack.append(action)
