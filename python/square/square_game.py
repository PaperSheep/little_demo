import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime 
import threading
import random

WINDOW_X_SIZE = 800
WINDOW_Y_SIZE = 700

class Game_manager:
    game_window = None
    b_play = None
    l_title = None
    canvas = None
    square = None
    bg_square = None
    is_clear = None
    time_count = None  
    tip_canvas = None
    square_type = None
    tip_bg = None
    l_score = None
    score = None
    time_speed = None
    def __init__(self, game_window):
        self.game_window = game_window
        self.b_play = tk.Button(self.game_window, text="开始游戏", font=('宋体', 12), width=10, height=3, command=self.play_game)
        self.b_play.focus_set()
        self.b_play.bind('<Return>', func=self.play_game)
        self.b_play.place(x=WINDOW_X_SIZE/2-50, y=WINDOW_Y_SIZE/2-20, anchor='nw')
        self.l_title = tk.Label(self.game_window, text=" 魔术方块 ", bg = 'pink', font=('宋体', 18), width=25, height=3)
        self.l_title.place(x=WINDOW_X_SIZE/2-150, y=WINDOW_Y_SIZE/2-220, anchor='nw')
        self.bg_square = []
        self.is_clear = True
        self.time_count = datetime.now()
        self.tip_bg = []
        self.score = 0
        self.time_speed = 1
    def play_game(self, event=None):
        self.b_play.destroy()
        self.l_title.destroy()
        self.l_score = tk.Label(self.game_window, text="得分:{}".format(self.score), bg = 'pink', font=('宋体', 12), width=15, height=3)
        self.l_score.place(x=620, y=500, anchor='nw')
        self.draw_bg()
        self.square = Square(random.choice(range(7)))
        self.draw_square()
        self.draw_tip_square()
        self.game_window.update()
        try:
            while True:
                time.sleep(0.033)
                self.clear_square()
                self.is_clear = True
                self.game_window.update()
                self.draw_square()
                self.is_clear = False
                self.game_window.update()
                if (datetime.now() - self.time_count).total_seconds() > 0.8 / self.time_speed:
                    self.time_count = datetime.now()
                    self.control_square('', auto=True)
        except:
            pass
    def draw_tip_square(self):
        self.square_type = random.choice(range(7))
        for point in self.tip_bg:  # 清理
            self.tip_canvas.delete(point)
        if self.square_type == 0:
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 40, 80, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 40, 120, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
        elif self.square_type == 1:
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 40, 80, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(120, 80, 160, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
        elif self.square_type == 2:
            self.tip_bg.append(self.tip_canvas.create_rectangle(0, 80, 40, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(120, 80, 160, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
        elif self.square_type == 3:
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 40, 80, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(0, 40, 40, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
        elif self.square_type == 4:
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 40, 80, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(0, 80, 40, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
        elif self.square_type == 5:
            self.tip_bg.append(self.tip_canvas.create_rectangle(0, 80, 40, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 40, 120, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
        elif self.square_type == 6:
            self.tip_bg.append(self.tip_canvas.create_rectangle(120, 40, 160, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 40, 120, 80, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(40, 80, 80, 120, fill='Lightyellow'))
            self.tip_bg.append(self.tip_canvas.create_rectangle(80, 80, 120, 120, fill='Lightyellow'))
    def control_square(self, key, auto=False):
        if auto:
            self.time_speed = 1
            if not self.check_down():
                for point in self.square.square_info:
                    point['y'] += 40
                return
        elif key.keycode == 39:
            if not self.check_right():
                for point in self.square.square_info:
                    point['x'] += 40
                return
        elif key.keycode == 37:
            if not self.check_left():
                for point in self.square.square_info:
                    point['x'] -= 40
                return
        elif key.keycode == 40:
            self.time_speed = 10
            return
        elif key.keycode == 38:
            temp = []
            for point in self.square.square_info:
                temp.append({'x': point['x'], 'y': point['y'], 'point': point['point'], 'direction': point['direction']})
            self.square.change_direction()
            left_side = 10
            right_side = 370
            for point in self.square.square_info:
                if point['x'] < left_side:
                    left_side = point['x']
                elif point['x'] > right_side:
                    right_side = point['x']
            if left_side < 10:
                for point in self.square.square_info:
                    point['x'] -= (left_side - 10)
            elif right_side > 370:
                for point in self.square.square_info:
                    point['x'] -= (right_side - 370)
            for point in self.square.square_info:
                for x in self.bg_square:
                    for y in x:
                        if point['x'] == y['x'] and point['y'] == y['y']:
                            self.square.square_info = temp
                            return 
            return
    def check_left(self):
        for point in self.square.square_info:
            if point['x'] <= 10:
                return True
            for x in self.bg_square:
                for y in x:
                    if point['x'] - 40 == y['x'] and point['y'] == y['y']:
                        return True
        else:
            return False
    def check_right(self):
        for point in self.square.square_info:
            if point['x'] >= 370:
                return True
            for x in self.bg_square:
                for y in x:
                    if point['x'] + 40 == y['x'] and point['y'] == y['y']:
                        return True
        else:
            return False
    def create_bg_square(self):
        self.bg_square.append(self.square.square_info)
        if self.is_clear:
            self.draw_square()
        self.square = Square(self.square_type)
        self.draw_tip_square()
        self.draw_square()
        self.game_window.update()
        self.check_remove()
    # def check_remove(self):
    #     word_dict = {}
    #     for x in self.bg_square:
    #         for y in x:
    #             if str(y['y']) not in word_dict:
    #                 word_dict[str(y['y'])] = 1
    #             else:
    #                 word_dict[str(y['y'])] += 1
    #     remove_y = []
    #     for i in y_point:
    #         if word_dict[str(i)] >= 10:
    #             remove_y.append(i)
    #     for i in remove_y:
    #         for x in self.bg_square:
    #             for y in x[:]:
    #                 if y['y'] == i:
    #                     x.remove(y)
    #                     self.canvas.delete(y['point'])
    #     for x in self.bg_square[:]:  # 清理多余的空列表
    #         if x == []:
    #             self.bg_square.remove(x)
    #     for i in remove_y:
    #         for x in self.bg_square:
    #             for y in x:
    #                 if y['y'] < i:  # 背景方块在消掉的上面
    #                     self.canvas.delete(y['point'])
    #                     y['y'] += 40 * len(remove_y)
    #                     y['point'] = self.canvas.create_rectangle(y['x'], y['y'], y['x'] + 40, y['y'] + 40, fill='Lightyellow')
    #     self.score += len(remove_y)
    #     self.l_score.config(text='得分:{}'.format(self.score))
    def check_remove(self):
        temp_y_point = []
        for x in self.bg_square:
            for y in x:
                temp_y_point.append(y['y'])
        word_dict = {}
        for word in temp_y_point:
            if str(word) not in word_dict:
                word_dict[str(word)] = 1
            else:
                word_dict[str(word)] += 1
        y_point = list(set(temp_y_point))
        remove_y = []
        for i in y_point:
            if word_dict[str(i)] >= 10:
                remove_y.append(i)
        for i in remove_y:
            for x in self.bg_square:
                for y in x[:]:
                    if y['y'] == i:
                        x.remove(y)
                        self.canvas.delete(y['point'])
        for x in self.bg_square[:]:
            if x == []:
                self.bg_square.remove(x)
        for i in remove_y:
            for x in self.bg_square:
                for y in x:
                    if y['y'] < i:
                        self.canvas.delete(y['point'])
                        y['y'] += 40 * len(remove_y)
                        y['point'] = self.canvas.create_rectangle(y['x'], y['y'], y['x'] + 40, y['y'] + 40, fill='Lightyellow')
        self.score += len(remove_y)
        self.l_score.config(text='得分:{}'.format(self.score))
    def check_down(self):
        for point in self.square.square_info:
            if point['y'] >= 450:
                self.create_bg_square()
                return True
            for x in self.bg_square:
                for y in x:
                    if point['x'] == y['x'] and point['y'] + 40 == y['y']:
                        self.create_bg_square()
                        return True
        else:
            return False
    def clear_square(self):
        for point in self.square.square_info:
            self.canvas.delete(point['point'])
    def draw_square(self):
        for point in self.square.square_info:
            point['point'] = self.canvas.create_rectangle(point['x'], point['y'], point['x'] + 40, point['y'] + 40, fill='Lightyellow')
    def draw_bg(self):
        self.canvas = tk.Canvas(self.game_window, width=420, height=500, bg='pink')
        self.canvas.place(x=(WINDOW_X_SIZE-420)/2, y=(WINDOW_Y_SIZE-500)/2, anchor='nw')
        self.tip_canvas = tk.Canvas(self.game_window, width=160, height=160, bg='pink')
        self.tip_canvas.place(x=620, y=300, anchor='nw')
        # self.canvas.create_line(10, 10, 410, 10) 
        self.canvas.create_line(10, 490, 410, 490) 
        self.canvas.create_line(10, 0, 10, 490) 
        self.canvas.create_line(410, 0, 410, 490)


class Square:
    square_info = None
    square_type = None
    def __init__(self, square_type):
        self.square_type = square_type
        self.square_info = []
        self.random_square()
    def random_square(self):
        # self.square_type = random.choice(range(7))
        if self.square_type == 0:
            self.square_one_type()
        elif self.square_type == 1:
            self.square_tow_type()
        elif self.square_type == 2:
            self.square_three_type()
        elif self.square_type == 3:
            self.square_four_type()
        elif self.square_type == 4:
            self.square_five_type()
        elif self.square_type == 5:
            self.square_six_type()
        elif self.square_type == 6:
            self.square_seven_type()
    def square_one_type(self):  # 田字
        self.square_info.append({'x': 170,'y': -110, 'point': '', 'direction': 1})
        self.square_info.append({'x': 210,'y': -110, 'point': '', 'direction': ''})
        self.square_info.append({'x': 170,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
    def square_tow_type(self):  # 7字
        self.square_info.append({'x': 170,'y': -110, 'point': '', 'direction': 1})
        self.square_info.append({'x': 170,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 250,'y': -70, 'point': '', 'direction': ''})
    def square_three_type(self):  # 一字
        self.square_info.append({'x': 130,'y': -70, 'point': '', 'direction': 1})
        self.square_info.append({'x': 170,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 250,'y': -70, 'point': '', 'direction': ''})
    def square_four_type(self):  # Z字
        self.square_info.append({'x': 170,'y': -110, 'point': '', 'direction': 1})
        self.square_info.append({'x': 210,'y': -110, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 250,'y': -70, 'point': '', 'direction': ''})
    def square_five_type(self): # 山字
        self.square_info.append({'x': 210,'y': -110, 'point': '', 'direction': 1})
        self.square_info.append({'x': 170,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 250,'y': -70, 'point': '', 'direction': ''})
    def square_six_type(self): # 正7字
        self.square_info.append({'x': 250,'y': -110, 'point': '', 'direction': 1})
        self.square_info.append({'x': 170,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 250,'y': -70, 'point': '', 'direction': ''})
    def square_seven_type(self): # 反Z字
        self.square_info.append({'x': 210,'y': -110, 'point': '', 'direction': 1})
        self.square_info.append({'x': 170,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 210,'y': -70, 'point': '', 'direction': ''})
        self.square_info.append({'x': 250,'y': -110, 'point': '', 'direction': ''})
    def change_direction(self):
        if self.square_type == 1:
            if self.square_info[0]['direction'] == 1:
                self.square_info[0]['direction'] = 2
                self.square_info[0]['x'] += 40
                self.square_info[3]['x'] -= 40
                self.square_info[3]['y'] -= 80
            elif self.square_info[0]['direction'] == 2:
                self.square_info[0]['direction'] = 3
                self.square_info[1]['y'] -= 40
                self.square_info[3]['x'] -= 80
                self.square_info[3]['y'] += 40
            elif self.square_info[0]['direction'] == 3:
                self.square_info[0]['direction'] = 4
                self.square_info[0]['x'] -= 40
                self.square_info[0]['y'] -= 40
                self.square_info[2]['y'] -= 80
                self.square_info[3]['x'] += 40
                self.square_info[3]['y'] += 40
            elif self.square_info[0]['direction'] == 4:
                self.square_info[0]['direction'] = 1
                self.square_info[0]['y'] += 40
                self.square_info[1]['y'] += 40
                self.square_info[2]['y'] += 80
                self.square_info[3]['x'] += 80
        elif self.square_type == 2:
            if self.square_info[0]['direction'] == 1:
                self.square_info[0]['direction'] = 2
                self.square_info[1]['x'] -= 40
                self.square_info[1]['y'] -= 40
                self.square_info[2]['x'] -= 80
                self.square_info[2]['y'] -= 80
                self.square_info[3]['x'] -= 120
                self.square_info[3]['y'] -= 120
            elif self.square_info[0]['direction'] == 2:
                self.square_info[0]['direction'] = 1
                self.square_info[1]['x'] += 40
                self.square_info[1]['y'] += 40
                self.square_info[2]['x'] += 80
                self.square_info[2]['y'] += 80
                self.square_info[3]['x'] += 120
                self.square_info[3]['y'] += 120
        elif self.square_type == 3:
            if self.square_info[0]['direction'] == 1:
                self.square_info[0]['direction'] = 2
                self.square_info[0]['x'] += 80
                self.square_info[0]['y'] -= 40
                self.square_info[3]['y'] -= 40
            elif self.square_info[0]['direction'] == 2:
                self.square_info[0]['direction'] = 1
                self.square_info[0]['x'] -= 80
                self.square_info[0]['y'] += 40
                self.square_info[3]['y'] += 40
        elif self.square_type == 4:
            if self.square_info[0]['direction'] == 1:
                self.square_info[0]['direction'] = 2
                self.square_info[1]['x'] += 80
                self.square_info[1]['y'] -= 80
                self.square_info[2]['x'] += 40
                self.square_info[2]['y'] -= 40
            elif self.square_info[0]['direction'] == 2:
                self.square_info[0]['direction'] = 3
                self.square_info[1]['x'] -= 80
                self.square_info[1]['y'] += 40
                self.square_info[3]['x'] -= 40
            elif self.square_info[0]['direction'] == 3:
                self.square_info[0]['direction'] = 4
                self.square_info[1]['x'] += 40
                self.square_info[1]['y'] -= 40
            elif self.square_info[0]['direction'] == 4:
                self.square_info[0]['direction'] = 1
                self.square_info[1]['x'] -= 40
                self.square_info[1]['y'] += 80
                self.square_info[2]['x'] -= 40
                self.square_info[2]['y'] += 40
                self.square_info[3]['x'] += 40
        elif self.square_type == 5:
            if self.square_info[0]['direction'] == 1:
                self.square_info[0]['direction'] = 2
                self.square_info[1]['x'] += 80
                self.square_info[1]['y'] -= 80
                self.square_info[2]['y'] -= 80
            elif self.square_info[0]['direction'] == 2:
                self.square_info[0]['direction'] = 3
                self.square_info[1]['x'] -= 80
                self.square_info[1]['y'] += 40
                self.square_info[2]['y'] += 40
                self.square_info[3]['x'] -= 80
            elif self.square_info[0]['direction'] == 3:
                self.square_info[0]['direction'] = 4
                self.square_info[0]['x'] -= 80
                self.square_info[0]['y'] -= 40
                self.square_info[2]['y'] += 40
            elif self.square_info[0]['direction'] == 4:
                self.square_info[0]['direction'] = 1
                self.square_info[0]['x'] += 80
                self.square_info[0]['y'] += 40
                self.square_info[1]['y'] += 40
                self.square_info[3]['x'] += 80
        elif self.square_type == 6:
            if self.square_info[0]['direction'] == 1:
                self.square_info[0]['direction'] = 2
                self.square_info[1]['x'] += 40
                self.square_info[1]['y'] -= 80
                self.square_info[2]['x'] += 40
            elif self.square_info[0]['direction'] == 2:
                self.square_info[0]['direction'] = 1
                self.square_info[1]['x'] -= 40
                self.square_info[1]['y'] += 80
                self.square_info[2]['x'] -= 40


game_window = tk.Tk()
game_window.wm_title(" 魔术方块 ")
game_window.geometry("{}x{}".format(WINDOW_X_SIZE, WINDOW_Y_SIZE))
game_window.resizable(0, 0) 
game = Game_manager(game_window)
game_window.bind('<Key>', game.control_square)
game_window.mainloop()
