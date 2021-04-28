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

    def get_dots(self):
        return self.dots

    def get_near_dots(self):
        """
        Возвращает список точек вокруг корабля
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
    def __init__(self, dots, ships=None, hid=False):
        self.dots = dots
        self.ships = [] if ships is None else ships
        self.hid = hid

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
        """ В случае попадания меняет состояние точки, возвращает True (чтобы стрелять повторно),
            удаляет корабль, если у него не осталось hp"""
        message = ''
        again = False

        if dot.state == 'П' or dot.state == '\N{Circle with Horizontal Bar}':
            message = 'В эту точку уже стреляли'
            again = True
        else:
            for ship in self.ships:
                if dot in ship.dots:
                    dot.state = '\N{Circle with Horizontal Bar}'
                    ship.hp -= 1
                    if ship.hp == 0:
                        self.ships.remove(ship)
                    message = 'Попадание'
                    again = True
                    break
                else:
                    dot.state = 'П'
                    message = 'Промах'
        print(message)
        return again

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
                hid = self.hid and element.state == '\N{Black Circle}'
                if k != len(line) - 1:
                    print(' ' if hid else element.state, end=' | ')
                else:
                    print(' ' if hid else element.state, end='')
            print()

        print('-' * 25)


class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        """ Возвращает точку, по которой будет производиться выстрел """
        pass

    def move(self):
        print(f'Ходит {self}')
        enemy_dot = self.ask()
        # Связывание выбранной точки с конкретной точкой на доске
        for line in self.enemy_board.dots:
            for dot in line:
                if enemy_dot == dot:
                    print(f'{self} стреляет по клетке {enemy_dot}')
                    shot = self.enemy_board.shot(dot)
        # shot = self.enemy_board.shot(enemy_dot)
        if shot and self.enemy_board.ships:  # Если попал и у соперника остались корабли, то нужно повторить ход
            self.enemy_board.print_board()
            Player.move(self)


class AI(Player):
    def __str__(self):
        return 'AI'

    def ask(self):
        return Dot(randint(1, 6), randint(1, 6))


class User(Player):
    def __str__(self):
        return 'User'

    def ask(self):
        return Dot(int(input("Введите 'x' точки: ")), int(input("Введите 'y' точки: ")))


class Game:
    def __init__(self):
        self.user_board = Game.generate_random_board()
        self.ai_board = Game.generate_random_board()
        self.ai_board.hid = True
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    @staticmethod
    def generate_random_board():
        random_board = Board([[Dot(x + 1, y + 1) for x in range(6)] for y in range(6)])
        forbidden_dots = []  # Точки, на которых нельзя размещать новый корабль
        count = 0  # Считает итерации в цикле создания одноклеточных кораблей
        flag = False  # Говорит о том, что счетчик перешел за 1000 (значит, нужно генерировать новую доску)

        while True:
            # Создание корабля из 3 клеток
            while True:
                ship3 = Ship(Dot(randint(1, 6), randint(1, 6)), 3, 3)
                ship3.near_dots = []
                ship3.build()
                ship3.get_near_dots()

                add = True
                delete = False
                for dot in ship3.dots:
                    if not random_board.in_board(dot):
                        add = False
                        delete = True
                if delete:
                    del ship3
                if add:
                    random_board.add_ship(ship3)
                    forbidden_dots.extend(ship3.near_dots)
                    break

            # Создание кораблей из 2 клеток
            for i in range(2):
                while True:
                    ship2 = Ship(Dot(randint(1, 6), randint(1, 6)), 2, 2)
                    ship2.near_dots = []
                    ship2.build()
                    ship2.get_near_dots()

                    add = True
                    delete = False
                    for dot in ship2.dots:
                        if not random_board.in_board(dot) or dot in forbidden_dots:
                            add = False
                            delete = True
                    if delete:
                        del ship2
                    if add:
                        random_board.add_ship(ship2)
                        forbidden_dots.extend(ship2.near_dots)
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

                    add = True
                    delete = False
                    if ship1.forward_dot in forbidden_dots:
                        add = False
                        delete = True
                    if delete:
                        del ship1
                    if add:
                        random_board.add_ship(ship1)
                        forbidden_dots.extend(ship1.near_dots)
                        # Если корабль одноклеточный, то он не попадает в список near_dots
                        forbidden_dots.append(ship1.forward_dot)
                        break

            if flag:
                forbidden_dots = []
                count = 0
                flag = False
                # Не понимаю, почему список не очищается сразу, а удаляет только корабли одного вида
                # Поэтому пришлось добавить while
                while random_board.ships:
                    for ship in random_board.ships:
                        random_board.delete_ship(ship)
                continue
            else:
                break

        return random_board

    def game_loop(self):
        while True:
            self.user.move()
            self.ai_board.print_board()
            if not self.ai_board.ships:
                print('Поздравляем, вы победили!')
                break

            self.ai.move()
            self.user_board.print_board()
            if not self.user_board.ships:
                print('Победил компьютер')
                break

    def greet(self):
        print("Приветствую вас в игре 'Морской бой'! Игра происходит на поле 6*6 клеток.\n" 
              "В вашем распоряжении 1 корабль на 3 клетки, 2 корабля на 2 клетки и 4 корабля на одну клетку.\n"
              "Корабли отображаются так: '\N{Black Circle}'\n"
              "Подбитые корабли так: '\N{Circle with Horizontal Bar}'\n"
              "В случае промаха на поле появится буква 'П'\n"
              "Удачной игры! Ваша доска:")
        self.user_board.print_board()

    def start(self):
        self.greet()
        self.game_loop()


game = Game()
game.start()

