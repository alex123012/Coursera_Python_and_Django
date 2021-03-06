# -*- coding: utf-8 -*-
"""
Press F1 in game for support
"""

import pygame
import random
import math


class Vec2d:

    """Класс для работы с векторами"""

    def __init__(self, x=0, y=None):
        if y is None:
            self.tup = (x[0], x[1])
        else:
            self.tup = (x, y)

    def __str__(self):
        return f'({self.tup[0]}, {self.tup[1]})'

    def __repr__(self):
        return f'({self.tup[0]}, {self.tup[1]})'

    def __sub__(self, obj):

        """Возвращает разность двух векторов"""

        return Vec2d(self.tup[0] - obj.tup[0], self.tup[1] - obj.tup[1])

    def __add__(self, obj):

        """возвращает сумму двух векторов"""

        return Vec2d(self.tup[0] + obj.tup[0], self.tup[1] + obj.tup[1])

    def __iadd__(self, obj):

        """возвращает себя после прибавления оператором присваивания +="""

        self.tup = (self.tup[0]+obj.tup[0], self.tup[1]+obj.tup[1])
        return self

    def __len__(self):

        """возвращает длину вектора"""

        return int(math.hypot(self.tup[0], self.tup[1]))

    def __mul__(self, val):

        """возвращает произведение вектора на число или вектора на вектор"""

        if isinstance(val, Vec2d):
            return self.tup[0] * val.tup[0] + self.tup[1] * val.tup[1]
        return Vec2d(self.tup[0] * val, self.tup[1] * val)

    def __getitem__(self, x):

        """Работа с вектором как с коллекцией

           Получение значения по индексу"""

        return self.tup[x]

    def __setitem__(self, x):

        """Работа с вектором как с коллекцией

           Добавление значения (возвращает новый tuple)"""

        return self.tup + x

    def int_pair(self):

        """возвращает пару координат, определяющих вектор,
        координаты начальной точки вектора совпадают с (0, 0)"""

        return int(self.tup[0]), int(self.tup[1])


class Polyline:

    """Класс для апперирования замкнутыми ломанными"""

    def __init__(self, SCREEN_DIM=(800, 600), obj=None):
        self.points = [] if obj is None else obj.points
        self.speeds = [] if obj is None else obj.speeds
        self.SCREEN_DIM = SCREEN_DIM

    def __repr__(self):
        return f'{self.points}'

    def __str__(self):
        return f'{self.points}'

    def __add__(self, obj):

        """Добавление новой точки (либо точек другой линии) и скорости"""

        if isinstance(obj, Vec2d):
            self.points.append(obj)
            self.speed.append((random.random() * 2, random.random() * 2))
            return self

        elif isinstance(obj, Polyline):
            points = self.points + obj.points
            speeds = self.speeds + obj.speeds
            return Polyline(points, speeds)

    def __iadd__(self, obj):

        """Добавление новой точки (либо точек другой линии) и скорости"""

        if isinstance(obj, Vec2d):
            self.points.append(obj)
            self.speeds.append((random.random() * 2, random.random() * 2))
            return self

        elif isinstance(obj, Polyline):
            points = self.points + obj.points
            speeds = self.speeds + obj.speeds
            return Polyline(points, speeds)

    def append(self, point, speed):

        """Добавление координаты и скорости (дополнительный метод)"""

        self.points.append(point)
        self.speeds.append(speed)

    def dell_last_point(self):

        """Удаления последенй координаты"""

        if self.points and self.speeds:
            self.points.pop()
            self.speeds.pop()

    def slow_down(self):

        """Функция замедления движения точек"""

        self.speeds = [Vec2d(x[0] * 0.9, x[1] * 0.9) for x in self.speeds]
        # print(self.speeds)

    def fast_up(self):

        """Функция ускорения движения точек"""

        self.speeds = [Vec2d(x[0] * 1.1, x[1] * 1.1) for x in self.speeds]
        # print(self.speeds)

    def set_points(self):

        """функция перерасчета координат опорных точек"""

        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            # print(self.points[p])
            if self.points[p][0] > self.SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d(-self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > self.SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, gameDisplay, width=3, color=(255, 255, 255)):

        """Отрисовка опорных точек"""

        for p in self.points:
            pygame.draw.circle(gameDisplay, color, p.int_pair(), width)

    def clear(self):

        """Очистка точек кривой"""

        self.points = []
        self.speeds = []


