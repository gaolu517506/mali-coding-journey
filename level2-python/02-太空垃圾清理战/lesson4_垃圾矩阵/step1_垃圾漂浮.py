# -*- coding: utf-8 -*-
# 第 4 课 · 垃圾漂浮（步骤 1）：一行太空垃圾
# 目标登场：轨道上的太空垃圾（打砖块的"砖"）。
# 8 块垃圾怎么管？又是老朋友——列表 + 循环。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道垃圾 · 一")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5

# 垃圾名单：一行 8 块——每块 80 宽，块间留 16 缝隙，从 x=20 开始铺
trashes = []
for i in range(8):
    r = pygame.Rect(20 + i * 96, 60, 80, 30)   # 20, 116, 212, ... 每块右移 96
    trashes.append(r)

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
    if ball.colliderect(ship) and ball_vy > 0:
        ball_vy = -ball_vy
        ball.bottom = ship.top
    if ball.top > H:
        ball.centerx = ship.centerx
        ball.bottom = ship.top
        ball_vx, ball_vy = 4, -5

    # 画
    screen.fill((8, 8, 35))
    for trash in trashes:                       # 名单里每块垃圾画一笔
        pygame.draw.rect(screen, (160, 120, 90), trash)     # 太空垃圾：锈棕色
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把 range(8) 改成 range(6)——垃圾少了两块，右边留出空轨道
#    2. 给垃圾块加边框：rect 的第 5 个参数 width，
#       pygame.draw.rect(screen, (160, 120, 90), trash, 3)——变成描边空心块
#    3. 思考：20 + i * 96 这个算式里，96 是怎么来的？（80 块宽 + 16 缝隙）
