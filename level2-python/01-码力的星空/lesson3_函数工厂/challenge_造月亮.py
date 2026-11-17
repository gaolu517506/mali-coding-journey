# -*- coding: utf-8 -*-
# 第 3 课 · 挑战任务：造月亮
# 函数工厂不只会造星星。造一个月亮需要"两圆相减"的小聪明：
# 先画一轮满月，再用"夜空颜色"画一个偏移的圆把它啃掉一块——月牙就出来了。

import turtle
import random

print("嘀——码力启动！")

screen = turtle.Screen()
screen.bgcolor("midnight blue")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# 积木一：画星器（本课主角）
def draw_star(size, color):
    t.pencolor(color)
    for i in range(5):
        t.forward(size)
        t.right(144)

# 积木二：造月亮——在 (x, y) 造一个大小为 r 的月牙
def draw_moon(x, y, r):
    t.penup()
    t.goto(x, y - r)              # circle 的规矩：从圆的正下方起笔
    t.pendown()
    t.pencolor("light yellow")
    t.fillcolor("light yellow")
    t.begin_fill()
    t.circle(r)                   # 先画一轮满月（circle = 画圆的新积木）
    t.end_fill()

    t.penup()
    t.goto(x + r * 0.3, y + r * 0.1 - r * 0.85)   # 偏移到满月的右上方
    t.pendown()
    t.pencolor("midnight blue")   # 拿"夜空的颜色"当画笔
    t.fillcolor("midnight blue")
    t.begin_fill()
    t.circle(r * 0.85)            # 用夜空色的圆啃掉一块 → 月牙！
    t.end_fill()

# 主程序：星野 + 装饰星 + 月亮
for i in range(60):
    t.penup()
    t.goto(random.randint(-350, 350), random.randint(-250, 250))
    t.dot(random.randint(2, 5), "white")

t.penup()
t.goto(-200, 120)
t.pendown()
draw_star(60, "gold")

t.penup()
t.goto(-40, -140)
t.pendown()
draw_star(45, "orchid")

draw_moon(140, 130, 60)           # 月亮挂到右上角

# 🔍 小实验：
#    1. 再造一个：加一行 draw_moon(-220, -160, 35)——工厂积木随便复用
#    2. 造流星：penup 到高空 → pencolor 白 → pendown → goto 到低处（一条斜线），
#       线尾再 dot 一个亮点——然后把它也打包成 draw_shooting_star() 吧
#    3. 月牙的朝向：改遮盖圆偏移里的 0.3（比如改成 -0.3），月牙会朝另一边弯

turtle.done()            # 让星空窗口保持打开
