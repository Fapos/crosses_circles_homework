from dataclasses import dataclass
from typing import List
from enum import Enum


class States(Enum):
    player_one_step: int = 1
    player_two_step: int = 2
    player_one_win: int = 3
    player_two_win: int = 4
    draw: int = 5
    game_on: int = 6


class CrossesCircles:
    def __init__(self):
        self.field_size = 3
        self.curr_state = None
        self.step_state = States.player_one_step
        self.game_field: List[List[str]] = [['-' for j in range(self.field_size)] for i in range(self.field_size)]
        self.print_field()
        ...

    def print_field(self):
        """
        Вывод игрового поля в консоль.

        :return:
        """
        print(' ', *[i for i in range(self.field_size)])
        for i, row in enumerate(self.game_field):
            print(i, *row)

    def set_cell_on_field(self, coord: str) -> bool:
        """
        Установка значения, в указанную пользователем ячейку.

        :param coord: Координаты ячейки.
        :return:
        """
        try:
            int(coord)
        except ValueError:
            print('Введены некорректные значения координат клетки, выберите другую клетку.')
            return False

        _coord = []
        _coord = list(coord)
        if len(_coord) == 2:
            _coord = list(map(int, _coord))
        else:
            _coord = list(map(int, coord.split(' ')))
            if len(_coord) != 2:
                print('Введены некорректные значения координат клетки, выберите другую клетку.')
                return False

        sep = 'x'
        if self.step_state == States.player_two_step:
            sep = 'o'

        if _coord[0] > self.field_size - 1 or _coord[1] > self.field_size - 1:
            print('Введены координаты клетки, выходящие за пределы игрового поля, выберите другую клетку.')
            return False
        if self.game_field[_coord[0]][_coord[1]] != '-':
            print('Эта клетка занята, выберите другую.')
            return False
        self.game_field[_coord[0]][_coord[1]] = sep
        return True

    def check_field_state(self):
        """
        Проверка поля на выйгрыш одного из пользователей.

        :return:
        """

        def check_diagonals(_range):
            _cnt_x = 0
            _cnt_o = 0
            for _i in range(*_range):
                if self.game_field[_i][_i] == 'x':
                    _cnt_x += 1
                if self.game_field[_i][_i] == 'o':
                    _cnt_o += 1

            if _cnt_x == self.field_size:
                return 'x'
            if _cnt_o == self.field_size:
                return 'o'
            return None

        def check_columns(_range):
            for _i in range(*_range):
                _cnt_x = 0
                _cnt_o = 0
                for _j in range(*_range):
                    if self.game_field[_j][_i] == 'x':
                        _cnt_x += 1
                    if self.game_field[_j][_i] == 'o':
                        _cnt_o += 1

                if _cnt_x == self.field_size:
                    return 'x'
                if _cnt_o == self.field_size:
                    return 'o'

        # Проверка строк
        for row in self.game_field:
            if row == ['x', 'x', 'x']:
                self.curr_state = States.player_one_win
                return
            if row == ['o', 'o', 'o']:
                self.curr_state = States.player_two_win
                return

        # Проверка столбцов
        if check_columns([0, self.field_size]) == 'x':
            self.curr_state = States.player_one_win
            return

        if check_columns([0, self.field_size]) == 'o':
            self.curr_state = States.player_two_win
            return

        # Проверка диагоналей
        if check_diagonals([0, self.field_size]) == 'x':
            self.curr_state = States.player_one_win
            return

        if check_diagonals([0, self.field_size]) == 'o':
            self.curr_state = States.player_two_win
            return

        if check_diagonals([self.field_size - 1, -1, -1]) == 'x':
            self.curr_state = States.player_one_win
            return

        if check_diagonals([self.field_size - 1, -1, -1]) == 'o':
            self.curr_state = States.player_two_win
            return

    def game_loop(self):
        """
        Игровой цикл.

        :return:
        """
        max_steps = self.field_size ** 2
        cnt_steps = 0
        while self.curr_state == States.game_on and cnt_steps < max_steps:
            step = input('Введите номер строки и номер столбца: ')
            result = self.set_cell_on_field(step)

            if result:
                self.check_field_state()
                self.print_field()
                if self.step_state == States.player_one_step:
                    self.step_state = States.player_two_step
                else:
                    self.step_state = States.player_one_step
            cnt_steps += 1

        if cnt_steps == max_steps:
            self.curr_state = States.draw

    def run(self):
        """
        Метод запуска игры.

        :return:
        """
        self.curr_state = States.game_on
        self.game_loop()

        if self.curr_state == States.player_one_win:
            print('Победил игрок 1')

        if self.curr_state == States.player_two_win:
            print('Победил игрок 2')

        if self.curr_state == States.draw:
            print('Ничья')


def main():
    run_game = True
    while run_game:
        game = CrossesCircles()
        game.run()
        replay = input('Сыграть еще? Введите "yes", если хотите сыграть еще раз: ')
        if replay != 'yes':
            run_game = False


if __name__ == '__main__':
    main()