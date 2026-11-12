# -*- coding: utf-8 -*-
# 第 1 课 · 自主改造（步骤 4）：彩虹五角星
# 给五角星的每条边换一种颜色——用列表装颜色，循环里挨个取。

import turtle

print("嘀——码力启动！")

t = turtle.Turtle()
t.shape("turtle")
t.speed(3)
t.pensize(5)

colors = ["gold", "orange", "tomato", "orchid", "deep sky blue"]

for i in range(5):
    t.pencolor(colors[i])    # 第 i 次循环取第 i 个颜色（i = 0,1,2,3,4）
    t.forward(220)
    t.right(144)

# 🔍 小实验：
#    1. 往 colors 里加几个颜色试试（多余的颜色不会被用到）
#    2. 把 t.speed(3) 改成 t.speed(0)，看看"极速模式"
#    3. 进阶：在循环前加 t.begin_fill()、循环后加 t.end_fill()，
#       再加一行 t.fillcolor("gold")——五角星变成实心的！

turtle.done()
