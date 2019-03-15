import tkinter as tk
from tkinter import messagebox
import time
import random

class Game_manager:
    # 定义基本属性
    b_play = None
    l_title = None
    snake = None
    win = None
    food = None
    is_change = None
    l_score = None
    score = None
    # 定义构造方法
    def __init__(self, win):
        self.win = win
        # 初始化开始按钮
        self.b_play = tk.Button(self.win, text="开始游戏", font=('宋体', 12), width=10, height=3, command=self.play_game)
        self.b_play.focus_set()  # 让按钮获得焦点
        self.b_play.bind('<Return>', func=self.play_game)
        self.b_play.place(x=200, y=300, anchor='nw')
        # 初始化标题标签
        self.l_title = tk.Label(self.win, text="贪食蛇", bg='pink', font=('宋体', 18), width=25, height=3)
        self.l_title.place(x=100, y=100, anchor='nw')
        self.is_change = False
    # 开始游戏
    def play_game(self, event=None):
        self.b_play.destroy()
        self.l_title.destroy()
        # 初始化分数 
        self.l_score = tk.Label(self.win, text="分数:0", bg='pink', font=('宋体', 14), width=10, height=3)
        self.l_score.place(x=100, y=200, anchor='nw')
        self.score = 0
        canvas = self.draw_bg()  # 画背景
        try:
            # 循环整个游戏
            while True:
                self.update_snake(canvas)  # 更新蛇位置
                self.snake = Snake()
                canvas.delete(self.food.food_info['point']) # 清除被吃食物
                # 初始化分数
                self.score = 0
                self.l_score.config(text='分数:{}'.format(self.score))
                # 刷新食物
                self.food = Food(self.snake.snake_info)
                self.draw_food(canvas)
        except:
            print('...')
    # 画游戏背景
    def draw_bg(self):
        canvas = tk.Canvas(self.win, width=520, height=520, bg='pink')
        canvas.pack()
        # 画格子,一共20个格子
        for x in range(26):
            canvas.create_line(10, x * 20 + 10, 510, x * 20 + 10)  # 横线26条
            canvas.create_line(x * 20 + 10, 10, x * 20 + 10, 510)  # 竖线26条
        self.snake = Snake()
        self.food = Food(self.snake.snake_info)
        self.draw_food(canvas)
        return canvas
    # 画食物
    def draw_food(self, canvas):
        self.food.food_info['point'] = canvas.create_oval(self.food.food_info['x'], self.food.food_info['y'], self.food.food_info['x'] + 20, self.food.food_info['y'] + 20, fill='red')
    # 更新蛇位置
    def update_snake(self, canvas):
        while self.snake.health:
            if self.snake.snake_info[0]['move_direction'] == 'right':
                if self.snake.snake_info[0]['move_direction'] == 'right':
                    temp = list(reversed(self.snake.snake_info))
                    i = 0
                    for point in temp:
                        if temp[temp.index(point)] == temp[-1]:
                            point['x'] += 20 
                        else:
                            point['x'] = temp[i + 1]['x']
                            point['y'] = temp[i + 1]['y']
                        i += 1
            elif self.snake.snake_info[0]['move_direction'] == 'down':
                if self.snake.snake_info[0]['move_direction'] == 'down':
                    temp = list(reversed(self.snake.snake_info))
                    i = 0
                    for point in temp:
                        if temp[temp.index(point)] == temp[-1]:
                            point['y'] = point['y'] + 20 
                        else:
                            point['x'] = temp[i + 1]['x']
                            point['y'] = temp[i + 1]['y']
                        i += 1
            elif self.snake.snake_info[0]['move_direction'] == 'left':
                if self.snake.snake_info[0]['move_direction'] == 'left':
                    temp = list(reversed(self.snake.snake_info))
                    i = 0
                    for point in temp:
                        if temp[temp.index(point)] == temp[-1]:
                            point['x'] = point['x'] - 20 
                        else:
                            point['x'] = temp[i + 1]['x']
                            point['y'] = temp[i + 1]['y']
                        i += 1
            elif self.snake.snake_info[0]['move_direction'] == 'up':
                if self.snake.snake_info[0]['move_direction'] == 'up':
                    temp = list(reversed(self.snake.snake_info))
                    i = 0
                    for point in temp:
                        if temp[temp.index(point)] == temp[-1]:
                            point['y'] = point['y'] - 20 
                        else:
                            point['x'] = temp[i + 1]['x']
                            point['y'] = temp[i + 1]['y']
                        i += 1
            self.is_change = True           
            self.draw_snake(canvas)
            self.win.update() 
            self.snake_eating(canvas)
            self.win.update() 
            self.snake_health() 
            time.sleep(0.1) 
            self.clear_snake(canvas)
            self.win.update()
    # 画蛇
    def draw_snake(self, canvas):
        for point in self.snake.snake_info:
            if self.snake.snake_info.index(point) == 0:
                point['point'] = canvas.create_rectangle(point['x'], point['y'], point['x'] + 20, point['y'] + 20, fill='Lightgreen')  # RGB 
            else:
                point['point'] = canvas.create_rectangle(point['x'], point['y'], point['x'] + 20, point['y'] + 20, fill='green')
    # 清理蛇
    def clear_snake(self, canvas):
        for point in self.snake.snake_info:
            canvas.delete(point['point'])
    # 控制蛇
    def control_snake(self, key):
        if not self.is_change:
            return
        elif key.keycode == 39 and self.snake.snake_info[0]['move_direction'] != 'left':
            self.snake.snake_info[0]['move_direction'] = 'right'
            self.is_change = False
        elif key.keycode == 40 and self.snake.snake_info[0]['move_direction'] != 'up':
            self.snake.snake_info[0]['move_direction'] = 'down'
            self.is_change = False
        elif key.keycode == 37 and self.snake.snake_info[0]['move_direction'] != 'right':
            self.snake.snake_info[0]['move_direction'] = 'left'
            self.is_change = False
        elif key.keycode == 38 and self.snake.snake_info[0]['move_direction'] != 'down':
            self.snake.snake_info[0]['move_direction'] = 'up'
            self.is_change = False
    # 判定蛇吃东西
    def snake_eating(self, canvas):
        if self.snake.snake_info[0]['x'] == self.food.food_info['x'] and self.snake.snake_info[0]['y'] == self.food.food_info['y']:
            canvas.delete(self.food.food_info['point']) # 清除被吃食物
            self.score += 1
            self.l_score.config(text='分数:{}'.format(self.score))
            self.food.creat_food()
            self.draw_food(canvas)
            self.snake.snake_info.append({'x': self.snake.snake_info[-1]['x'], 'y': self.snake.snake_info[-1]['y'], 'point': ''})
    # 判定蛇死亡
    def snake_health(self):
        if self.snake.snake_info[0]['x'] >= 510 or self.snake.snake_info[0]['y'] >= 510 or self.snake.snake_info[0]['x'] < 10 or self.snake.snake_info[0]['y'] < 10:
            self.snake.health = False
            if messagebox.askokcancel("是否继续游戏", "当前游戏结束\n是否重新开始？"):
                pass
            else:
                self.win.destroy()
            return
        for point in self.snake.snake_info[1:]:
            if self.snake.snake_info[0]['x'] == point['x'] and self.snake.snake_info[0]['y'] == point['y']:
                self.snake.health = False
                if messagebox.askokcancel("是否继续游戏", "当前游戏结束\n是否重新开始？"):
                    pass
                else:
                    self.win.destroy()
                return


