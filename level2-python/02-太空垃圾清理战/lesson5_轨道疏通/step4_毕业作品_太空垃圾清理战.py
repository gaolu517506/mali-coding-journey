# -*- coding: utf-8 -*-
# 第 5 课 · 毕业作品（步骤 4）：《太空垃圾清理战》
# 五课手艺总装：主循环（1）+ 键盘与事件（2）+ 球与反弹（3）
# + 垃圾与计分（4）+ 生命、胜负与关卡（5）。
# 代码不长——因为每一块你都亲手造过了。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("太空垃圾清理战 · 毕业作品")
clock = pygame.time.Clock()

W, H = 800, 600
LEVELS = [
    {"rows": 3, "cols": 8, "speed": 5},
    {"rows": 4, "cols": 9, "speed": 6},
    {"rows": 5, "cols": 10, "speed": 8},
]
ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120), (150, 120, 220)]
font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)   # 中文水笔
big_font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 60)

def build_trashes(rows, cols):
    gap = (W - 40) / cols
    result = []
    for row in range(rows):
        for col in range(cols):
            r = pygame.Rect(int(20 + col * gap), 60 + row * 40, int(gap) - 16, 30)
            result.append([r, ROW_COLORS[row % len(ROW_COLORS)], 1, 10])
    return result

level = 0
lv = LEVELS[level]
trashes = build_trashes(lv["rows"], lv["cols"])
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -lv["speed"]
score, lives = 0, 3
state = "playing"                # playing / win / over / final（全通关）

running = True
while running:
    # 1. 听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == "playing" and event.key == pygame.K_ESCAPE:
                running = False
            if state in ("win", "over", "final") and event.key == pygame.K_SPACE:
                if state == "win":
                    level += 1
                    if level >= len(LEVELS):
                        state = "final"
                    else:
                        lv = LEVELS[level]
                        trashes = build_trashes(lv["rows"], lv["cols"])
                        ball_vx, ball_vy = 4, -lv["speed"]
                        state = "playing"
                elif state == "over":
                    level = 0
                    lv = LEVELS[level]
                    score, lives = 0, 3
                    trashes = build_trashes(lv["rows"], lv["cols"])
                    ball_vx, ball_vy = 4, -lv["speed"]
                    state = "playing"
                else:            # final：全通后从第 1 关再来
                    level = 0
                    lv = LEVELS[level]
                    score, lives = 0, 3
                    trashes = build_trashes(lv["rows"], lv["cols"])
                    ball_vx, ball_vy = 4, -lv["speed"]
                    state = "playing"

    # 2. 算
    if state == "playing":
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
            hit = (ball.centerx - ship.centerx) / (ship.width / 2)   # 控球（第 3 课）
            if hit > 1:
                hit = 1
            if hit < -1:
                hit = -1
            ball_vx = int(7 * hit)
            ball_vy = -max(3, 7 - abs(int(7 * hit)))
            ball.bottom = ship.top
        if ball.top > H:
            lives -= 1
            if lives <= 0:
                state = "over"
            else:
                ball.centerx = ship.centerx
                ball.bottom = ship.top
                ball_vx, ball_vy = 4, -lv["speed"]

        for trash in trashes[:]:
            rect, color, hp, value = trash
            if ball.colliderect(rect):
                trash[2] -= 1
                ball_vy = -ball_vy
                if trash[2] <= 0:
                    trashes.remove(trash)
                    score += value
        if len(trashes) == 0:
            state = "win"

    # 3. 画
    screen.fill((255, 226, 150) if state == "final" else (8, 8, 35))
    if state == "playing":
        for rect, color, hp, value in trashes:
            pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 200, 255), ship)
        pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
        screen.blit(font.render(f"第 {level + 1} 关   分数: {score}", True, (255, 255, 255)), (20, 555))
        screen.blit(font.render(f"生命: {'♥' * lives}   ESC 退出", True, (255, 80, 120)), (600, 555))
    elif state == "win":
        screen.blit(big_font.render("过关！", True, (255, 215, 0)), (300, 230))
        screen.blit(font.render("按 空格 进入下一关", True, (255, 255, 255)), (300, 320))
    elif state == "over":
        screen.blit(big_font.render("GAME OVER", True, (255, 60, 60)), (230, 250))
        screen.blit(font.render(f"分数: {score}   按 空格 从头再来", True, (255, 255, 255)), (290, 340))
    else:
        screen.blit(big_font.render("轨道全部疏通！", True, (180, 90, 20)), (170, 220))
        screen.blit(font.render("阳光重回地面，人类回家的路亮了 ✓", True, (120, 70, 20)), (220, 300))
        screen.blit(font.render(f"最终分数: {score}   按 空格 再战一轮", True, (120, 70, 20)), (250, 360))

    pygame.display.flip()
    # 4. 等
    clock.tick(60)

pygame.quit()

# 🔍 毕业检查单（全部打勾才算毕业）：
#    □ 能从第 1 关玩到通关（或至少撑过 2 关）
#    □ 能向同学解释"听-算-画-等"四步各在干嘛
#    □ 能指出：控球在哪几行？扣命在哪几行？关卡表在哪几行？
#    □ 截一张通关画面——这是你 Python 第二站的成绩单
