# -*- coding: utf-8 -*-
# 第 2 课 · 飞船日志（步骤 4）：事件驱动
# 持续移动用 get_pressed（每帧点名），那"按一下就做一次"的事呢？
# 用 KEYDOWN 事件——它像门铃，只在按键"按下那一瞬间"响一声。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的飞船 · 日志")
clock = pygame.time.Clock()

ship = pygame.Rect(350, 540, 100, 18)
SHIP_COLORS = [(0, 200, 255), (255, 215, 0), (255, 80, 120), (120, 255, 140)]
color_index = 0                   # 当前涂装编号

running = True
while running:
    # 听：事件队列——pygame 把发生的事一件件排好队等你处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:               # 有个键"刚刚按下"
            if event.key == pygame.K_SPACE:            # 是空格
                color_index += 1                       # 换下一套涂装
                if color_index >= len(SHIP_COLORS):    # 编号超出了名单
                    color_index = 0                    # 回到第一套
            if event.key == pygame.K_ESCAPE:           # ESC：紧急脱离
                running = False

    # 算：持续移动还是交给每帧点名
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.x -= 6
    if keys[pygame.K_RIGHT]:
        ship.x += 6
    if ship.x < 0:
        ship.x = 0
    if ship.x > 800 - ship.width:
        ship.x = 800 - ship.width

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.rect(screen, SHIP_COLORS[color_index], ship)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 往 SHIP_COLORS 里加你调的 RGB 色，空格多按几下轮到它
#    2. 加一个 KEYDOWN：按回车打印一条飞行日志到终端 print("坐标:", ship.x)
#    3. 关键对比：把"换涂装"搬进 get_pressed 的 if 里会怎样？
#       每帧都 +1，每秒 60 次——涂装闪成走马灯！
#       结论：持续动作用点名（get_pressed），一次性的动作用门铃（KEYDOWN）
