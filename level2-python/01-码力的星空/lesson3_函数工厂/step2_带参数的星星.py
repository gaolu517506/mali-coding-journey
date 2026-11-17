# -*- coding: utf-8 -*-
# 第 3 课 · 给积木装旋钮（步骤 2）：函数的参数
# Scratch 自制积木可以加"输入"（数字、文字），Python 的函数也可以——
# 它们叫参数。draw_star(size, color)：size 旋钮控大小，color 旋钮控颜色。

import turtle

print("嘀——码力启动！")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.pensize(2)

# 打包：这次积木上装了两个旋钮——size 和 color
def draw_star(size, color):
    t.pencolor(color)    # 用旋钮 color 指定的颜色
    for i in range(5):
        t.forward(size)  # 每条边飞 size 那么长
        t.right(144)

# 使用：旋钮拧到不同档位，星星就不一样大、不一样色
t.penup()
t.goto(-220, 40)
t.pendown()
draw_star(40, "gold")            # 小金星

t.penup()
t.goto(-60, -60)
t.pendown()
draw_star(80, "orchid")          # 中号紫星

t.penup()
t.goto(120, 60)
t.pendown()
draw_star(120, "deep sky blue")  # 大蓝星

# 🔍 小实验：
#    1. 先想清楚 draw_star(120, "gold") 会画出什么，再运行验证你的预测
#    2. 造你的第三个旋钮：给 def 加参数 edge（边数），
#       循环改成 for i in range(edge) 和 t.right(720 / edge)——
#       n 角星积木诞生！第 1 课 challenge 的知识在这里合体
#    3. 思考：调用时把两个参数写反了 draw_star("gold", 40) 会怎样？试试看报什么错

turtle.done()            # 让星空窗口保持打开
