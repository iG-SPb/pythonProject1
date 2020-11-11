import random

# размер игрового поля
number_line = 3  # количество строк
number_column = 3  # количество столбцов
SYMBOL_HUMAN = "X"  # символ, которым играет человек
SYMBOL_AI = "S"  # символ, которым играет искусственный интеллект
SYMBOL_EMPTY = " "  # символ пустой ячейки
number_victory = 3  # количество символов для победы
EXIT_GAME = False  # признак окончания игры человеком
# координаты последнего хода человека
pos_x_human = 0
pos_y_human = 0
# координаты последнего хода машины
generate_x = 0
generate_y = 0
colGreen = "\u001B[32m"  # зеленый цвет символов в терминале
colRed = "\u001B[31m"  # красный цвет символов в терминале
colNo = "\u001B[0m"  # исходный цвет символов в терминале

# инициализация массива пустыми значениями
array_game = [[SYMBOL_EMPTY for column in range(number_column)] for line in range(number_line)]


# функция печати массива
def print_array(array_param):
    global pos_x_human, pos_y_human, generate_x, generate_y
    # печать номеров столбцов
    i = 1  # нулевой элемент пропускаем
    print(" |", end='')  # отступ на 1 элемент и разделитель (т.к. нужно место под нумерацию строк)
    while i < (len(array_param[0]) * 2):  # цикл длиннее размера строки в 2 раза
        if i % 2 != 0:  # определяем нечетный элемент
            print(i // 2 + 1, end='|')  # печать номера столбца и разделителя
        i += 1  # увеличение номера столбца
    print()  # перевод строки после печати всей строки

    i = 1  # первая строка
    for element in array_param:  # проход по строкам
        print(i, end='|')  # печать номера строки
        i += 1  # увеличение номера строки
        num_element = 1
        for one_element in element:  # проход по столбцам строки
            if (i - 1) == pos_x_human and num_element == pos_y_human:  # если совпало с последним ходом человека
                print(colGreen, one_element, colNo, sep='', end='|')
            elif (i - 1) == (generate_x + 1) and num_element == (generate_y + 1):  # если совпало с последним ходом AI
                print(colRed, one_element, colNo, sep='', end='|')
            else:
                print(one_element, end='|')  # печать элемента и разделителя без совпадений с последними ходами
            num_element += 1
        print()  # перевод строки после печати всей строки


# проверка свободных ходов
def check_step(current_step, max_step):
    return current_step == max_step


# ход человека
def step_human():
    global pos_x_human, pos_y_human, EXIT_GAME
    end_iteration = True
    while end_iteration:
        input_string = input("Введите координаты (строка столбец) >>").split()
        if input_string[0] == "q":  # если "q" то выходим из игры
            EXIT_GAME = True
            return EXIT_GAME
        pos_x_human = int(input_string[0])
        pos_y_human = int(input_string[1])
        if number_line >= pos_x_human > 0 and number_column >= pos_y_human > 0:  # проверка допустимости значений
            if array_game[pos_x_human - 1][pos_y_human - 1] == SYMBOL_EMPTY:  # проверка свободной ячейки
                array_game[pos_x_human - 1][pos_y_human - 1] = SYMBOL_HUMAN  # запись в свободную ячейку
                end_iteration = False
        else:
            print("Недопустимые значения")
    return EXIT_GAME


# ход машины
def step_ai():
    global generate_x, generate_y
    end_iteration = True
    while end_iteration:
        generate_x = random.randint(0, number_line - 1)  # генерация номера строки
        generate_y = random.randint(0, number_column - 1)  # генерация номера столбца
        if array_game[generate_x][generate_y] == SYMBOL_EMPTY:  # проверка свободной ячейки
            array_game[generate_x][generate_y] = SYMBOL_AI  # запись в свободную ячейку
            end_iteration = False


# проверка горизонтали и вертикали
def check_line(symbol):
    global array_game, number_line, number_column
    for line in range(number_line - 1):
        count_symbol_line = 0
        count_symbol_column = 0
        for position in range(number_column):
            if array_game[line][position] == symbol:  # подсчет по строкам
                count_symbol_line += 1
                if count_symbol_line == number_victory:
                    return True
            else:
                count_symbol_line = 0
            if array_game[position][line] == symbol:  # подсчет по столбцам
                count_symbol_column += 1
                if count_symbol_column == number_victory:
                    return True
            else:
                count_symbol_column = 0
    return False


# проверка диагоналей
def check_diagonal(symbol):
    global array_game, number_line, number_column
    count_symbol_diagonal_xy = 0
    count_symbol_diagonal_yx = 0

    # проход от первой линии до последней минус количество символов для победы
    for position_x in range(number_column - number_victory + 1):
        # проход от первого столбца до последнего минус количество символов для победы
        for position_y in range(number_line - number_victory + 1):
            # проход по диагонали из точки position_j, position_z
            for position_z in range(number_line - position_x):
                # проверка выхода за границы поля
                if position_x + position_z < number_line and position_y + position_z < number_column:
                    if array_game[position_x + position_z][position_y + position_z] == symbol:  # проверка 1 диагонали
                        count_symbol_diagonal_xy += 1
                        if count_symbol_diagonal_xy == number_victory:
                            return True
                    else:
                        count_symbol_diagonal_xy = 0
                    if array_game[position_x + position_z][number_column - position_y - position_z - 1] == symbol:  # проверка 2 диагонали
                        count_symbol_diagonal_yx += 1
                        if count_symbol_diagonal_yx == number_victory:
                            return True
                    else:
                        count_symbol_diagonal_yx = 0
    return False


# проверка победы
def check_victory(check_symbol):
    global number_column, number_line, number_victory
    # проверка линии по горизонтали и вертикали
    if check_line(check_symbol):
        return True
    # проверка диагонали - это надо дописать
    if check_diagonal(check_symbol):
        return True
    return False


GAME_OVER = True  # признак окончания игры
victory_human = False  # признак выигрыша человека
victory_ai = False  # признак выигрыша машины
game_over = False  # признак окончания игры (нет ходов)
max_count_step = number_line * number_column  # максимальное количество ходов
count_step = 0  # текущий ход

print_array(array_game)  # печать текущего поля
while GAME_OVER:  # играем до победы или окончания ходов
    if step_human():  # ход человека
        print("Выход из игры")
        break  # выход если был ввод "q"
    count_step += 1  # увеличение счетчика текущего хода
    if check_victory(SYMBOL_HUMAN):  # проверка победы человека
        print_array(array_game)  # печать текущего поля
        print("You victory")
        break
    if check_step(count_step, max_count_step):  # проверка свободных ходов
        print_array(array_game)  # печать текущего поля
        print("End steps")
        break
    step_ai()  # ход машины
    count_step += 1  # увеличение счетчика текущего хода
    if check_victory(SYMBOL_AI):  # проверка победы машины
        print_array(array_game)  # печать текущего поля
        print("AI victory")
        break
    if check_step(count_step, max_count_step):  # проверка свободных ходов
        print_array(array_game)  # печать текущего поля
        print("End steps")
        break
    print_array(array_game)  # печать текущего поля
