class CoordinatesError(Exception):
    '''Класс ошибки вызываемой неправильной записью координат фигуры'''

class EmptyNLK(Exception):
    '''Класс ошибки вызываемой при отсутсвии одного из параметров N, L, K в поле ввода'''

class InputError(Exception):
    '''Класс ошибки вызываемой в случае неккоректных вводных данных из фалйа "input.txt"

    Является критической и полностью завершает работу программы'''

class PlayerFiguresCoordinate(Exception):
    '''Класс ошибки вызываемой в случае некорректного ввода координат для изначальных фигур

    Является критической и полностью завершает работу программы'''