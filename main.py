class Dot:
    def __init__(self, x, y, state='O'):
        self.x = x
        self.y = y
        self.state = state

    def __eq__(self, other):
        if self.y == other.y and self.x == other.x:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.x}:{self.y}"


class Ship:
    dots = []

    def __init__(self, length, front_dot, back_dot, hp):
        self.length = length
        self.front_dot = front_dot
        self.back_dot = back_dot
        self.hp = hp

    def get_dots(self):
        for i in range(self.length):
            self.dots.append(i)
        return self.dots


class Board:
    def __init__(self, dots, ships=(), hid=False, living_ships=7):
        self.dots = dots
        self.ships = ships
        self.hid = hid
        self.living_ships = living_ships

    def out(self, dot):
        if dot in self.dots:
            return False
        return True

    def print_board(self):
        """ Выводит поле для игры на консоль """
        # Вывод первой строки (с цифрами)
        for i in range(7):
            print(f"{i} | ", end='') if i != 6 else print(f"{i}", end='')
        print()

        for i, line in enumerate(self.dots):
            # Вывод первого столбца (с цифрами)
            print(i + 1, end=' | ')
            # Вывод самого поля для игры
            for k, element in enumerate(line):
                print(element.state, end=' | ') if k != len(line) - 1 else print(element.state, end='')
            print()


# print('\N{Black Circle}') # корабль
# print('\N{Circle with Horizontal Bar}') # подбитый корабль

# dot1 = Dot(1, 1)
# ship1 = Ship(1, dot1, dot1, 1)
board1 = Board([[Dot(x + 1, y + 1) for x in range(6)] for y in range(6)])
board1.print_board()
