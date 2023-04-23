from abc import ABC, abstractmethod


class Figure(ABC):
    '''
    Абстрактный класс для всевозможных фигур
    '''
    color: str

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


class UPrincessFigure(Figure):
    '''
    Класс фигуры выставленной на поле игроком
    '''
    color = 'red'

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
        doska[i][j] = UPrincessFigure()
        return doska

    def __repr__(self):
        return '#'


class PPrincessFigure(Figure):
    '''
    Класс фигуры выставленной на поле в ход выполнения программы
    '''
    color = 'green'

    def figure_attack(self, board: list[list], i: int, j: int, N: int):
        doska = [board[i].copy() for i in range(N)]
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
        doska[i][j] = PPrincessFigure()
        return doska

    def __repr__(self):
        return '#'


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        f = tuple(f)
        NLK = f[0].split()
        coords = f[1:]

    N, L, K = tuple(map(int, NLK))
    board = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(K):
        i, j = tuple(map(int, coords[i].split()))
        board = UPrincessFigure().figure_attack(board, i, j, N)
        print(board[i][j].color)

    for stroka in board:
        stroka = ' '.join([str(i) for i in stroka])
        print(stroka)
