# -*- coding: utf-8 -*-
# 第 3 课 · 撞墙反弹（步骤 2）：速度反向
# 只会向上飞的球是烟花，会弹的球才是武器。
# 反弹的秘诀：撞哪面墙，就把那个方向的速度"反过来"。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("能量球 · 反弹")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx = 4                       # 横向速度：每帧向右 4
ball_vy = -5                      # 纵向速度：每帧向上 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.x -= 6
    if keys[pygame.K_RIGHT]:
        ship.x += 6
    if ship.x < 0:
        ship.x = 0
    if ship.x > W - ship.width:
        ship.x = W - ship.width

    # 算：球每帧挪（横竖各挪各的）
    ball.x += ball_vx
    ball.y += ball_vy

    # 算：三面墙反弹——身份证的 left/right/top 就是球的三条边
    if ball.left < 0 or ball.right > W:    # 撞左墙或右墙
        ball_vx = -ball_vx                 # 横速反过来：往左↔往右
    if ball.top < 0:                       # 撞天花板
        ball_vy = -ball_vy                 # 竖速反过来：向上→向下

    # 算：漏球了（掉出屏幕底）——回到飞船头顶重来
    if ball.top > H:
        ball.centerx = ship.centerx
        ball.bottom = ship.top
        ball_vx = 4
        ball_vy = -5

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把"撞左墙或右墙"的条件删掉一半（只留 ball.left < 0）——球会穿右墙消失
#    2. 换个开局角度：ball_vx = 7、ball_vy = -3，球的路线变得很斜
#    3. 思考：为什么撞墙要"把速度反过来"，而不是"把位置挪回去"？
#       （位置回去了，速度没变，下一帧又撞——出不去；反过来速度才能掉头飞走）
