# -*- coding: utf-8 -*-
# 第 2 课 · 挑战任务：我的星座
# 北斗是古人的星座，现在轮到你——用 5~8 个坐标，
# 在星野上连出属于你自己的星座，并给它命名。

import turtle
import random

print("嘀——码力启动！")

screen = turtle.Screen()
screen.bgcolor("midnight blue")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# 第一步：先撒一层星野当背景（步骤 3 的手艺）
for i in range(80):
    x = random.randint(-350, 350)
    y = random.randint(-250, 250)
    t.penup()
    t.goto(x, y)
    t.dot(random.randint(2, 5), "white")

# 第二步：连出我的星座
# 示例连了一个"小箭头"——把它改成你想要的形状（爱心？飞机？名字首字母？）
# 坐标规则：右为正 x、上为正 y；改这几个数字，形状就跟着变
my_stars = [
    [140, -80],
    [40, -20],
    [-60, 40],
    [-160, 100],
    [40, 100],
    [40, -120],
]

t.penup()
t.goto(140, -80)         # 空降到第一颗星（数字和 my_stars 第一行相同）
t.pendown()
t.pencolor("gold")
t.pensize(3)

for x, y in my_stars:
    t.goto(x, y)

# 第三步：给我的星座命名（write = 让海龟在星图上写字的新积木）
t.penup()
t.goto(0, -180)
t.pencolor("white")
t.write("码力座 · 由未来的天文学家命名", align="center", font=("Arial", 16, "bold"))

# 🔍 小实验：
#    1. 改 my_stars 里的坐标，连出你自己的形状（先在草稿纸上画草图，再标坐标）
#    2. 在每颗星的位置 dot 一个大金点，让星座更醒目
#    3. 你的连线回到起点了吗？想想步骤 2"勺子闭合"的实验

turtle.done()            # 让星空窗口保持打开
