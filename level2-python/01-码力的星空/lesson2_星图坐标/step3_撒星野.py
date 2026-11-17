# -*- coding: utf-8 -*-
# 第 2 课 · 撒一片星野（步骤 3）：random 随机数
# 北斗只有七颗，真正的夜空有几千颗。
# 一颗一颗写坐标要写到明天早上——让 random 帮我们"随机撒"。

import turtle
import random            # 新工具箱：随机数发生器（骰子大师）

print("嘀——码力启动！")

screen = turtle.Screen()
screen.bgcolor("midnight blue")   # 先把画布刷成深夜蓝——夜空到位

t = turtle.Turtle()
t.speed(0)
t.hideturtle()          # 隐身术：撒星星的时候海龟先藏起来

# 撒 60 颗星：每颗的位置和大小，都由 random.randint 现场掷骰子决定
for i in range(60):
    x = random.randint(-350, 350)    # x 坐标：在 -350 到 350 之间掷一个
    y = random.randint(-250, 250)    # y 坐标：再掷一个
    size = random.randint(2, 7)      # 星星大小也掷一个——有大有小才像真的夜空

    t.penup()            # 起飞（不留痕地移动）
    t.goto(x, y)         # 空降到随机位置
    t.dot(size, "white") # dot = 盖一个圆点印章，一颗星星落地

# 🔍 小实验：
#    1. 把 60 改成 200，星空会密集到什么程度？
#    2. 把 dot 的颜色换成 "gold"，变成一片金色星野
#    3. 进阶：再撒一层"大星星"（size 掷 8~15），夜空立刻有了远近层次

turtle.done()            # 让星空窗口保持打开
