from abc import ABC, abstractmethod


class Figure(ABC):
    '''
    Абстрактный класс для всевозможных фигур
    '''

    @abstractmethod
    def figure_attack(self, doska: list[list], i: int, j: int, N: int) -> list[list]:
        '''
        Функция отвечающая за запись фигуры и ее клеток боя на заданную доску

        Параметры:
            doska: list[list]
                Заданная доска для подстановки фигуры
            i: int
                Индекс строки для подстановки фигуры
            j: int
                Индекс столбца для подстановки фигуры
            N: int
                Размерность заданной доски
        '''
        pass

    def __repr__(self):
        return '#'


class PrincessFigure(Figure):
    '''
    Класс фигуры выставленной на поле игроком
    '''

    def __init__(self, color='green'):
        self.color = color

    def figure_attack(self, doska, i, j, N):
        for a in range(1, 4):

            #  просчитывание клеток под боем для нижней части ходов фигуры
            if 0 <= i + a < N:
                c = j - a
                for b in range(3):
                    if 0 <= c < N:
                        doska[i + a][c] = '*'
                    c += a

            # просчитывание клеток под боем для верхнй части ходов фигуры
            if 0 <= i - a < N:
                c = j - a
                for b in range(3):
                    if 0 <= c < N:
                        doska[i - a][c] = '*'
                    c += a

            # просчитывание клеток под боем по горизонтали
            if 0 <= j - a < N:
                doska[i][j - a] = '*'

            if 0 <= j + a < N:
                doska[i][j + a] = '*'

        doska[i][j] = PrincessFigure(self.color)
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
