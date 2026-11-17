# -*- coding: utf-8 -*-
# 第 3 课 · 打包第一块积木（步骤 1）：def 定义函数
# 上一课的痛点：画一颗星 = 5 行代码，换个地方画就要再抄一遍。
# Scratch 里你会怎么办？——自制积木！Python 里它叫 def。

import turtle

print("嘀——码力启动！")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.pensize(2)

# 🏭 打包：def 是"定义"的意思——下面这块新积木的名字叫 draw_star
# 注意：def 里面的代码不会立刻执行，它只是被装进积木盒子，等被"调用"才工作
def draw_star():
    for i in range(5):
        t.forward(50)
        t.right(144)

# 🧱 使用：现在"画一颗星"浓缩成一行。想画三颗？到不同位置各喊一次它的名字
t.pencolor("gold")
t.penup()
t.goto(-220, 0)
t.pendown()
draw_star()              # 第一颗

t.pencolor("orchid")
t.penup()
t.goto(0, 60)
t.pendown()
draw_star()              # 第二颗

t.pencolor("deep sky blue")
t.penup()
t.goto(180, -40)
t.pendown()
draw_star()              # 第三颗

# 🔍 小实验：
#    1. 数一数：不用 def，画这三颗星要写几行画星代码？用了 def 呢？
#    2. 把 def 里的 forward(50) 改成 forward(90)——三颗星一起变大！
#       这就是积木的威力：改一处，处处生效
#    3. 把三行 draw_star() 都删掉再运行——屏幕上什么都没有。
#       记住：定义积木 ≠ 使用积木

turtle.done()            # 让星空窗口保持打开
