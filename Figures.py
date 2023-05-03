from abc import ABC, abstractmethod


class Figure(ABC):
    '''
    Абстрактный класс для всевозможных фигур
    '''

    @abstractmethod
    def __init__(self, color):
        '''
        Параметры:
            color: str
                Цвет фигуры: red - фигура выставленная на исходную доску; green - фигура выставленная в ходе поиска решений
        '''
        self.color: str

    @abstractmethod
    def figure_attack(self, doska: list[list], y: int, x: int, N: int) -> list[list]:
        '''
        Функция отвечающая за запись фигуры и ее клеток боя на заданную доску

        Параметры:
            doska: list[list]
                Заданная доска для подстановки фигуры
            y, x: int
                Координаты для подстановки фигуры
            N: int
                Размерность заданной доски
        '''
        pass

    # При обращении возвращает условное обозначение выставленной фигуры для вывода доски в консоль
    def __repr__(self):
        return '#'


class PrincessFigure(Figure):
    '''
    Класс фигуры "Принцесса"
    '''

    def __init__(self, color: str):
        self.color = color

    def figure_attack(self, doska, y, x, N):

        # Создание копии доски, чтобы данные в исходной доске не переписывались
        doska = [doska[i].copy() for i in range(N)]

        # Проход по возможным координатам клеток боя
        for el in (y - 3, x - 3), (y - 3, x), (y - 3, x + 3), (y - 2, x - 2), (y - 2, x), (y - 2, x + 2), \
                (y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 3), (y, x - 2), (y, x - 1), (y, x + 1), (
        y, x + 2), (y, x + 3), \
                (y + 1, x - 1), (y + 1, x), (y + 1, x + 1), (y + 2, x - 2), (y + 2, x), (y + 2, x + 2), (
        y + 3, x - 3), (y + 3, x), (y + 3, x + 3):
            if 0 <= el[0] < N and 0 <= el[1] < N:
                doska[el[0]][el[1]] = '*'

        # Запись самой фигуры на поле
        doska[y][x] = PrincessFigure(self.color)

        return doska


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        f = tuple(f)
        NLK = f[0].split()
        coords = f[1:]

    N, L, K = tuple(map(int, NLK))
    board = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(K):
        i, j = tuple(map(int, coords[i].split()))
        board = PrincessFigure('red').figure_attack(board, i, j, N)
        print(board[i][j].color)

    for stroka in board:
        stroka = ' '.join([str(i) for i in stroka])
        print(stroka)
