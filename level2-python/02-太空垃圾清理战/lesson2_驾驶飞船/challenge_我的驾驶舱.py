# -*- coding: utf-8 -*-
# 第 2 课 · 挑战任务：我的驾驶舱
# 驾驶舱升级：四方向飞行 + 全屏护栏 + 三角形飞船（polygon）+ 空格换涂装。
# 综合运用本课全部手艺。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的飞船 · 我的驾驶舱")
clock = pygame.time.Clock()

W, H = 800, 600
ship_x, ship_y = 350, 480                 # 飞船左上角位置
SHIP_W, SHIP_H = 100, 40                  # 飞船大小
COLORS = [(0, 200, 255), (255, 215, 0), (255, 80, 120)]
color_index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                color_index = (color_index + 1) % len(COLORS)   # 取余轮换
            if event.key == pygame.K_ESCAPE:
                running = False

    # 算：四方向飞行
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_x -= 6
    if keys[pygame.K_RIGHT]:
        ship_x += 6
    if keys[pygame.K_UP]:
        ship_y -= 6
    if keys[pygame.K_DOWN]:
        ship_y += 6

    # 算：四面护栏
    if ship_x < 0:
        ship_x = 0
    if ship_x > W - SHIP_W:
        ship_x = W - SHIP_W
    if ship_y < 0:
        ship_y = 0
    if ship_y > H - SHIP_H:
        ship_y = H - SHIP_H

    # 画：三角形飞船——polygon(画布, 颜色, [顶点1, 顶点2, 顶点3])
    screen.fill((8, 8, 35))
    tip = (ship_x + SHIP_W // 2, ship_y)              # 机头（上中）
    left = (ship_x, ship_y + SHIP_H)                  # 左后
    right = (ship_x + SHIP_W, ship_y + SHIP_H)        # 右后
    pygame.draw.polygon(screen, COLORS[color_index], [tip, left, right])
    # 驾驶舱小圆叠在机身中间
    pygame.draw.circle(screen, (255, 255, 255), (ship_x + SHIP_W // 2, ship_y + SHIP_H // 2), 7)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. % 取余轮换：color_index = (color_index + 1) % 3——想想它怎么代替
#       "超出名单就归零"的两行 if（第 4 课硬垃圾还会用到 %）
#    2. 机身加宽 SHIP_W 改 140、机头更尖（把 tip 的 x 改到正中再收窄）
#    3. 预告：下一课飞船要发射能量球——想想球应该从哪个顶点出发？
