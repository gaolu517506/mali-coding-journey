# -*- coding: utf-8 -*-
# 第 1 课 · 点亮舷窗（步骤 1）：最小的 pygame 程序
# 轨道实战第一步：给码力的飞船造一扇舷窗（游戏窗口），
# 并让它保持"活着"——这就是游戏主循环的雏形。

import pygame

print("嘀——码力启动！")

pygame.init()                                   # 点火：启动 pygame 引擎
screen = pygame.display.set_mode((800, 600))    # 造一扇 800×600 的舷窗
pygame.display.set_caption("码力的舷窗")         # 窗口标题

running = True                                  # 心脏跳动的开关
while running:                                  # ── 游戏主循环：心脏开始跳 ──
    # 1. 听：这一帧发生了什么事（点按钮、按键盘都叫"事件"）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # 玩家点了窗口的红色关闭钮
            running = False                     # 心脏停跳，游戏结束

    # 2. 画：先把整扇窗刷成深夜色，再翻给玩家看
    screen.fill((8, 8, 35))                     # (红, 绿, 蓝) 三个 0~255 的数调出颜色
    pygame.display.flip()                       # 把画好的这一帧"翻"到屏幕上

pygame.quit()                                   # 熄火：退出前打扫干净

# 🔍 小实验：
#    1. 把 fill 里的三个数换成 (200, 30, 30)——舷窗变成警报红！
#       再试试 (255, 215, 0)？对，这就是星空站用过的金色，RGB 通吃
#    2. 把窗口尺寸改成 (1000, 700)，标题改成你给它起的名字
#    3. 思考：为什么画面要放在 while 循环里"反复画"，
#       而不是画一次就结束？（步骤 3 揭晓）
