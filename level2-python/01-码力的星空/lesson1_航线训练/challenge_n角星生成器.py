# -*- coding: utf-8 -*-
# 第 1 课 · 挑战任务：任意 n 角星生成器
# 问一遍要几角星，就画几角星——把"复读机"变成"可编程的复读机"。

import turtle

print("嘀——码力启动！")

n = int(input("要画几角星？（建议 5 以上）："))
size = int(input("要多大？（建议 100~300）："))

t = turtle.Turtle()
t.shape("turtle")
t.speed(0)               # 极速模式
t.pensize(3)
t.pencolor("gold")

angle = 720 / n          # 五角星的秘密推广：n 角星每步转 720 ÷ n

for i in range(n):
    t.forward(size)
    t.right(angle)

# 🔍 数学彩蛋（试出来的）：
#    5 角星 = 五角星 ✓
#    6 角星 → 画出了两个三角形？！
#    因为 720 ÷ 6 = 120，恰好是三角形的转角——
#    连笔的 n 角星只有 n 是奇数时才成立，偶数会拆成好几颗星。
#    发现这个规律的同学，你已经站在数学和编程的交界线上了。

turtle.done()
