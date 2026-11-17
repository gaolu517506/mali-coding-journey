# -*- coding: utf-8 -*-
# 第 3 课 · 毕业作品（步骤 4）：《码力的星空》
# 三课总动员：循环（第 1 课）+ 坐标与随机（第 2 课）+ 函数（第 3 课）。
# 工厂把积木造好，主程序只剩"指挥"——这就是程序员的日常。

import turtle
import random

print("嘀——码力启动！")

screen = turtle.Screen()
screen.bgcolor("midnight blue")
screen.title("码力的星空 · 航线解锁")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# ── 工厂区：先造两块积木 ──────────────────────────────

def draw_star(size, color):
    # 画一颗五角星（在当前位置，大小 size、颜色 color）
    t.pencolor(color)
    for i in range(5):
        t.forward(size)
        t.right(144)

def draw_starfield(n):
    # 随机撒 n 颗小星点当背景
    for i in range(n):
        t.penup()
        t.goto(random.randint(-350, 350), random.randint(-250, 250))
        t.dot(random.randint(2, 5), "white")

# ── 主程序：指挥积木干活 ──────────────────────────────

draw_starfield(80)       # 1. 铺背景星野

beidou = [               # 2. 北斗七星坐标表（第 2 课的数据）
    [170, 60], [110, -10], [20, 0], [-20, 70],
    [-10, 140], [-80, 180], [-160, 220],
]
t.pencolor("deep sky blue")
t.pensize(2)
t.penup()
t.goto(170, 60)          # 空降到天枢
t.pendown()
for x, y in beidou:
    t.goto(x, y)         # 连出北斗

for x, y in beidou:      # 3. 北斗七星各亮一颗小金星
    t.penup()
    t.goto(x, y)
    t.pendown()
    draw_star(35, "gold")

t.penup()                # 4. 夜空下方：一颗航线纪念星
t.goto(0, -60)
t.pendown()
draw_star(90, "gold")

t.penup()                # 5. 签上码力的名字
t.goto(0, -170)
t.pencolor("white")
t.write("航线解锁 ✓ 下一站：太空轨道", align="center", font=("Arial", 14, "bold"))

# 🔍 小实验：
#    1. 主程序只有二十来行——数数看，不用函数的话这些代码要写多少行？
#    2. 改 draw_starfield(80) 的数字，夜空的密度你说了算
#    3. 毕业彩蛋：运行成功后截个图——这是你 Python 第一站的成绩单

turtle.done()            # 让星空窗口保持打开
