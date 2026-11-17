# -*- coding: utf-8 -*-
# 第 4 课 · 挑战任务：特殊垃圾
# 普通垃圾一击就碎，太没挑战——造两种特殊货：
# 硬垃圾（要打两次：第一打变"裂纹色"，第二打才碎）和金色垃圾（值 50 分）。
# 每块垃圾的口袋变大了：[身份证, 颜色, 生命值, 分值]。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道垃圾 · 特殊垃圾")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5
score = 0
# 中文水笔（名单里谁在用谁：Windows 微软雅黑 / Mac 冬青黑体）
font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)

ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120)]
trashes = []
for row in range(4):
    for col in range(8):
        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)
        if row == 0 and col % 3 == 0:            # 第 1 行隔 3 列放一块硬垃圾
            trashes.append([r, (140, 140, 150), 2, 30])   # 灰钢色，2 条命，30 分
        elif row == 2 and col % 4 == 1:          # 第 3 行隔 4 列放一块金垃圾
            trashes.append([r, (255, 215, 0), 1, 50])     # 金色，1 条命，50 分
        else:
            trashes.append([r, ROW_COLORS[row], 1, 10])   # 普通垃圾

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

    # 算：打垃圾——先扣血，血空才删除
    for trash in trashes[:]:
        rect, color, hp, value = trash           # 口袋掏四个：身份证、颜色、命、分值
        if ball.colliderect(rect):
            trash[2] -= 1                        # 血 -1
            ball_vy = -ball_vy
            if trash[2] <= 0:                    # 血空了
                trashes.remove(trash)
                score += value
            else:                                # 还剩 1 条命：变裂纹色
                trash[1] = (90, 90, 100)         # 换暗色表示"裂了"

    # 画
    screen.fill((8, 8, 35))
    for rect, color, hp, value in trashes:
        pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
    screen.blit(font.render(f"分数: {score}", True, (255, 255, 255)), (20, 555))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把硬垃圾的命改成 3——钢化垃圾，得打三下（记得配色看得出"越打越暗"）
#    2. 自创垃圾品种：会移动的垃圾（每帧 rect.x += 1，撞右墙反向）？
#       会加命的"补给舱"（打中 lives + 1，第 5 课有 lives）？
#    3. 思考：为什么打垃圾要"先扣血再查血"？直接删行不行——
#       那硬垃圾和普通垃圾就没区别了