class Snake:
    snake_info = None
    health = None
    # 定义构造方法
    def __init__(self):
        self.snake_info = []
        self.health = True
        self.ini_snake()

    # 蛇起始位置(蛇信息初始化)
    def ini_snake(self):
        self.snake_info.append({'x': 130, 'y': 90, 'point': '', 'move_direction': 'right'})  # 蛇头坐标
        self.snake_info.append({'x': 110, 'y': 90, 'point': ''})  # 蛇身坐标
        self.snake_info.append({'x': 90, 'y': 90, 'point': ''})  # 蛇身坐标


class Food:
    food_info = None
    snake_info = None
    def __init__(self, snake_info):
        self.food_info = {'x': 0, 'y': 0, 'point': ''}
        self.snake_info = snake_info
        self.creat_food()
    # 随机生成食物
    def creat_food(self):
        while True:
            creat_point_x = random.choice(range(10, 510, 20))
            creat_point_y = random.choice(range(10, 510, 20))
            for point in self.snake_info:
                if point['x'] == creat_point_x and point['y'] == creat_point_y:
                    break
            else:
                self.food_info['x'] = creat_point_x
                self.food_info['y'] = creat_point_y
                break
        

def callback():
    if messagebox.askokcancel("Quit", "确定退出当前游戏吗？"):
        win.destroy()


win = tk.Tk()
win.wm_title("贪食蛇")  # 窗口标题
win.geometry("1000x600")  # 窗口大小
win.resizable(0, 0)  # 阻止Python GUI的大小调整
game = Game_manager(win)
win.bind('<Key>', game.control_snake)
win.protocol("WM_DELETE_WINDOW", callback)
win.mainloop()

