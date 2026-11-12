# -*- coding: utf-8 -*-
# 第 1 课 · 发现重复（步骤 2）：for 循环画正方形
# 上一课写 4 遍 forward + right，手都酸了。
# 把重复的动作交给复读机——for 循环！

import turtle

print("嘀——码力启动！")

t = turtle.Turtle()
t.shape("turtle")
t.pensize(3)             # 笔画粗一点，航线更清楚

for i in range(4):       # 复读 4 遍（range(4) = 0,1,2,3 共 4 次）
    t.forward(150)       # ↑ 注意这两行开头有空格缩进：
    t.right(90)          #   缩进表示"这两行在循环体内"

# 🔍 小实验：把 range(4) 改成 range(3) 试试？改成 range(6) 呢？
#    你会发现：边数 = 次数，每次转的角度 = 360 ÷ 边数。
#    三角形转 120，六边形转 60……这是几何给程序员的礼物。

turtle.done()
