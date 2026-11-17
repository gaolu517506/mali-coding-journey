# -*- coding: utf-8 -*-
# 第 4 课 · 分数面板（步骤 4）：把字画进游戏
# 战报只在终端里不过瘾——用 pygame.font 把分数画进游戏画面。
# f"分数: {score}" 是"会说话的字符串"：大括号里的名字会被换成真值。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道垃圾 · 计分板")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5
score = 0

# 中文水笔：SysFont 从名单里挑一个电脑上有的中文字体
# （Windows 用微软雅黑，Mac 用冬青黑体/苹果 Arial Unicode——默认字体不含中文，会变豆腐块□）
font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)

ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120)]
trashes = []
for row in range(4):
    for col in range(8):
        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)
        trashes.append([r, ROW_COLORS[row]])

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

    for trash in trashes[:]:
        if ball.colliderect(trash[0]):
            trashes.remove(trash)
            ball_vy = -ball_vy
            score += 10

    # 画
    screen.fill((8, 8, 35))
    for trash, color in trashes:
        pygame.draw.rect(screen, color, trash)
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)

    # 画字：先用笔 render 出"字片"，再把字片贴到画面上
    score_text = font.render(f"分数: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 555))                      # 左下角
    left_text = font.render(f"剩余垃圾: {len(trashes)}", True, (180, 180, 180))
    screen.blit(left_text, (640, 555))                      # 右下角

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. f 字符串玩法：f"分数: {score} 分，剩余 {len(trashes)} 块"——大括号可以放表达式
#    2. 字号 32 改 48，分数更醒目；SysFont(None, 48, bold=True) 还能加粗
#    3. 游戏名大字：造第二支笔 big_font = pygame.font.SysFont(None, 60)，
#       在画面顶部中间 blit 一行"太空垃圾清理战"
