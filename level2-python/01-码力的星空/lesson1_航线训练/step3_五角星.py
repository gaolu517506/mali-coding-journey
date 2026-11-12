# -*- coding: utf-8 -*-
# 第 1 课 · 大招（步骤 3）：五角星
# 正方形之后，码力的第一个真正的任务：在星图上点亮一颗五角星。
# 秘密只有两个数字：5 条边，每次右转 144 度。

import turtle

print("嘀——码力启动！")

t = turtle.Turtle()
t.shape("turtle")
t.pensize(3)
t.pencolor("gold")       # 金色的航线

for i in range(5):       # 5 条边
    t.forward(200)
    t.right(144)         # 144 = 180 - 36：五角星每个尖角是 36 度

# 🔍 数字的秘密：
#    画正方形时海龟转了一整圈（4 × 90 = 360）；
#    画五角星时海龟转了整整两圈（5 × 144 = 720）！
#    星星比正方形多绕了一圈——这就是它更像星星的原因。

turtle.done()
