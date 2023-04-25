import Tk, Board, Pg


class Game:
    def start(self):
        #Делается, на всякий случай, чтобы очистить файл от предыдущих записей
        with open('input.txt', 'w') as f:
            pass

        # Открывается окно ввода N, L, K
        start_window = Tk.NLKWindow()
        start_window.mainloop()

        # Выполняется поиск первого решения, если таковое есть, и его вывод в окно pygame
        Pg.GUI()

        # Если была нажата кнопки о записи решений в файл, выполняется поиск решений и их запись
        Board.Board()
        # self.wait_window = Tk.WaitWindow()
        # self.wait_window.mainloop()

    def error_occured(self, error, error_text):
        '''
        Функция вызывааемая для выводя в консоль вызванной ошибки

        Параметры:
            error:
                Класс вызванной ошибки
            erorr_text: str
                Сообщение о содержании ошибки
        '''
        raise error(error_text)


if __name__ == '__main__':
    game = Game()
    game.start()
