# -*- coding: utf-8 -*-
# 第 1 课 · 第一颗星（步骤 2）：在舷窗上画画
# 舷窗亮了，但外面空空的。先在窗外的星空中点一颗星——
# 游戏画面就是"每帧重新刷背景 + 重新画所有东西"画出来的。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的舷窗 · 星空")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画：先刷深夜底色（把上一帧的旧画全部盖掉）
    screen.fill((8, 8, 35))

    # 再画一颗白星：circle(画在哪, 什么颜色, 圆心 (x, y), 半径)
    pygame.draw.circle(screen, (255, 255, 255), (400, 300), 6)
    # 再来一颗金星和一颗蓝星——多画几行就多几颗
    pygame.draw.circle(screen, (255, 215, 0), (200, 150), 9)
    pygame.draw.circle(screen, (80, 180, 255), (600, 420), 5)

    pygame.display.flip()

pygame.quit()

# 🔍 小实验：
#    1. 再加三行 circle，亲手摆一个你喜欢的星图（记得选不同的圆心和颜色）
#    2. 颜色 DIY：RGB 每个数都是 0~255 的旋钮——(255, 0, 255) 是什么色？试出来
#    3. 半径改大改小，星星就有远有近
