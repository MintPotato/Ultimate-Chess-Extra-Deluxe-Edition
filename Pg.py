import pygame, Figures, Board

class GUI:
    def __init__(self):
        '''
        Инициализация окна с выводом одного из решений, если такое существует
        '''

        board = Board.Board(True)

        self.razmernost, self.board = board.N, board.only_fist_solve()
        if not self.board:
            self.no_solution_found()
        self.cell_size = 400 // self.razmernost



        pygame.init()
        self.display = pygame.display.set_mode((self.cell_size * self.razmernost, 500))
        self.display.fill('white')
        self.close_btn = CloseButton(self.display, 40, 420, 200, 50, text='Записать решения в файл', onClickFunc=self.close)

        self.otrisovka(self.razmernost)

        self.run = True
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.close_btn.running()

            pygame.display.update()


    def close(self):
        '''Функция кнопки завершающая работу окна с визуализацией решения'''
        self.run = False

    def otrisovka(self, lines: int):
        '''
        Функция отвечающая за разметку доски и отрисовки на ней условных фигур и клеток их боя

        Параметры:
            lines: int
                Число отражающее количество размерность доски
        '''
        board_size = self.cell_size * self.razmernost
        for i in range(lines + 1):
            pygame.draw.line(self.display, 'black', (self.cell_size * i, 0), (self.cell_size * i, board_size))
            pygame.draw.line(self.display, 'black', (0, self.cell_size * i), (board_size, self.cell_size * i))
            pygame.display.flip()

        for i in range(lines):
            for j in range(self.razmernost):
                if isinstance(self.board[i][j], Figures.Figure):
                    color = self.board[i][j].color
                    pygame.draw.rect(
                        self.display, color,
                        (self.cell_size * j + 1, self.cell_size * i + 1, self.cell_size - 1, self.cell_size - 1)
                    )
                elif self.board[i][j] == '*':
                    pygame.draw.rect(
                        self.display,
                        'blue',
                        (self.cell_size * j + 1, self.cell_size * i + 1, self.cell_size - 1, self.cell_size - 1)
                    )
        pygame.display.flip()


    def no_solution_found(self):
        '''
        Функция вызываемая в случае ненахождения ни одного решения для заданных вводных.

        Создает окно с надписью "No solution" и по закрытии завершает работу программы, тк дальнейшее ее выполнение лишено смысла
        '''
        pygame.init()

        self.display = pygame.display.set_mode((400, 400))
        self.display.fill('white')

        font = pygame.font.SysFont('TimesNewRoman', 50)
        text = font.render('No solution', True, 'black')

        self.display.blit(text, (80, 150))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open ('output.txt', 'w') as f:
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
        self.color = ((200,200,200))
        self.color_hover = ((50,50,50))

        self.pressed = False


        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_txt = pygame.font.SysFont('TimesNewRoman', 15).render(text, True, 'black')


    def running(self):
        '''
        Функция вызываемая во время работы окна для проверки взаимодействия пользователя с кнопкой
        '''
        mouse = pygame.mouse.get_pos()
        self.button_surface.fill(self.color)
        if self.button_rect.collidepoint(mouse):
            self.button_surface.fill(self.color_hover)
            if pygame.mouse.get_pressed()[0]:
                if not self.pressed:
                    self.onclickFunction()
            else:
                self.pressed = False


        self.button_surface.blit(self.button_txt, [
            self.button_rect.width/2 - self.button_txt.get_rect().width/2,
            self.button_rect.height/2 - self.button_txt.get_rect().height/2
        ])
        self.screen.blit(self.button_surface, self.button_rect)

