# -*- coding: utf-8 -*-
# 第 3 课 · 飞船反弹（步骤 3）：碰撞检测
# 球会撞墙了，还要会撞飞船——这是打砖块类游戏的灵魂：
# colliderect：两张身份证碰一碰，重叠就返回 True。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("能量球 · 飞船反弹")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx = 4
ball_vy = -5

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

    # 算：球运动 + 三面墙反弹（上一课手艺）
    ball.x += ball_vx
    ball.y += ball_vy
    if ball.left < 0 or ball.right > W:
        ball_vx = -ball_vx
    if ball.top < 0:
        ball_vy = -ball_vy

    # 算：撞飞船！——身份证碰身份证
    if ball.colliderect(ship) and ball_vy > 0:   # 碰到飞船，且球正在下落
        ball_vy = -ball_vy                       # 竖速反过来：弹回太空
        ball.bottom = ship.top                   # 把球顶回飞船上方（防粘连！）

    # 算：漏球重置
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
#    1. 删掉 ball.bottom = ship.top 这行再玩——球会"粘"在飞船上抖！
#       因为反弹后下一帧还和飞船重叠，又反弹……位置顶出去才能彻底分开
#    2. 加速球：在撞飞船的 if 里加一行 ball_vy = -ball_vy * 1.05——每弹一次快 5%
#    3. 条件里 and ball_vy > 0 去掉会怎样？刚弹起的球（还在飞船附近）又被判碰撞，
#       方向瞬间翻回去——所以"只拦下落的球"很重要
