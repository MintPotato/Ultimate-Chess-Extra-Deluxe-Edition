import Tk, Board, Pg


class Game:
    def __init__(self):
        pass

    def start(self):
        with open('input.txt', 'w') as f:
            pass

        self.start_window = Tk.NLKWindow()
        self.start_window.mainloop()
        Pg.GUI()
        Board.Board()
        # self.wait_window = Tk.WaitWindow()
        # self.wait_window.mainloop()

    def error_occured(self, error, error_text):
        raise error(error_text)



if __name__ == '__main__':
    game = Game()
    game.start()
