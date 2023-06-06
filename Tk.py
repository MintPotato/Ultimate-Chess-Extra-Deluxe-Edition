import tkinter as tk
import tkinter.ttk as ttk
from MyErrors import CoordinatesError, EmptyNLK
import Game


def write_coords(coords: str):
    '''
    Функция записывающая полученную строку в файл "input.txt"

    Параметры:
        coords: str
             Строка состоящая из значений N, L, K (+ координат фигур)
    '''

    with open('input.txt', 'w') as f:
        f.write(coords)


class CoordsWindow(tk.Toplevel):
    '''
    Класс окна с вводом координат
    '''

    def __init__(self, nlk: str, n: str, k: str):
        '''
        Инициализация окна и его объектов

        Параметры:
            nlk: str
                Строка с значениями N, L, K для записи в файл "input.txt"
            n: str
                Значение N (размерность доски)
            k: str
                Значение K (количество фигур для подстановки игроком)
        '''

        super().__init__()

        # Объявление необходимых переменных
        self.nlk_and_coords = nlk  # Строка содержащая первую строку файла "input.txt"
        self.razmernost = int(n)  # Размерность доски
        self.k = int(k)  # Количество строк ввода координат
        self.coords_entries = []  # Список для хранения полей ввода координат

        # Создание команды валидации ввода значений координат
        self.vcmd_coords = (self.register(self.is_valid), '%P')

        # Инициализация строк ввода координат
        for i in range(self.k):
            self.label = ttk.Label(self, text='Введите координаты "x y":').grid(row=i, column=0)
            self.entry = ttk.Entry(self, validate='key', validatecommand=self.vcmd_coords)
            self.coords_entries += [self.entry]
            self.entry.grid(row=i, column=1)

        # Создание кнопки подтверждения ввода координат
        self.start_btn = ttk.Button(self, text='Запуск', command=self.get_coords).grid(row=self.k)

        self.resizable(False, False)

    def get_coords(self):
        '''
        Функция записывающая координаты фигур, расставленных пользователем
        '''

        # Проход по полям ввода координат
        for vvod in self.coords_entries:

            try:

                coords = vvod.get().split()

                if len(coords) == 2:  # Если записано нужное количество координат, добавляем их к строке записи
                    self.nlk_and_coords = self.nlk_and_coords + vvod.get().strip() + '\n'
                else:
                    self.destroy()
                    Game.Game().error_occured(CoordinatesError,
                                              "Как минимум одна из пар координат записана не по условию"
                                              )
            except:
                # Открытие нового окна записи координат для повторной попытки
                CoordsWindow(self.nlk_and_coords, str(self.razmernost), str(self.k))

                # Закрытие уже существующего окна, и вызов ошибки
                self.destroy()
                Game.Game().error_occured(CoordinatesError, 'Как минимум одна из пар координат записана не по условию')

        # Вызов функции записывающей координаты в файл и закрытие окна
        write_coords(self.nlk_and_coords)
        self.quit()

    def is_valid(self, string: str) -> bool:
        '''
        Функция для валидации ввода координат фигур

        Параметры:
            string: str
                Строка ввда координат фигур
        '''
        # Нужна для возможности удалять первый написаный элемент
        if string == '':
            return True

        # Переменная для хранения записаных координат
        coords = string.split()

        if len(coords) > 2:  # если пытаются ввести третью координату
            return False
        try:
            coords = map(int, coords)

            # если введенная координата не превышает размерность поля
            # (ввод координат ведется с 0 до self.razmernost - 1)
            if max(coords) < self.razmernost:
                return True
            else:
                return False

        except:
            return False


class NLKWindow(tk.Tk):
    """
    Класс с вводом значений:
        n - размерность доски

        l - количество фигур дл подстановки

        k - количество уже стоящих фигур (не под боем)
    """

    def __init__(self):
        '''
        Инициализация параметров окна и его объектов
        '''
        super().__init__()
        self.geometry('150x200')
        self.resizable(False, False)

        # Создание команд валидации для записи значени N, L, K
        vcmd_n = (self.register(self.is_valid_n), '%P')
        vcmd_lk = (self.register(self.is_valid), '%P')

        # Инициализация фрейма для записи значения N
        self.frame_n = ttk.Frame(self, padding=[8, 5])
        self.frame_n.pack()
        self.label_n = ttk.Label(self.frame_n, text='Введите N').pack()
        self.entry_n = ttk.Entry(self.frame_n, validate='key', validatecommand=vcmd_n)
        self.entry_n.pack()

        # Инициализация фрейма для записи значения L
        self.frame_l = ttk.Frame(self, padding=[8, 5])
        self.frame_l.pack()
        self.label_l = ttk.Label(self.frame_l, text='Введите L').pack()
        self.entry_l = ttk.Entry(self.frame_l, validate='key', validatecommand=vcmd_lk)
        self.entry_l.pack()

        # Инициализация фрейма для записи значения K
        self.frame_k = ttk.Frame(self, padding=[8, 5])
        self.frame_k.pack()
        self.label_k = ttk.Label(self.frame_k, text='Введите K').pack()
        self.entry_k = ttk.Entry(self.frame_k, validate='key', validatecommand=vcmd_lk)
        self.entry_k.pack()

        # Инициализация кнопки перехода к окну записи координат
        self.frame_btn = ttk.Frame(self, padding=[8, 6])
        self.frame_btn.pack()
        self.btn = ttk.Button(self.frame_btn, text='Далее', command=self.open_coords_window).pack()

    def is_valid_n(self, string: str) -> bool:
        '''
        Функция валидации поля ввода значения N

        Параметры:
            string: str
                Строка из поля ввода значения N
        '''

        # Нужна для возможности удалять первый написаный элемент
        if string == '':
            return True

        try:
            # Проверка на то что введено число
            string = int(string)
            if string > 20:  # Если введенная размерность не превышает максимально допустимую (0-19)
                return False
            else:
                return True

        except:
            return False

    def is_valid(self, string: str) -> bool:
        '''
        Функция валидации поля ввода значения L и K

        Параметры:
            string: str
                Строка из поля ввода значения N или K
        '''

        # Нужна для возможности удалять первый написаный элемент
        if string == '':
            return True

        try:

            # Проверка на то что введено число
            string = int(string)
            return True
        except:
            return False

    def open_coords_window(self):
        '''
        Функция кнопки вызывающая окно ввода координат если введенное K отлично от 0,
        или вызывающая функцию записи координат в файл
        '''
        # Проверка о том, что во всех полях присутсвуют значения
        try:

            # Значения полей (обрезать пробелы по бокам не обязательно, однако сделано для красоты записи в файл)
            n, l, k = self.entry_n.get().strip(), self.entry_l.get().strip(), self.entry_k.get().strip()

            # Первая строка файла 'input.txt'
            nlk = '{} {} {}\n'.format(n, l, k)

            if k == '0':  # Если вводить координаты не нужно, записываем данные в 'input.txt' и закрываем окно
                write_coords(nlk)
                self.quit()

            else:  # Иначе открываем окно для записи координат
                CoordsWindow(nlk, n, k)
        except:
            # Закрываем окно и открываем новое для повторной попытки записи значений
            self.destroy()
            NLKWindow()
            Game.Game().error_occured(EmptyNLK, 'Как минимум одно из полей для ввода значений является пустым')
