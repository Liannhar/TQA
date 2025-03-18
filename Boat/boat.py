from .paddle import Paddle as paddle
import numpy as np


class Boat:
    def __init__(self):
        print("Создаем лодку")
        self.left_paddle = paddle(self, 1)
        self.right_paddle = paddle(self, -1)
        self.__angle = 0  # угол от 0 до 360, лодка направлена по y при 0 градусах
        self.__max_durability = 10
        self.__durability = self.__max_durability
        self.__acceleration = 10
        self.__max_weight = 100
        self.__current_weight = 0
        self.__exceed_weight_modifier = 1
        self.__x = 0
        self.__y = 0

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def max_weight(self):
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, weight):
        if 0 < weight:
            self.__max_weight = weight
        else:
            print("Недопустимое значение максимального веса")
    @property
    def exceed_weight_modifier(self):
        return self.__exceed_weight_modifier

    @property
    def acceleration(self):
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration):
        if 0 < acceleration:
            self.__acceleration = acceleration
        else:
            print("Недопустимое значение ускорения")

    @property
    def angle(self):
        return self.__angle

    @property
    def current_weight(self):
        return self.__current_weight

    @angle.setter
    def angle(self, angle):
        if 0 <= angle <= 360:
            self.__angle = angle
        else:
            print("Недопустимое значение угла")

    @property
    def max_durability(self):
        return self.__max_durability

    @max_durability.setter
    def max_durability(self, durability):
        if 0 < durability:
            self.__max_durability = durability
        else:
            print("Недопустимое значение прочности")

    def left_paddle_move(self, direction,angle):
        if self.is_break():
            return False
        self.left_paddle.twist(direction,angle)

    def right_paddle_move(self, direction,angle):
        if self.is_break():
            return False
        self.right_paddle.twist(direction,angle)

    def move(self, t, direction):
        direction_sign = np.sign(direction)
        angle = np.radians(self.__angle)

        self.__x = self.__x + direction_sign * 0.5 * (self.__acceleration * t ** 2) * np.sin(
            angle) * self.__exceed_weight_modifier
        self.__y = self.__y + direction_sign * 0.5 * (self.__acceleration * t ** 2) * np.cos(
            angle) * self.__exceed_weight_modifier
        print(self.__x, " ", self.__y)

    def both_paddle_move(self, t, direction):
        if self.is_break():
            return False
        if self.left_paddle.is_break() or self.right_paddle.is_break():
            print(f"Сломано одно из весел для движения вперед")
            return False
        self.move(t, direction)

    def change_angle(self, direction,angle):
        if self.is_break():
            return False
        if angle<0 and angle>360:
            print("Неправильнй угол")
            return False
        direction_sign = np.sign(direction)
        self.__angle += direction_sign * angle
        if self.__angle > 360:
            self.__angle -= 360
        if self.__angle < 0:
            self.__angle += 360
        print("Новый угол", self.__angle)

    def check_weight(self, weight):
        return 0 <= weight <= self.__max_weight

    def add_weight(self, weight):
        if self.is_break():
            return
        if weight <= 0:
            print(f"Неправильный вес")
            return
        self.__current_weight += weight
        self.__exceed_weight_modifier = np.clip(1.0 - (self.__current_weight - self.__max_weight) / self.__max_weight,
                                                0, 1)
        if not self.check_weight(self.__current_weight):
            print(f"Превышен вес на: {self.__current_weight - self.__max_weight}")

    def subtract_weight(self, weight):
        if self.is_break():
            return False
        if weight <= 0:
            print(f"Неправильный вес")
            return False
        self.__current_weight = np.clip(self.__current_weight-weight,
                                                0, self.__current_weight)
        self.__exceed_weight_modifier = np.clip(1.0 - (self.__current_weight - self.__max_weight) / self.__max_weight,
                                                0, 1)
        if not self.check_weight(self.__current_weight):
            print(f"Вес меньше 0")

    def damage(self, damage_amount):
        if self.is_break():
            return False
        if damage_amount < 0:
            print(f"Неправильное значение урона")
            return False
        self.__durability -= np.clip(damage_amount, 0, self.__max_durability)

    def is_break(self):
        if self.__durability == 0:
            print(f"Лодка сломана")
            return True
        return False
