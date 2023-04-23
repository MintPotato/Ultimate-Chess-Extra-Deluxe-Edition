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
    Класс в котором реализуется создание окна с вводом координат
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
        self.nlk_and_coords = nlk
        self.razmernost = int(n)
        self.k = int(k)

        self.vcmd_coords = (self.register(self.is_valid), '%P')
        self.coords_entries = []

        for i in range(self.k):
            self.label = ttk.Label(self, text='Ввежите координаты "x y":').grid(row=i, column=0)
            self.entry = ttk.Entry(self, validate='key', validatecommand=self.vcmd_coords)
            self.coords_entries += [self.entry]
            self.entry.grid(row=i, column=1)

        self.start_btn = ttk.Button(self, text='Запуск', command=self.get_coords).grid(row=self.k)
        self.resizable(False, False)

    def is_valid(self, string: str) -> bool:
        '''
        Функция для валидации ввода координат фигур

        Параметры:
            string: str
                Строка ввда координат фигур
        '''
        if string == '':
            return True
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

    def get_coords(self):
        '''
        Функция записывающая координаты фигур, расставленных пользователем
        '''

        for vvod in self.coords_entries:
            try:
                coords = vvod.get().split()
                if len(coords) == 2:
                    self.nlk_and_coords = self.nlk_and_coords + vvod.get().strip() + '\n'
                else:
                    self.destroy()
                    Game.Game().error_occured(CoordinatesError,
                                              "Как минимум одна из пар координат записана не по условию"
                                              )
            except:
                CoordsWindow(self.nlk_and_coords, str(self.razmernost), str(self.k))
                self.destroy()
                Game.Game().error_occured(CoordinatesError, 'Как минимум одна из пар координат записана не по условию')

        write_coords(self.nlk_and_coords)
        self.quit()


class NLKWindow(tk.Tk):
    """
    Класс в котором реализуется создание окна с вводом значений:
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

        vcmd_n = (self.register(self.is_valid_n), '%P')
        vcmd_lk = (self.register(self.is_valid), '%P')

        self.frame_n = ttk.Frame(self, padding=[8, 5])
        self.frame_n.pack()
        self.label_n = ttk.Label(self.frame_n, text='Введите N').pack()
        self.entry_n = ttk.Entry(self.frame_n, validate='key', validatecommand=vcmd_n)
        self.entry_n.pack()

        self.frame_l = ttk.Frame(self, padding=[8, 5])
        self.frame_l.pack()
        self.label_l = ttk.Label(self.frame_l, text='Введите L').pack()
        self.entry_l = ttk.Entry(self.frame_l, validate='key', validatecommand=vcmd_lk)
        self.entry_l.pack()

        self.frame_k = ttk.Frame(self, padding=[8, 5])
        self.frame_k.pack()
        self.label_k = ttk.Label(self.frame_k, text='Введите K').pack()
        self.entry_k = ttk.Entry(self.frame_k, validate='key', validatecommand=vcmd_lk)
        self.entry_k.pack()

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
        if string == '':
            return True

        try:
            string = int(string)
            if string > 20:
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
        if string == '':
            return True
        try:
            string = int(string)
            return True
        except:
            return False

    def open_coords_window(self):
        '''
        Функция кнопки вызывающая окно ввода координат если введенное K отлично от 0,
        или вызывающая функцию записи координат в файл
        '''
        try:
            n, l, k = self.entry_n.get().strip(), self.entry_l.get().strip(), self.entry_k.get().strip()
            nlk = '{} {} {}\n'.format(n, l, k)
            if k == '0':
                write_coords(nlk)
                self.quit()
            else:
                CoordsWindow(nlk, n, k)
        except:
            self.destroy()
            NLKWindow()
            Game.Game().error_occured(EmptyNLK, 'Как минимум одно из полей для ввода значений является пустым')

# class WaitWindow(tk.Tk):
#     def __init__(self):
#         super().__init__()
#
#         self.geometry('200x100')
#
#         self.label_text = tk.StringVar()
#         self.label = ttk.Label(self, textvariable=self.label_text).grid(row=0)
#         self.label_text.set('Идет запись решений, ожидайте')
#
#
#     def done(self):
#         self.label = ttk.Label(self, textvariable=self.label_text).grid(row=0)
#         self.label_text.set('Запись окончена')
#         self.close_btn = ttk.Button(self, text='Закрыть', command=self.close).grid(row=1)
#
#     def close(self):
#         self.quit()
