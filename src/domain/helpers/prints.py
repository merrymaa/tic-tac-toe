from constants import HUMAN, AI

""""Модуль для запуска игры в терминале"""


def print_field(field):
    print(f" {field.field[0][0]} | {field.field[0][1]} | {field.field[0][2]}")
    print("---+---+---")
    print(f" {field.field[1][0]} | {field.field[1][1]} | {field.field[1][2]}")
    print("---+---+---")
    print(f" {field.field[2][0]} | {field.field[2][1]} | {field.field[2][2]}")
    print()


def print_previe():
    field_previe = [i for i in range(1, 11)]
    print("Welcome to tic-tac-toe")
    print("Нумерация клеток происходит следующим образом:")
    print(f" {field_previe[0]} | {field_previe[1]} | {field_previe[2]}")
    print("---+---+---")
    print(f" {field_previe[3]} | {field_previe[4]} | {field_previe[5]}")
    print("---+---+---")
    print(f" {field_previe[6]} | {field_previe[7]} | {field_previe[8]}")
    print("Игра началась!")
    print()


def step_human(game):
    field = game.field
    steps = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), 9: (2, 2)}
    while True:
        try:
            step = int(input("Выберите ход: "))

            if step < 1 or step > 9:
                raise ValueError

            x, y = steps[step]
            if field.field[x][y] in [HUMAN, AI]:
                print("Клетка уже занята")
                raise ValueError
            field.field[x][y] = HUMAN
            return
        except:
            print("Введите корректный номер клетки")
