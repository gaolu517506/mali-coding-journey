# -*- coding: utf-8 -*-
# 第 3 课 · 角度反弹（步骤 4）：打在哪，飞向哪
# 真正的打砖块高手能"控球"：用飞船左边缘接球，球就往左飞。
# 秘密：按命中飞船的位置，重新分配横竖速度。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("能量球 · 控球")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx = 4
ball_vy = -5
BALL_SPEED = 7                   # 球的总速度（横竖分量的"总预算"）

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

    ball.x += ball_vx
    ball.y += ball_vy
    if ball.left < 0 or ball.right > W:
        ball_vx = -ball_vx
    if ball.top < 0:
        ball_vy = -ball_vy

    # 算：命中位置决定反弹角度
    if ball.colliderect(ship) and ball_vy > 0:
        # hit：打在飞船正中是 0，左边缘约 -1，右边缘约 +1
        hit = (ball.centerx - ship.centerx) / (ship.width / 2)
        if hit > 1:              # 防止极端值（球超出船边缘太多）
            hit = 1
        if hit < -1:
            hit = -1
        ball_vx = int(BALL_SPEED * hit)          # 横速：命中越偏，横得越厉害
        ball_vy = -int(BALL_SPEED * (1 - abs(hit) * 0.7))   # 竖速相应变小
        ball.bottom = ship.top

    if ball.top > H:
        ball.centerx = ship.centerx
        ball.bottom = ship.top
        ball_vx = 4
        ball_vy = -5

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.rect(screen, (0, 200, 255), ship)
    # 船中刻一条瞄准线：提示"打这里球会直着飞"
    pygame.draw.rect(screen, (255, 255, 255), (ship.centerx - 1, ship.y, 2, 18))
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 分别用船的左边缘、正中、右边缘接球，观察三种反弹路线——你就是控球手
#    2. 把 0.7 改成 0：边缘接球时球变成水平飞（永远上不去——这就是为什么要留竖速）
#    3. BALL_SPEED 改 10：球更快，控球更难——快去试试你的手感
