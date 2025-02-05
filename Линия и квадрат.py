import pygame
import sys
import os
from pygame.color import THECOLORS
import random
import tkinter as tk
from tkinter import font
import threading


pygame.init()
pygame.font.init()


"""Константы"""

LINE_WIDTH = 2  # толщина линий
CIRCLE_RADIUS = 20  # радиус точки

# количество строк и столбцов
BOARD_ROWS = 5
BOARD_COLS = BOARD_ROWS
GRID_SIZE = BOARD_COLS + 1

# Цвета
PLAYER_COLOR = (255, 59, 48)  # цвет игрока
COMPUTER_COLOR = (0, 122, 255)  # цвет компьютера
BACKGROUND_COLOR = (245, 245, 245)  # цвет фона
POINT_COLOR = (80, 80, 80)  # цвет точек


"""Задаем значения ширины и высоты окна игры для корректности отображения"""

screen_info = pygame.display.Info()
window_height = 648
window_width = 960

"""Проверяем запустится программа как скомпилированный файл"""

def resource_path(relative_path):
    # Проверяем, запускается ли программа как скомпилированный файл
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

"""Размеры рабочей зоны,  белого прямоугольника"""

EDGE_WIDTH = 15
y_white_rect = EDGE_WIDTH
x_white_rect = 327  # начальная координата по X

xlen_white_rect = 618
ylen_white_rect = 618

"""Координаты для точек"""

x_coor_st = x_white_rect + CIRCLE_RADIUS + LINE_WIDTH
Y_COOR_ST = y_white_rect + CIRCLE_RADIUS + LINE_WIDTH
div = ((ylen_white_rect - CIRCLE_RADIUS * 2 - LINE_WIDTH * 2) / 5)
step = (ylen_white_rect - CIRCLE_RADIUS * 2 - LINE_WIDTH * 2) / 5


"""Шрифты"""
"""Проверка компилируемости"""

font_path1 = resource_path("assets/YujiMai-Regular.ttf")
font_path2 = resource_path("assets/MarckScript-Regular.ttf")
font_path3 = resource_path("assets/Kablammo-Regular-VariableFont_MORF.ttf")

font_user1 = pygame.font.Font(font_path1, 20)
font_user2 = pygame.font.Font(font_path2, 20)
font_user3 = pygame.font.Font(font_path3, 20)


"""Создаем окно заданного размера"""

window = pygame.display.set_mode((window_width, window_height))
window.fill(BACKGROUND_COLOR)
pygame.display.set_caption('Линия и Квадраты')
icon = pygame.image.load(resource_path('assets/Значок.bmp'))
pygame.display.set_icon(icon)


"""Класс прямоугльник (ребра квадрата)"""

class Rectangle:
    def __init__(self, x, y, width, height, orientation, sensitivity=CIRCLE_RADIUS/3):
        self.rect = pygame.Rect(x, y, width, height)
        self.sensitivity_rect = self.rect.inflate(sensitivity, sensitivity)
        self.selected = False
        self.orientation = orientation
        self.color = None

    def draw(self, surface):
        if self.selected:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=7)
        else:
            pygame.draw.rect(surface, (224, 224, 224), self.rect, border_radius=7)
            pygame.draw.rect(surface, (200, 200, 200), self.rect, LINE_WIDTH, border_radius=7)

    def highlight(self, surface):
        if not self.selected:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=7)
            pygame.draw.rect(surface, (255, 223, 0), self.rect, LINE_WIDTH, border_radius=7)


"""Класс квадрат"""

class Square:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = None
        self.selected = False

        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

    def draw(self, surface):
        
        """Отрисовка квадратов"""
        
        if self.color and self.selected:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=7)

        else:
            pygame.draw.rect(surface, (224, 224, 224), self.rect, border_radius=7)
            pygame.draw.rect(surface, (200, 200, 200), self.rect, LINE_WIDTH, border_radius=7)

    def is_complete(self):
        
        """Проверяем, все ли линии вокруг квадрата выбраны."""
        
        return self.top.selected and self.bottom.selected and self.left.selected and self.right.selected

    def set_surrounding_lines(self, top, bottom, left, right):
        
        """Устанавливает четыре окружающие линии для квадрата."""
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def fill_square(self, color):
        
        """Заполнение, закрашивание квадрата"""
        self.color = color
        self.selected = True
        self.draw(window)

