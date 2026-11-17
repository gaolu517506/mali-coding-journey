# -*- coding: utf-8 -*-
# 第 3 课 · 积木流水线（步骤 3）：函数 + 循环 + 随机
# 三课的手艺合体：第 1 课的循环、第 2 课的 goto 和 random、今天的函数——
# 流水线开工：随机位置、随机大小、随机颜色，铺 25 颗星。

import turtle
import random

print("嘀——码力启动！")

screen = turtle.Screen()
screen.bgcolor("midnight blue")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

colors = ["gold", "white", "orchid", "deep sky blue", "tomato", "orange"]

# 积木：带两个旋钮的画星器（步骤 2 的成品）
def draw_star(size, color):
    t.pencolor(color)
    for i in range(5):
        t.forward(size)
        t.right(144)

# 流水线：25 次"随机选位 + 按一下积木"
for i in range(25):
    x = random.randint(-330, 330)
    y = random.randint(-230, 230)
    size = random.randint(20, 70)
    c = colors[random.randint(0, 5)]   # 从颜色表里随机抽一个（下标 0~5）

    t.penup()
    t.goto(x, y)
    t.pendown()
    draw_star(size, c)                 # 按积木——一颗星落地

# 🔍 小实验：
#    1. 星星太大容易"撞车"——把 size 的范围改成 10~40 试试
#    2. 把 25 改成 60（放心，电脑不累，真的）
#    3. 想一想：如果没有 def，这个循环体里要塞进几行画星代码？还能一眼看懂吗？

turtle.done()            # 让星空窗口保持打开
