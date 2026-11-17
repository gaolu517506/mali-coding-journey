# -*- coding: utf-8 -*-
# 第 2 课 · 别撞墙（步骤 3）：边界检查
# 按住左键不放——飞船飞出屏幕消失了！太空也有护栏：
# 每帧检查位置，超出边界就把它"按回来"。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的飞船 · 护栏")
clock = pygame.time.Clock()

W, H = 800, 600                   # 窗口宽高起个名字，以后改窗口只改这里
ship = pygame.Rect(350, 540, 100, 18)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 算：听键盘移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.x -= 6
    if keys[pygame.K_RIGHT]:
        ship.x += 6

    # 算：边界护栏——身份证的左边不能小于 0，右边不能超过窗口宽
    if ship.x < 0:
        ship.x = 0                          # 左护栏：贴住左边
    if ship.x > W - ship.width:
        ship.x = W - ship.width             # 右护栏：贴住右边（要减掉船自己的宽度！）

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.rect(screen, (0, 200, 255), ship)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把右护栏那行改成 ship.x > W（不减宽度）——飞船右边一小截卡在屏幕外
#    2. 注释掉两个护栏再按住左键：飞船走丢，再也回不来
#    3. 思考：为什么右护栏是 W - ship.width，左护栏却不用加什么？
#       （提示：身份证上的 x 记的是"左上角"的位置）