"""Класс кнопка"""

class Button:
    def __init__(self, x, y, width, height, color, text='', font_size=24, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.highlight_color = (255, 223, 0)
        self.is_active = True
        self.is_selected = False

    def draw(self, surface):
        if self.is_selected:
            draw_color = (0, 255, 0)  # Зеленый для выбранной кнопки
            pygame.draw.rect(surface, draw_color, self.rect, border_radius=7)

        elif self.is_active and self.rect.collidepoint(pygame.mouse.get_pos()):
            draw_color = self.highlight_color  # Подсветка для активной кнопки под курсором
            pygame.draw.rect(surface, (224, 224, 224), self.rect, border_radius=7)
            pygame.draw.rect(surface, draw_color, self.rect, LINE_WIDTH, border_radius=7)
        else:
            draw_color = self.color
            pygame.draw.rect(surface, (224, 224, 224), self.rect, border_radius=7)
            pygame.draw.rect(surface, draw_color, self.rect, LINE_WIDTH, border_radius=7)
         
        # Добавляем текст в центр кнопки
        if self.text:
            font = pygame.font.Font(font_path2, self.font_size)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def set_selected(self, state):
        # Устанавливаем состояние выбора (выбрана или нет)
        self.is_selected = state
    def set_active(self, state):
        # Меняем активность кнопки (можно выбрать или нет)
        self.is_active = state


    def is_clicked(self, event: object) -> object:
        # Проверка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_active:
            if self.rect.collidepoint(event.pos):
                return True
        return False


"""Графический интерфейс"""

"""Функция отрисовки основго (главного) поля"""
def main_field():

    pygame.draw.rect(window, (THECOLORS['white']), (x_white_rect, y_white_rect, xlen_white_rect, ylen_white_rect),
                    border_radius=7)
    pygame.draw.rect(window, (96, 255, 128), (x_white_rect, y_white_rect, xlen_white_rect, ylen_white_rect), LINE_WIDTH,
                    border_radius=7)

"""Функция отрисовки левого меню"""
def left_menu():

    pygame.draw.rect(window, (THECOLORS['white']), (EDGE_WIDTH, step + 3 * EDGE_WIDTH,  x_white_rect - 2 * EDGE_WIDTH, 1.65* div),
                     border_radius=7)
    pygame.draw.rect(window, (96, 255, 128), (EDGE_WIDTH, step + 3 * EDGE_WIDTH,  x_white_rect - 2 * EDGE_WIDTH, 1.65* div), LINE_WIDTH,
                     border_radius=7)

    tablo3 = font_user2.render(f'Выбор уровня сложности', True,(0, 0, 0),)
    window.blit(tablo3, (4 * EDGE_WIDTH, step + 4 * EDGE_WIDTH))


"""Функция для отрисовки точек поля игры"""
def draw_point(cols, rows):
  
    for i in range(0, cols + 1):
        for j in range(0, rows + 1):
            pygame.draw.circle(window, POINT_COLOR,
                               (x_coor_st + step * i, Y_COOR_ST + step * j),
                               CIRCLE_RADIUS)

"""Определение (инициализация) квадратов и прямоугольных линий"""
def create_grid():
    
    rectangles = []
    squares = []
    delta = 3
    for i in range(BOARD_COLS):
        for j in range(BOARD_ROWS + 1):
            rectangles.append(Rectangle(x_coor_st + delta + CIRCLE_RADIUS + step * i, CIRCLE_RADIUS + step * j,
                                        step - 2 * CIRCLE_RADIUS - 2 * delta, 2 * CIRCLE_RADIUS - 2 * delta,
                                        "horizontal"))
    for i in range(BOARD_COLS + 1):
        for j in range(BOARD_ROWS):
            rectangles.append(
                Rectangle(x_coor_st + delta - CIRCLE_RADIUS + step * i, Y_COOR_ST + delta + CIRCLE_RADIUS + step * j,
                          2 * CIRCLE_RADIUS - 2 * delta, step - 2 * CIRCLE_RADIUS - 2 * delta, "vertical"))

    for i in range(BOARD_COLS):
        row = []
        for j in range(BOARD_ROWS):
            square = Square(x_coor_st + CIRCLE_RADIUS + step * i, Y_COOR_ST + CIRCLE_RADIUS + step * j,
                            step - 2 * CIRCLE_RADIUS, step - 2 * CIRCLE_RADIUS)

            top = rectangles[i * GRID_SIZE + j]  # Верхняя линия квадрата
            bottom = rectangles[i * GRID_SIZE + j + 1]  # Нижняя линия квадрата
            left = rectangles[len(rectangles) // 2 + i * (GRID_SIZE - 1) + j]  # Левая линия квадрата
            right = rectangles[
                len(rectangles) // 2 + i * (GRID_SIZE - 1) + j + (GRID_SIZE - 1)]  # Правая линия квадрата

            square.set_surrounding_lines(top, bottom, left, right)
            row.append(square)
        squares.append(row)
    return rectangles, squares

"""Отрисовка счета"""

def draw_score(temp_res, temp_res2):
    window.fill((BACKGROUND_COLOR), (0, Y_COOR_ST + step * 3- CIRCLE_RADIUS, x_white_rect-LINE_WIDTH, 2*step+2*CIRCLE_RADIUS))
    font_user3 = pygame.font.Font(font_path3, 35)
    font_user4 = pygame.font.Font(font_path3, 76)

    number_tablo1 = font_user3.render(f'Игрок : ', True, PLAYER_COLOR)
    number_tablo2 = font_user3.render(f'Компьютер: ', True, COMPUTER_COLOR)
    window.blit(number_tablo1, (EDGE_WIDTH, Y_COOR_ST + step * 3-CIRCLE_RADIUS))
    window.blit(number_tablo2, (EDGE_WIDTH, Y_COOR_ST + step * 4-CIRCLE_RADIUS))

    number_tablo3 = font_user4.render(f'{temp_res}', True, PLAYER_COLOR)
    number_tablo4 = font_user4.render(f'{temp_res2}', True, COMPUTER_COLOR)
    window.blit(number_tablo3, (x_white_rect*3/4-3*LINE_WIDTH, Y_COOR_ST + step * 3))
    window.blit(number_tablo4, (x_white_rect*3/4-3*LINE_WIDTH, Y_COOR_ST + step * 4))

"""Функция запуска правил"""

def show_rules_window():
    # Создаем новое окно Tkinter

    root = tk.Tk()
    root.title("Правила игры")
    root.geometry("500x400")
    root.attributes("-topmost", True)
    print(font.families())

    rules_text = (
        "Правила игры:\n\n"
        "1. Игроки по очереди ставят линии между точками.\n"
        "2. Если линия завершает квадрат, игрок получает очко.\n"
        "3. Игра продолжается, пока все квадраты не заполнены.\n"
        "4. Побеждает тот, кто заполнил больше квадратов."
    )
    font1 = font.Font(family="Marck Script", size=12, weight="normal")
    label = tk.Label(root, text=rules_text, font=font1,   justify="left", padx=10, pady=10)
    label.pack()

    # Кнопка закрытия окна
    close_button = tk.Button(root, text="Закрыть", command=root.destroy)
    close_button.pack(pady=10)

    # Запускаем окно Tkinter
    root.mainloop()

# Функция для запуска окна с правилами в отдельном потоке независимом
def open_rules_in_thread():
    threading.Thread(target=show_rules_window, daemon=True).start()

"""Игровой цикл"""

"""проверка на замыкание квадрата с возвратом количества закрашенных квадратов"""
def check_squares(squares, color):
    score = 0
    square_filled = False
    for row in squares:
        for square in row:
            if not square.selected and square.is_complete():
                square.fill_square(color)
                square_filled = True
                score += 1
    return square_filled, score


"""Функция хода компьютера"""

def computer_move(rectangles, squares, difficulty):
    if difficulty == 'easy':
        return easy_move(rectangles)
    elif difficulty == 'medium':
        return medium_move(rectangles, squares)
    elif difficulty == 'hard':
        return hard_move(rectangles, squares)
    
"""Функция выбора уровня"""

def set_difficulty(level):
    print(level)
    global difficulty
    # Выбор кнопки, отображение выбранного состояния
    Button_EasyMove.set_selected(level == "easy")
    Button_MediumMove.set_selected(level == "medium")
    Button_HardMove.set_selected(level == "hard")
    difficulty = level
    # Блокируем кнопки выбора после начала игры
    Button_EasyMove.set_active(False)
    Button_MediumMove.set_active(False)
    Button_HardMove.set_active(False)
    
# Ход Компьютера на легком уровне
def easy_move(rectangles):
    available_rectangles = [ObjRect for ObjRect in rectangles if not ObjRect.selected]
    if available_rectangles:
        chosen_line = random.choice(available_rectangles)
        chosen_line.selected = True
        chosen_line.color = COMPUTER_COLOR
        return chosen_line.color

# Ход Компьютера на среднем уровне
def medium_move(rectangles, squares):

    for row in squares:
        for square in row:
            if square.is_complete():
                continue
            if square.top.selected + square.bottom.selected + square.left.selected + square.right.selected == 3:
                if not square.top.selected:
                    square.top.selected = True
                    square.top.color = COMPUTER_COLOR
                    return square.top.color
                elif not square.bottom.selected:
                    square.bottom.selected = True
                    square.bottom.color = COMPUTER_COLOR
                    return square.bottom.color
                elif not square.left.selected:
                    square.left.selected = True
                    square.left.color = COMPUTER_COLOR
                    return square.left.color
                elif not square.right.selected:
                    square.right.selected = True
                    square.right.color = COMPUTER_COLOR
                    return square.right.color
    return easy_move(rectangles)

# Ход Компьютера на сложном уровне
def hard_move(rectangles, squares):
    """ Первым шагом пытаемся завершить квадрат"""
    """Проверяем закрашен ли квадрат"""
    
    for row in squares:
        for square in row:
            if square.is_complete():
                continue  # Пропускаем уже завершенные квадраты

            """Если три из четырёх линий выбраны, завершаем квадрат"""
            
            if square.top.selected + square.bottom.selected + square.left.selected + square.right.selected == 3:
                if not square.top.selected:
                    square.top.selected = True
                    square.top.color = COMPUTER_COLOR
                    return square.top.color
                elif not square.bottom.selected:
                    square.bottom.selected = True
                    square.bottom.color = COMPUTER_COLOR
                    return square.bottom.color
                elif not square.left.selected:
                    square.left.selected = True
                    square.left.color = COMPUTER_COLOR
                    return square.left.color
                elif not square.right.selected:
                    square.right.selected = True
                    square.right.color = COMPUTER_COLOR
                    return square.right.color

    """Второй шаг: избегаем ходов, которые дают возможность игроку завершить квадрат"""
    safe_rectangles = []

    for row in squares:
        for square in row:
            if square.is_complete():
                continue
            available = [square.top, square.bottom, square.left, square.right]
            available = [rect for rect in available if not rect.selected]
            if len(available) == 3:
                safe_rectangles.extend(available)
                
    """Если безопасные линии есть, выбираем одну из них"""
    if safe_rectangles:
        chosen_line = random.choice(safe_rectangles)
        chosen_line.selected = True
        chosen_line.color = COMPUTER_COLOR
        return chosen_line.color

    """Если нет безопасных линий, играем на среднем уровне"""
    
    return medium_move(rectangles, squares)

"""Фукция возрата состояния активности кнопок, сброс их выбора"""
def reset_buttons():
    Button_EasyMove.set_active(True)
    Button_MediumMove.set_active(True)
    Button_HardMove.set_active(True)
    Button_EasyMove.is_selected = False
    Button_MediumMove.is_selected = False
    Button_HardMove.is_selected = False

"""Функция проверки завершения игры + ее перезапуск"""

def game_over(squares, player_score, computer_score):
    temp = []
    text_temp = None
    for row in squares:
        for square in row:
            if not square.selected:
                temp.append(square)
    if len(temp) == 0:
        if player_score == computer_score:
            text_temp = "Ничья!\n\n\nНажми любую кнопку\nмыши для продолжения..."

        elif player_score > computer_score:
            text_temp = f"Победил ИГРОК!!!\nсо счётом {player_score} : {computer_score}\n\n\nНажми любую кнопку\nмыши для продолжения..."

        elif player_score < computer_score:
            text_temp = f"Победил КОМПЬЮТЕР!!!\n со счётом  {computer_score} : {player_score} \n\n\nНажми любую кнопку\nмыши для продолжения..."
        window.fill(BACKGROUND_COLOR)
        font_user5 = pygame.font.Font(font_path1, 32)
        lines = text_temp.splitlines()
        for i, line in enumerate(lines):
            tablo5 = font_user5.render(line, True, (0, 0, 0))
            window.blit(tablo5, (EDGE_WIDTH, window_height / 4 + i * font_user5.get_linesize()))

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                window.fill(BACKGROUND_COLOR)
                reset_buttons()
                game_loop()

            if event.type == pygame.QUIT:
                sys.exit()

"""Игровой процесс, функция игры"""
def game_loop():
    
    main_field() # Создание главного окна
    left_menu() # Создание левого меню
    draw_point(BOARD_COLS, BOARD_ROWS) # Создание точек
    
    """создание массивов прямоугольников(линии, грани квадрата) и двумерного массива квадратов"""
    
    rectangles, squares = create_grid() # Создание прямоугольных линий и квадратов (инициализация)
        
    """условие определение хода"""
    
    player_turn = True
      
    """переменные для счета"""
    player_score = 0
    computer_score = 0

    for row in squares:
        for square in row:
            square.draw(window) 

    while True:     
        mouse_pos = pygame.mouse.get_pos() # Определние позиции мыши
        
        
        for event in pygame.event.get(): # Обработка событий
            """ Логика для перезапуска игры"""
            if Button_Rules.is_clicked(event):
                open_rules_in_thread()
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn: # Если мышь нажатаи ход игрока
                """ проверка нажатия ЛКМ"""
                if event.button == 1:
                    
                    if not Line_rect.selected: # пока не выбран ни одна линия и не выбраны кнопки, кнопки активные до первого хода
                        """ Выбор уровня сложности """
                        if Button_EasyMove.is_clicked(event):
                            set_difficulty("easy")

                        elif Button_MediumMove.is_clicked(event):
                            set_difficulty("medium")

                        elif Button_HardMove.is_clicked(event):
                            set_difficulty("hard")

                    if Button_restart.is_clicked(event): # кнопка перезапуска игры

                        reset_buttons()
                        game_loop()



                    for Line_rect in rectangles:
                        if Line_rect.sensitivity_rect.collidepoint(mouse_pos) and not Line_rect.selected:  # подсветка возможного хода
                            """Если мышь нажата, то:"""
                            Line_rect.selected = True # выбирается прямоугльник для закрашивания
                            Button_EasyMove.set_active(False)
                            Button_MediumMove.set_active(False)
                            Button_HardMove.set_active(False)

                            Line_rect.color = PLAYER_COLOR # цвет прямоугольника
                            """проверка можно закрашивать квадрат"""
                            square_filled, score = check_squares(squares, Line_rect.color)
                            """если квадрат нельзя закрасить, то переход хода"""
                            if not square_filled:
                                player_turn = False

                            if square_filled:
                                player_score += score
                                draw_score(player_score, computer_score)


        if not player_turn:
            pygame.time.wait(200)  # Задержка перед ходом компьютера

            computer_color = computer_move(rectangles, squares, difficulty)  # Компьютер делает ход
            """проверка можно закрашивать квадрат"""
            square_filled, score = check_squares(squares, computer_color)
            """если квадрат нельзя закрасить, то переход хода"""
            if not square_filled:
                player_turn = True
            """если линии закрашены то закрашиваем квадрат"""
            if square.selected:
                square.fill_square(square.color)

            if square_filled:
                computer_score += score



        """Подсветка линии (прямоугольников)"""
        for Line_rect in rectangles:
            Line_rect.draw(window)
            if Line_rect.sensitivity_rect.collidepoint(mouse_pos) and not Line_rect.selected:
                Line_rect.highlight(window)

        Button_restart.draw(window)
        Button_Rules.draw(window)
        Button_EasyMove.draw(window)
        Button_MediumMove.draw(window)
        Button_HardMove.draw(window)
        draw_score(player_score, computer_score)
        game_over(squares,player_score, computer_score)

        pygame.display.flip()


class StartWindow:
    def __init__(self, image_path, width, height, caption="Start Window"):
        """
        Инициализирует стартовое окно Pygame.

        Args:
            image_path (str): Путь к изображению для отображения.
            width (int): Ширина окна.
            height (int): Высота окна.
            caption (str, optional): Заголовок окна. По умолчанию "Start Window".
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        try:
            self.image = pygame.image.load(image_path).convert() #Convert для повышения производительности
        except pygame.error as message:
            print('Не удалось загрузить изображение:', image_path)
            raise SystemExit(message)

        self.running = False

    def run(self):
        """
        Запускает стартовое окно и ожидает нажатия клавиши для закрытия.
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.running = False # Закрываем окно при любом нажатии клавиши

            self.screen.blit(self.image, (0, 0)) # Отображаем изображение
            pygame.display.flip() # Обновляем экран
        self.screen.fill((255, 255, 255))


start_window = StartWindow("assets/start_window.jpg", window_width, window_height, "Точки и квадраты")
start_window.run()

Button_restart = Button(EDGE_WIDTH,  EDGE_WIDTH,  x_white_rect - 2 * EDGE_WIDTH, step / 2,(224, 224, 224),
                            "Новая игра", 30, (0, 0, 0))

Button_Rules = Button(EDGE_WIDTH,  step / 2 + 2 * EDGE_WIDTH, x_white_rect - 2 * EDGE_WIDTH, step / 2, (224, 224, 224),
                              "Правила игры ", 30, (0, 0, 0))

Button_EasyMove = Button(EDGE_WIDTH + 2*LINE_WIDTH, step + 6.5 * EDGE_WIDTH, x_white_rect - 2 * EDGE_WIDTH - 4*LINE_WIDTH, 2 * CIRCLE_RADIUS, (255, 255, 255),
                              "Легкий уровень",20, (0, 0, 0))

Button_MediumMove = Button(EDGE_WIDTH + 2*LINE_WIDTH, step + 6.5 * EDGE_WIDTH + 2 * CIRCLE_RADIUS + 2*LINE_WIDTH, x_white_rect - 2 * EDGE_WIDTH - 4*LINE_WIDTH,
                           2 * CIRCLE_RADIUS, (255, 255, 255),
                          "Средний уровень", 20, (0, 0, 0))

Button_HardMove = Button(EDGE_WIDTH + 2*LINE_WIDTH, step + 6.5 * EDGE_WIDTH + 4 * CIRCLE_RADIUS + 4*LINE_WIDTH, x_white_rect - 2 * EDGE_WIDTH - 4*LINE_WIDTH,
                           2 * CIRCLE_RADIUS, (255, 255, 255),
                         "Сложный уровень", 20, (0, 0, 0))

difficulty = 'easy'

game_loop()
sys.exit()
