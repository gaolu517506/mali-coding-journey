# -*- coding: utf-8 -*-
# 第 5 课 · 三条命（步骤 1）：生命与 Game Over
# 真游戏有输的可能：漏一颗球扣一条命，命光了 Game Over。
# 这引入"游戏状态"：playing（玩着）还是 gameover（结束了）。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道疏通 · 生命")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5
score = 0
lives = 3                                   # 三条命
game_over = False                           # 游戏状态：还在玩

# 中文水笔（名单里谁在用谁：Windows 微软雅黑 / Mac 冬青黑体）
font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)
big_font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 72)

ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120)]
trashes = []
for row in range(4):
    for col in range(8):
        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)
        trashes.append([r, ROW_COLORS[row], 1, 10])

def reset_ball():
    "球回到飞船头顶"
    ball.centerx = ship.centerx
    ball.bottom = ship.top
    return 4, -5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:  # Game Over 后按空格 → 重开一局
                score, lives, game_over = 0, 3, False
                ball_vx, ball_vy = reset_ball()

    if not game_over:                        # ── 只在"玩着"时才结算运动 ──
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

        if ball.top > H:                     # 漏球！
            lives -= 1                       # 扣一条命
            if lives <= 0:
                game_over = True             # 命光：游戏结束
            else:
                ball_vx, ball_vy = reset_ball()

        for trash in trashes[:]:
            rect, color, hp, value = trash
            if ball.colliderect(rect):
                trash[2] -= 1
                ball_vy = -ball_vy
                if trash[2] <= 0:
                    trashes.remove(trash)
                    score += value

    # 画
    screen.fill((8, 8, 35))
    for rect, color, hp, value in trashes:
        pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
    screen.blit(font.render(f"分数: {score}", True, (255, 255, 255)), (20, 555))
    screen.blit(font.render(f"生命: {'♥' * lives}", True, (255, 80, 120)), (660, 555))

    if game_over:                            # 结束画面盖在最上层
        screen.blit(big_font.render("GAME OVER", True, (255, 60, 60)), (230, 250))
        screen.blit(font.render("按 空格 重新开始", True, (255, 255, 255)), (310, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. lives 改 5 更宽容；改 1 就是"一命通关"模式
#    2. ♥ 符号换成 ● 或 ❥，找到你喜欢的命值图标
#    3. 思考：为什么运动结算要包在 if not game_over 里？
#       去掉试试——Game Over 画面背后球还在乱飞（幽灵球）
