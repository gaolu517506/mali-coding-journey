# -*- coding: utf-8 -*-
# 第 1 课 · 训练舱手动飞行（步骤 1）
# 海龟 = 码力的飞行训练舱。我们先用"一条一条下指令"的方式驾驶它。

import turtle            # 借来飞控系统（turtle 模块）

print("嘀——码力启动！")   # 仪式感开场：让终端先响一声

t = turtle.Turtle()      # 造出一架训练舱，给它起名叫 t
t.shape("turtle")        # 让它长成海龟的样子
t.speed(3)               # 飞行速度（1 慢 → 3 正常 → 0 最快）

# 手动飞行：先飞出一个 L 形
t.forward(100)           # 前进 100（forward = 向前飞）
t.right(90)              # 右转 90 度（right = 顺时针转）
t.forward(100)
t.right(90)

# ✏️ 补全任务：再加 4 行，把正方形画完。
# 写到手酸的时候你就明白了——下一课的 for 循环就是为这一刻发明的。

turtle.done()            # 让星空窗口保持打开
