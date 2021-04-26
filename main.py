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

    def __init__(self, forward_dot, length, hp, dots=None):
        self.forward_dot = forward_dot
        self.length = length
        self.hp = hp
        self.direction = randint(1, 4)
        self.dots = [forward_dot] if dots is None else dots

    def __str__(self):
        return f"Ship with forward dot: {self.forward_dot}, length: {self.length}"

    def build(self):
        """
         Корабль создается от одной точки - forward_dot
         Этот метод достраивает корабль в зависимости от direction и length
         """
        for i in range(self.length - 1):
            if self.direction == 1:
                self.dots.append(Dot(self.forward_dot.x + (i + 1), self.forward_dot.y))
            elif self.direction == 2:
                self.dots.append(Dot(self.forward_dot.x - (i + 1), self.forward_dot.y))
            elif self.direction == 3:
                self.dots.append(Dot(self.forward_dot.x, self.forward_dot.y - (i + 1)))
            else:
                self.dots.append(Dot(self.forward_dot.x, self.forward_dot.y + (i + 1)))
        # print(f'direction: {self.direction}')
        # for dot in self.dots:
        #     print(dot)

    def get_dots(self):
        return self.dots

    def get_near_dots(self):
        """ Возвращает список точек вокруг корабля
            Также сюда попадают точки самих кораблей, если состоят из 2 или 3 клеток
            Если корабль одноклеточный, то его точка не попадает в этот список
            """

        for ship_dot in self.dots:
            ship_dot.get_near_dots()
            for near_dot in ship_dot.near_dots:
                if near_dot not in self.near_dots:
                    self.near_dots.append(near_dot)
        return self.near_dots


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

    def delete_ship(self, ship):
        """
        Удаляет объект класса Ship из списка Board.ships
        Удаляет отображение корабля на доске
        """
        self.ships.remove(ship)
        # Сравниваются список точек корабля и список списков точек доски. Возможно, можно оптимизировать
        for ship_dot in ship.dots:
            for line in self.dots:
                for dot in line:
                    if dot == ship_dot:
                        dot.state = ' '

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

    def in_board(self, dot):
        """ Определяет, находится ли точка в диапазоне доски"""
        for line in self.dots:
            if dot in line:
                return True
        return False

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
        forbidden_dots = []

        count = 0  # Считает итерации в цикле создания одноклеточных кораблей
        flag = False  # Говорит о том, что счетчик перешел за 100

        while True:
            # Создание корабля из 3 клеток
            while True:
                ship3 = Ship(Dot(randint(1, 6), randint(1, 6)), 3, 3)
                ship3.near_dots = []
                ship3.build()
                ship3.get_near_dots()

                print('ship3 построен с точками:')
                for dot in ship3.dots:
                    print(dot)

                add = True
                delete = False
                for dot in ship3.dots:
                    if not random_board.in_board(dot):
                        add = False
                        delete = True
                if delete:
                    del ship3
                    print('ship3 удален')
                if add:
                    random_board.add_ship(ship3)
                    forbidden_dots.extend(ship3.near_dots)
                    print(f'forbidden: {len(forbidden_dots)}')
                    break

            # Создание кораблей из 2 клеток
            for i in range(2):
                while True:
                    # count += 1
                    # if count > 100:
                    #     flag = True
                    #     break
                    ship2 = Ship(Dot(randint(1, 6), randint(1, 6)), 2, 2)
                    ship2.near_dots = []
                    ship2.build()
                    ship2.get_near_dots()

                    print(f'ship2 построен с точками:')
                    for dot in ship2.dots:
                        print(dot)

                    add = True
                    delete = False
                    for dot in ship2.dots:
                        if not random_board.in_board(dot) or dot in forbidden_dots:
                            add = False
                            delete = True
                    if delete:
                        del ship2
                        print('ship2 удален')
                    if add:
                        random_board.add_ship(ship2)
                        forbidden_dots.extend(ship2.near_dots)
                        print(f'forbidden: {len(forbidden_dots)}')
                        break

            # Создание кораблей из 1 клетки
            for i in range(4):
                while True:
                    count += 1
                    if count > 1000:
                        flag = True
                        break
                    ship1 = Ship(Dot(randint(1, 6), randint(1, 6)), 1, 1)
                    ship1.near_dots = []
                    ship1.build()
                    ship1.get_near_dots()

                    print('ship1 построен с точкой:', ship1.forward_dot)
                    add = True
                    delete = False
                    if ship1.forward_dot in forbidden_dots:
                        add = False
                        delete = True
                    if delete:
                        del ship1
                        print('ship1 удален')
                    if add:
                        random_board.add_ship(ship1)
                        forbidden_dots.extend(ship1.near_dots)
                        # Если корабль одноклеточный, то он не попадает в список near_dots
                        forbidden_dots.append(ship1.forward_dot)
                        print(f'forbidden: {len(forbidden_dots)}')
                        break

            random_board.print_board()

            if flag:
                forbidden_dots = []
                count = 0
                flag = False
                # Не понимаю, почему список не очищается сразу, а удаляет только корабли одного вида
                # Поэтому пришлось добавить while
                while random_board.ships:
                    for ship in random_board.ships:
                        random_board.delete_ship(ship)
                random_board.print_board()
                continue
            else:
                break


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
