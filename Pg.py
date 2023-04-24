import pygame, Figures, Board


# Переделать метод отрисовки под solution_found
class GUI:
    def __init__(self):
        '''
        Формирования поиска решения для отрисовки, и в зависимости от результата запуск отрисовки разных окон
        '''

        board = Board.Board(only_first_solution=True)

        razmernost, board = board.N, board.only_fist_solve()

        if board:
            self.run = True
            self.solution_found(razmernost, board)
        else:
            self.no_solution_found()

    def close(self):
        '''Функция кнопки завершающая работу окна с визуализацией решения'''
        self.run = False

    def solution_found(self, lines: int, board: list[list]):
        '''
        Функция вызываемая в случае если решение было найдено

        Создает окно с отрисовкой найденного решения и кнопкой для осуществления записи всех решений в файл

        Параметры:
            lines: int
                Количество строк/столбцов доски в найденом решении
            board: list[list]
                Матрица доски найденного решения
        '''

        # Создание размерности клетки на доске и самой доски
        cell_size = 400 // lines
        board_size = cell_size * lines

        pygame.init()
        display = pygame.display.set_mode((board_size, board_size + 100))
        display.fill('white')
        self.close_btn = CloseButton(display, 40, board_size + 20, 200, 50, text='Записать решения в файл',
                                     onClickFunc=self.close)

        # Разметка доски в окне
        for i in range(lines + 1):
            pygame.draw.line(display, 'black', (cell_size * i, 0), (cell_size * i, board_size))
            pygame.draw.line(display, 'black', (0, cell_size * i), (board_size, cell_size * i))

        # Закрашивание клеток фигур и боя
        for i in range(lines):
            for j in range(lines):
                if isinstance(board[i][j], Figures.Figure):
                    color = board[i][j].color
                    pygame.draw.rect(
                        display, color,
                        (cell_size * j + 1, cell_size * i + 1, cell_size - 1, cell_size - 1)
                    )
                elif board[i][j] == '*':
                    pygame.draw.rect(
                        display,
                        'blue',
                        (cell_size * j + 1, cell_size * i + 1, cell_size - 1, cell_size - 1)
                    )

        pygame.display.flip()

        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Проверка взаимодействия с кнопкой
            self.close_btn.running()

            pygame.display.update()

    def no_solution_found(self):
        '''
        Функция вызываемая в случае ненахождения ни одного решения для заданных вводных.

        Создает окно с надписью "No solution" и по закрытии завершает работу программы, тк дальнейшее ее выполнение лишено смысла
        '''

        pygame.init()
        display = pygame.display.set_mode((400, 400))
        display.fill('white')

        # Создание надписи и ее положения в окне
        font = pygame.font.SysFont('TimesNewRoman', 50)
        text = font.render('No solution', True, 'black')
        display.blit(text, (80, 150))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('output.txt', 'w') as f:
                        f.write('No solution')
                        exit()

            pygame.display.update()


class CloseButton:
    '''
    Класс имитирующий кнопку завершения работы приложения
    '''

    def __init__(self, screen, x, y, width, height, text='Button', onClickFunc=None):
        '''
        Инициализация кнопки на экране

        Параметры:
            screen:
                Экран на который будет добавлена кнопка
            x, y: int
                Положение кнопки на экране
            width, height: int
                Размерность кнопки
            text: str
                Текст внутри кнопки
            onClickFunc: function
                Функция выполняемая при нажатии
        '''
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onClickFunc
        self.color = ((200, 200, 200))
        self.color_hover = ((50, 50, 50))


        # Создание надписи внутри кнопки
        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_txt = pygame.font.SysFont('TimesNewRoman', 15).render(text, True, 'black')

        # Задавание размеров кнопки и ее положения
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def running(self):
        '''
        Функция вызываемая во время работы окна для проверки взаимодействия пользователя с кнопкой
        '''

        mouse = pygame.mouse.get_pos() # Получение положения мыши в окне
        self.button_surface.fill(self.color)

        # Проверка на положение мыши внутри рамки кнопки
        if self.button_rect.collidepoint(mouse):
            self.button_surface.fill(self.color_hover)

            # Если при этом кнопка была нажата, то выполнить функцию заданную кнопке
            if pygame.mouse.get_pressed()[0]:
                self.onclickFunction()

        # Задавание положения текста внутри кнопки
        self.button_surface.blit(self.button_txt, [
            self.button_rect.width / 2 - self.button_txt.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_txt.get_rect().height / 2
        ])

        # Отображение кнопки в заданном окне
        self.screen.blit(self.button_surface, self.button_rect)
