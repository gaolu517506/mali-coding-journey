# -*- coding: utf-8 -*-
# 第 4 课 · 垃圾矩阵（步骤 2）：循环套循环铺砖阵
# 一行垃圾不够挡阳光——铺满 4 行 8 列。
# 外层循环数行、内层循环数列（星空站画北斗七星时的双层循环，长大了）。
# 每块垃圾 = [身份证, 颜色]，颜色按行分：离地球越近的越危险（越红）。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道垃圾 · 矩阵")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5

ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120)]

# 垃圾矩阵：外层管行（4 行），内层管列（8 列）
trashes = []
for row in range(4):
    for col in range(8):
        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)  # 行往下错 40
        trashes.append([r, ROW_COLORS[row]])                   # 口袋：[身份证, 颜色]

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
    for trash, color in trashes:                # 一次掏两个：身份证 + 颜色
        pygame.draw.rect(screen, color, trash)
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. range(4) 改 range(6)：垃圾墙变厚——阳光快被挡完了！
#    2. 换个阵型：把内层的 20 + col * 96 改成 20 + col * 96 + row * 20——
#       每行往右错开 20，砖阵变成斜的阶梯
#    3. 思考：4 行 × 8 列 = 32 块垃圾，列表里有几个口袋？（print(len(trashes)) 验证）
