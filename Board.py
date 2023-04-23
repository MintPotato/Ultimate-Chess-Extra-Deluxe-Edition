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

        '''
        with open('input.txt', 'r') as f:
            try:
                    f = tuple(f)
                    NLK = f[0].split()
                    coords_to_place = f[1:]
            except Exception:
                Game.Game().error_occured(InputError, 'Ошибка чтения данных из файла "input.txt" так как данные введены некорректно')
                exit()

        self.N, self.L, self.K = tuple(map(int, NLK))
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.founded_solves = 0
        coords_placed = []
        self.first_founded = False

        # Задаем желаемые фигуры
        self.user_figure = fig.UPrincessFigure()
        self.programm_figure = fig.PPrincessFigure()

        for pair in range(self.K):
            i, j = tuple(map(int, coords_to_place[pair].split()))

            if self.board[i][j] != 0:
                Game.Game().error_occured(PlayerFiguresCoordinate, 'Координаты фигур для стартовой расстановки заданы неверно (совпадают/ находятся под боем)')
                exit()

            self.board = self.user_figure.figure_attack(self.board, i, j, self.N)
            coords_placed += [f'({i}, {j})']

        enogh_cells = self.if_free_cells()

        if enogh_cells and not only_first_solution:
            f = open('output.txt', 'w')
            self.solves(self.board, 0, f, 0, 0, coords_placed)
            if self.founded_solves == 0:
                print('No solution')
                f.write('No solution')
            else:
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
            coords: list[tuple]
                Список координат выставленных фигур
        '''

        if placed < self.L:
            for i in range(i1, self.N):
                for j in range(j1, self.N):
                    if board[i][j] == 0:
                        new_board = self.programm_figure.figure_attack(board, i, j, self.N)
                        self.solves(new_board, placed + 1, file, i, j, coords + [f'({i}, {j})'])
                j1 = 0

        elif placed == self.L:
            self.founded_solves += 1
            file.write(' '.join(coords) + '\n')

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
        for el in self.board:
            free_cells += el.count(0)

        if free_cells < self.L:
            return False
        else:
            return True

    def only_fist_solve(self) -> Any:
        '''Функция выполняющая поиск первого решения путем прохождения по матрице и заполнением пустых клеток

        Если решение было найдено, то возвращает полученную матрицу данных.
        Иначе возвращает False
        '''
        return_board = [self.board[i].copy() for i in range(self.N)]
        placed = 0
        for i in range(self.N):
            for j in range(self.N):
                if return_board[i][j] == 0:
                    return_board = self.programm_figure.figure_attack(return_board, i, j, self.N)
                    placed += 1

                if placed == self.L:
                    return return_board

        return False


if __name__ == '__main__':
    start_time = time.time()
    board = Board()

    print(board.founded_solves)
    print(time.time() - start_time)
