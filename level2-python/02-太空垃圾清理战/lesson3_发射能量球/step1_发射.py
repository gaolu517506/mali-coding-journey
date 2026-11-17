# -*- coding: utf-8 -*-
# 第 3 课 · 发射（步骤 1）：能量球起飞
# 飞船能开了，但清垃圾需要武器——能量球。
# 运动的秘密只有一句话：速度 = 每帧挪多少，主循环每帧挪一点。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("能量球 · 起飞")
clock = pygame.time.Clock()

ship = pygame.Rect(350, 540, 100, 18)
# 能量球也是一张身份证（用 16×16 的方框包住一颗圆）
ball = pygame.Rect(392, 510, 16, 16)
ball_vy = -5                      # 竖直速度：负数 = 向上（y 轴向下为正！）

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 算：飞船左右开（上一课手艺）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.x -= 6
    if keys[pygame.K_RIGHT]:
        ship.x += 6
    if ship.x < 0:
        ship.x = 0
    if ship.x > 800 - ship.width:
        ship.x = 800 - ship.width

    # 算：能量球每帧向上挪 5（vy 是负的，y 越来越小 = 越飞越高）
    ball.y += ball_vy
    if ball.y < 0:                                    # 飞出天空
        ball.centerx = ship.centerx                   # 重置到飞船头顶
        ball.bottom = ship.top                        # （bottom 贴住飞船顶）

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)   # 亮黄能量球

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. ball_vy 改成 -10：能量球变成激光；改成 -2：慢速漂浮
#    2. ball_vy 改成 4（正数）会怎样？球往下沉——y 轴向下为正，屏幕世界里"下"是大的 y
#    3. 已埋好的细节：球出天后会回到"飞船头顶"（centerx/bottom 自动跟着船走），
#       开着飞船试试，球永远在你头顶重生
