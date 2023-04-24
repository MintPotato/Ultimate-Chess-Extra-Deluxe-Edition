from typing import Any
import Figures as fig
import time, Game
from MyErrors import InputError, PlayerFiguresCoordinate


class Board:
    def __init__(self, only_first_solution=False):
        '''
        Инициализация доски, в виде матрицы, и внесение в нее заданных фигур

        Параметры:
            only_first_solution: bool
                Параметр отражающий необходимость поиска одного или всех решений
        '''
        # Попытка прочитать файл и проверить первичную правильность записанных данных
        with open('input.txt', 'r') as f:
            try:
                f = tuple(f)
                NLK = f[0].split()
                coords_to_place = f[1:]

                if len(NLK) != 3:
                    Game.Game().error_occured(InputError, 'Некорректно введены значения N, L, K')
                    exit()

                if int(NLK[-1]) != len(coords_to_place):
                    Game.Game().error_occured(InputError, 'Недостаточно заданных координат для чтения')
                    exit()

            except Exception:
                Game.Game().error_occured(InputError,
                                          'Ошибка чтения данных из файла "input.txt" так как данные введены некорректно')
                exit()

        # Запись размерность, количества фигур для подстановки и количества координат фигур для считывания
        self.N, self.L, self.K = tuple(map(int, NLK))

        # Создание матрицы доски
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]

        self.founded_solves = 0
        coords_placed = []  # Список координат уже выставленных фигур в виде строк
        self.first_founded = False

        # Задаем желаемую фигуру
        self.figure = fig.PrincessFigure

        # Расставление первичных фигур на доску
        for pair in range(self.K):
            i, j = tuple(map(int, coords_to_place[pair].split()))

            # Если заданные пользователем фигуры не удовлетворяют условию
            if self.board[i][j] != 0:
                Game.Game().error_occured(PlayerFiguresCoordinate,
                                          'Координаты фигур для стартовой расстановки заданы неверно (совпадают/ находятся под боем)')
                exit()

            # Обновление доски и запись координат выставленной фигуры
            self.board = self.figure('red').figure_attack(self.board, i, j, self.N)
            coords_placed += [f'({i}, {j})']

        # Если количество свободных клеток не меньше необходимого количества и нужно найти все решения
        if self.if_free_cells() and not only_first_solution:
            # Открывает файл для записи найденых решений
            f = open('output.txt', 'w')

            # Запускается функция осуществляющая поиск реений
            self.solves(self.board, 0, f, 0, 0, coords_placed)

            # Если решений не найдно, записать вывести в консоль и записать в файл "No solution"
            if self.founded_solves == 0:
                print('No solution')
                f.write('No solution')

            else:  # Иначе вывести количество найденных решений
                print(self.founded_solves)

    def solves(self, board: list[list], placed: int, file, i1: int, j1: int, coords: list[str]):
        '''
        Рекуррентная функция целью которой является поиск возможных вариантов расстановки заданной фигуры

        Параметры:
            board: list[list]
                Доска с уже расставленными фигурами и клетками под атакой
            placed: int
                Количество уже поставленных фигур в ходе выполнения функции
            file:
                Ссылка на  файл 'output.txt', в который осуществляется ввод найденных решений
            i1: int
                Индекс строки с которой продолжается поиск свободного места для подстановки
            j1: int
                Индекс столбца с которго продолжается поиск свободного места для подстановки
            coords: list[str]
                Список координат выставленных фигур
        '''

        # Если количество выставленных фигур меньше необходимого
        if placed < self.L:

            # Продолжается проход по матрице доски с позиции посленей выставленной фигуры в ходе решения, по умолчанию (0, 0)
            for i in range(i1, self.N):
                for j in range(j1, self.N):

                    if board[i][j] == 0:
                        # Обновленная матрица доски с новой выставленной фигурой и ее боем
                        updated_board = self.figure('green').figure_attack(board, i, j, self.N)

                        self.solves(updated_board, placed + 1, file, i, j, coords + [f'({i}, {j})'])

                # j1 обнуляется тк на строках матрицы, отличных от исходной, проход осуществляется с 0-го столбца
                j1 = 0

        # Если выставленно необходимое количество фигур увеличивается счетчик найденных решений и осуществляется запись полученых координат в 'output.txt'
        elif placed == self.L:
            self.founded_solves += 1
            file.write(' '.join(coords) + '\n')

            # Если доска с решением, до этого, не была выведена в консоль
            if not self.first_founded:
                for stroka in board:
                    stroka = ' '.join([str(i) for i in stroka])
                    print(stroka)
                self.first_founded = board

    def if_free_cells(self) -> bool:
        '''
        Функция проверяющая наличие свободных мест, и их достаточность, для подстановки фигур
        '''

        free_cells = 0

        # Подсчитывается количество свободных мест для подстановки
        for el in self.board:
            free_cells += el.count(0)

        # Если количество клеток для подстановки меньше необходимого количества фигур для подстановки
        if free_cells < self.L:
            return False
        else:
            return True

    def only_fist_solve(self) -> Any:
        '''Функция выполняющая поиск первого решения путем прохождения по матрице и заполнением пустых клеток

        Если решение было найдено, то возвращает полученную матрицу данных.
        Иначе возвращает False
        '''

        placed = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] == 0:
                    self.board = self.figure('green').figure_attack(self.board, i, j, self.N)
                    placed += 1

                # Если решение для заданных условий было найдено, возвращается доска с найденым решением
                if placed == self.L:
                    return self.board

        # Если решенияне было найдено вощвращает False
        return False


if __name__ == '__main__':
    start_time = time.time()
    board = Board()

    print(time.time() - start_time)
