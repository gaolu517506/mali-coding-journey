# -*- coding: utf-8 -*-
# 第 5 课 · 胜利之光（步骤 2）：清空轨道，阳光重回地面
# 游戏有了输，还要有赢：垃圾清空 → 胜利。
# 胜利画面的底色换成晨光金——这就是故事里说的"轨道疏通，阳光重回地表"。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道疏通 · 胜利")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5
score, lives = 0, 3
game_over = False                             # 输了
game_win = False                              # 赢了（两个状态开关）

font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)   # 中文水笔
big_font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 60)

ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120)]
trashes = []
for row in range(4):
    for col in range(8):
        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)
        trashes.append([r, ROW_COLORS[row], 1, 10])

def reset_ball():
    ball.centerx = ship.centerx
    ball.bottom = ship.top
    return 4, -5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and (game_over or game_win):
            if event.key == pygame.K_SPACE:   # 重开一局
                trashes.clear()
                for row in range(4):
                    for col in range(8):
                        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)
                        trashes.append([r, ROW_COLORS[row], 1, 10])
                score, lives = 0, 3
                game_over, game_win = False, False
                ball_vx, ball_vy = reset_ball()

    if not game_over and not game_win:        # 只有"玩着"才结算
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
            lives -= 1
            if lives <= 0:
                game_over = True
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
        if len(trashes) == 0:                 # 名单空了：轨道疏通！
            game_win = True

    # 画：平时深夜色，胜利换晨光金
    screen.fill((255, 226, 150) if game_win else (8, 8, 35))
    if not game_win:
        for rect, color, hp, value in trashes:
            pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 200, 255), ship)
        pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
        screen.blit(font.render(f"分数: {score}", True, (255, 255, 255)), (20, 555))
        screen.blit(font.render(f"生命: {'♥' * lives}", True, (255, 80, 120)), (660, 555))
    else:
        screen.blit(big_font.render("轨道疏通！", True, (180, 90, 20)), (240, 220))
        screen.blit(font.render("阳光重回地面 ✓", True, (120, 70, 20)), (320, 300))
        screen.blit(font.render(f"最终分数: {score}   按 空格 再来一局", True, (120, 70, 20)), (250, 360))

    if game_over:
        screen.blit(big_font.render("GAME OVER", True, (255, 60, 60)), (230, 250))
        screen.blit(font.render("按 空格 重新开始", True, (255, 255, 255)), (310, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 胜利文案自己写："码力向你敬礼！" / "人类的回家之路又近了一步"
#    2. 想快速看胜利画面：把垃圾初始改成 1 块（range(1) 行 range(1) 列），一球定音
#    3. 思考：game_over 和 game_win 为什么要用两个开关而不是一个？
#       一个开关存三种状态（玩/赢/输）也行：state = "playing"——下一课我们就这样重构