class Knot(Polyline):

    def __init__(self, count, SCREEN_DIM=(800, 600)):
        super().__init__(SCREEN_DIM)
        self.count = count

    def set_points(self):
        super().set_points()
        self.get_knot()

    def append(self, val, speed):
        super().append(val, speed)
        self.get_knot()

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha)\
            + (self.__get_point(points, alpha, deg - 1) * (1 - alpha))

    def __get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(base_points, i * alpha))
        return res

    def get_knot(self):

        """Расчет точек кривой"""

        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.__get_points(ptn, self.count))
        return res

    def draw_line(self, gameDisplay, width=3, color=(255, 255, 255)):

        """Отрисовка точек кривой (линии) по опорным точкам)"""
        points = self.get_knot()
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(),
                             points[p_n + 1].int_pair(), width)


class Game:

    def __init__(self, SCREEN_DIM=(800, 600)):
        pygame.init()
        self.SCREEN_DIM = SCREEN_DIM
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

        self.count = 35
        self.working = True
        self.knots = []
        self.show_help = False
        self.pause = True
        self.i = -1

        self.hue = 0
        self.color = pygame.Color(0)

    def working_f(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.show_help:
                        self.working = False
                    else:
                        self.show_help = False
                if event.key == pygame.K_r:
                    self.knots[self.i].clear()
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_KP_PLUS:
                    self.knots[self.i].count += 1
                if event.key == pygame.K_F1:
                    self.show_help = not self.show_help
                if event.key == pygame.K_KP_MINUS:
                    p = self.knots[self.i]
                    self.knots[self.i].count -= 1 if p.count > 1 else 0
                if event.key == pygame.K_n:
                    self.make_new_knot()
                if event.key == pygame.K_d:
                    self.knots[self.i].dell_last_point()
                if event.key == pygame.K_l:
                    self.change_knot(0)
                if event.key == pygame.K_k:
                    self.change_knot(1)
                if event.key == pygame.K_j:
                    self.knots.pop()
                if event.key == pygame.K_s:
                    self.knots[self.i].slow_down()
                if event.key == pygame.K_f:
                    self.knots[self.i].fast_up()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(self.i)
                if not self.knots:
                    self.knots.append(Knot(self.count))
                self.knots[self.i].append(Vec2d(event.pos),
                                          Vec2d(random.random() * 2,
                                                random.random() * 2))

    def make_new_knot(self):

        """Функция добавления новой кривой"""

        self.i = -1
        self.knots.append(Knot(self.count))

    def change_knot(self, x=0):

        """Функция контроля индекса для списка кривых"""

        if x == 0:
            self.i -= 1
            if abs(self.i) > len(self.knots):
                self.i = -1
        elif x == 1:
            self.i += 1
            if abs(self.i) > len(self.knots)-1:
                self.i = -1

    def draw_help(self):

        """функция отрисовки экрана справки программы"""

        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["N", "New Knot"])
        data.append(["D", "Del last point"])
        data.append(["J", "Del last knot"])
        data.append(["L", "Change Knot to newer"])
        data.append(["K", "Change Knot to older"])
        data.append(["F", "Make Knot quiklier"])
        data.append(["S", "Make Knot slower"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.knots[self.i].count), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def start(self):
        while self.working:
            self.working_f()
            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            for i in self.knots:
                i.draw_points(self.gameDisplay)
                i.draw_line(self.gameDisplay, 3, self.color)
            if not self.pause:
                for i in self.knots:
                    i.set_points()
            if self.show_help:
                self.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


if __name__ == "__main__":
    g = Game()
    g.start()
