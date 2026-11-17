# -*- coding: utf-8 -*-
# 第 2 课 · 飞船听令（步骤 2）：键盘控制
# 飞船造好了，但它还不会动。让键盘接管驾驶舱：
# 每帧问一次键盘"现在哪些键被按着？"——按左往左，按右往右。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的飞船 · 听令")
clock = pygame.time.Clock()

ship = pygame.Rect(350, 540, 100, 18)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 算：问键盘——现在哪些键被按着？（返回一整份按键状态表）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:        # 左方向键正被按着
        ship.x -= 6                # 飞船每帧左移 6（速度 = 每帧挪几步）
    if keys[pygame.K_RIGHT]:       # 右方向键正被按着
        ship.x += 6

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.circle(screen, (255, 255, 255), (150, 120), 3)
    pygame.draw.circle(screen, (255, 255, 255), (650, 300), 2)
    pygame.draw.rect(screen, (0, 200, 255), ship)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把 6 改成 12——灵敏度翻倍；改成 2——慢速巡航
#    2. 加上下移动：
#       if keys[pygame.K_UP]: ship.y -= 6
#       if keys[pygame.K_DOWN]: ship.y += 6
#    3. 同时按左右会怎样？左右抵消，飞船不动——因为两个 if 都成立
