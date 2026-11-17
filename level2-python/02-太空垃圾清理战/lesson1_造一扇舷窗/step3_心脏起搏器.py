# -*- coding: utf-8 -*-
# 第 1 课 · 心脏起搏器（步骤 3）：帧率与动画
# 游戏为什么要把画面放在循环里反复画？因为动画 = 一帧一帧地画！
# clock 每秒敲 60 下，每敲一下画一帧——这就是"每一帧发生什么"。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的舷窗 · 心跳")

clock = pygame.time.Clock()      # 心脏起搏器：负责稳定的心跳
star_x = 0                       # 星星当前的 x 位置（从最左边出发）

running = True
while running:
    # 1. 听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. 算：星星这一帧往右挪 4 步（速度 = 每帧挪多少）
    star_x += 4
    if star_x > 800:             # 飞出右边界
        star_x = 0               # 从左边重新进场（永远飞不完的星）

    # 3. 画
    screen.fill((8, 8, 35))
    pygame.draw.circle(screen, (255, 215, 0), (star_x, 300), 10)
    pygame.display.flip()

    # 4. 等：每秒最多 60 帧——就像心跳，稳定才健康
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把 4 改成 12，星星飞快；改成 1，慢悠悠——"速度"就是每帧挪几步
#    2. 把 tick(60) 改成 tick(5)：整个游戏卡成幻灯片！60 是流畅的魔法数
#    3. 大发现：把 screen.fill 那行注释掉再运行——星星拖出一条长长的尾巴！
#       因为旧帧的画没被擦掉。这证明：每一帧都是"擦干净重画"画出来的
