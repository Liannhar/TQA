import numpy as np


class Paddle:
    def __init__(self, boat, base_direction_move):
        print("Создаем весло")
        self.__max_durability = 5
        self.__base_direction_move = base_direction_move
        self.__current_durability = self.__max_durability
        self.__boat = boat

    @property
    def max_durability(self):
        return self.__max_durability

    @max_durability.setter
    def max_durability(self, durability):
        if 0 < durability:
            self.__max_durability = durability
        else:
            print("Недопустимое значение прочности")

    @property
    def current_durability(self):
        return self.__current_durability

    def twist(self, direction, angle):
        if self.is_break():
            return False
        self.__boat.change_angle(self.__base_direction_move * direction, angle)
        print("Крутим весло")
        return True

    def damage(self, damage_amount):
        if self.is_break():
            return False
        if damage_amount < 0:
            print(f"Неправильное значение урона")
            return False
        self.__current_durability -= np.clip(damage_amount, 0, self.__max_durability)
        return True

    def is_break(self):
        if self.__current_durability == 0:
            print(f"Весло уже сломано")
            return True
        return False
