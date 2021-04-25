from random import randint


# class BoardOutException(Exception):
#     def __init__(self, message):
#         self.message = message
#
#     def __str__(self):
#         return f'BoardOutException, {self.message}'


class Dot:
    near_dots = []

    def __init__(self, x, y, state=' '):
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

    def get_near_dots(self):
        self.near_dots = [
            Dot(self.x + 1, self.y),
            Dot(self.x - 1, self.y),
            Dot(self.x + 1, self.y - 1),
            Dot(self.x - 1, self.y - 1),
            Dot(self.x + 1, self.y + 1),
            Dot(self.x - 1, self.y + 1),
            Dot(self.x, self.y + 1),
            Dot(self.x, self.y - 1)
        ]


class Ship:
    near_dots = []

    def __init__(self, dots, hp):
        self.dots = dots
        self.hp = hp
        self.direction = randint(1, 2)

    def get_near_dots(self):
        """ Возвращает список точек вокруг корабля """
        for ship_dot in self.dots:
            ship_dot.get_near_dots()
            for near_dot in ship_dot.near_dots:
                if near_dot not in self.near_dots:
                    self.near_dots.append(near_dot)


class Board:
    def __init__(self, dots, ships=None, hid=False, living_ships=7):
        self.dots = dots
        self.ships = [] if ships is None else ships
        self.hid = hid
        self.living_ships = living_ships

    def add_ship(self, ship):
        """
        Добавляет объект класса Ship в список Board.ships
        Отображает добавленный корабль на доске
        """
        self.ships.append(ship)
        # Сравниваются список точек корабля и список списков точек доски. Возможно, можно оптимизировать
        for ship_dot in ship.dots:
            for line in self.dots:
                for dot in line:
                    if dot == ship_dot:
                        dot.state = '\N{Black Circle}'

    def shot(self, dot):
        """ Меняет состояние точки в случае попадания """
        message = ''

        if dot.state == 'П':
            message = 'В эту точку уже стреляли'
        else:
            for ship in self.ships:

                if dot in ship.dots:
                    dot.state = '\N{Circle with Horizontal Bar}'
                    message = 'Попадание'
                    break
                else:
                    dot.state = 'П'
                    message = 'Промах'
        print(message)

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

        print('-' * 25)


class Game:
    # def __init__(self, board):
    #     self.board = board

    def generate_random_board(self):
        random_board = Board([[Dot(x + 1, y + 1) for x in range(6)] for y in range(6)])

        for i in range(4):
            ship1 = Ship([Dot(randint(1, 6), randint(1, 6))], 1)
            random_board.add_ship(ship1)

        ship2_1 = Ship([Dot(x + 1, 1) for x in range(2)], 2)
        ship2_2 = Ship([Dot(x + 1, 1) for x in range(2)], 2)
        #
        # ship3 = Ship([Dot(5, y + 2) for y in range(3)], 3)
        random_board.print_board()
        #
        random_board.add_ship(ship2_1)
        random_board.add_ship(ship2_2)
        # random_board.add_ship(ship3)
        # random_board.print_board()


game = Game()
game.generate_random_board()

# # Тест - создание списка ближайших точек для точки
# dot1 = Dot(0, 0)
# dot1.get_near_dots()
# print(dot1.near_dots)

# # Тест - создание доски, 3 разных кораблей и вывод пустой доски
# board1 = Board([[Dot(x + 1, y + 1) for x in range(6)] for y in range(6)])
# ship1 = Ship([Dot(3, 3)], 1)
# ship2 = Ship([Dot(x + 1, 1) for x in range(2)], 2)
# ship3 = Ship([Dot(5, y + 2) for y in range(3)], 3)
# board1.print_board()

# # Тест - добавление кораблей на доску и вывод
# board1.add_ship(ship1)
# board1.add_ship(ship2)
# board1.add_ship(ship3)
# board1.print_board()
#
# # Тест - метод shot
# board1.shot(board1.dots[0][0])
# board1.print_board()
# board1.shot(board1.dots[4][4])
# board1.print_board()
# board1.shot(board1.dots[4][4])
# board1.print_board()

# # Тест - создание списка ближайших точек для корабля
# ship3.get_near_dots()
# print(len(ship3.near_dots))