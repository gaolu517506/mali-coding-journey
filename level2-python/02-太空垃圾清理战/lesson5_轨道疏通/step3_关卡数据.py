# -*- coding: utf-8 -*-
# 第 5 课 · 关卡数据（步骤 3）：数据驱动——关卡表
# 每关只有三个数不一样：几行、几列、球多快。
# 与其在代码里改来改去，不如把"关卡设计"做成一张表——
# 改关卡不用碰逻辑，这张表就是游戏的"设计图纸"。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道疏通 · 关卡")
clock = pygame.time.Clock()

W, H = 800, 600

# ── 关卡表：想设计新关卡，往这张表里加一行就行 ──
LEVELS = [
    {"rows": 3, "cols": 8, "speed": 5},       # 第 1 关：热身
    {"rows": 4, "cols": 9, "speed": 6},       # 第 2 关：更厚更快
    {"rows": 5, "cols": 10, "speed": 8},      # 第 3 关：垃圾风暴
]
ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120), (150, 120, 220)]

font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)   # 中文水笔
big_font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 60)

def build_trashes(rows, cols):
    "按行数列数生成垃圾阵（列数变了，间距自动收紧）"
    gap = (W - 40) / cols                     # 每列分到的宽度
    result = []
    for row in range(rows):
        for col in range(cols):
            x = 20 + col * gap
            r = pygame.Rect(int(x), 60 + row * 40, int(gap) - 16, 30)
            result.append([r, ROW_COLORS[row % len(ROW_COLORS)], 1, 10])
    return result

level = 0                                     # 当前关（从 0 数起）
lv = LEVELS[level]
trashes = build_trashes(lv["rows"], lv["cols"])
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -lv["speed"]
score, lives = 0, 3
state = "playing"                             # 三态：playing / win / over
win_all = False                               # 三关全通

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and state != "playing":
            if event.key == pygame.K_SPACE:
                if state == "win":            # 过关 → 下一关
                    level += 1
                    if level >= len(LEVELS):  # 全通了！
                        win_all = True
                        state = "playing"
                    else:
                        lv = LEVELS[level]
                        trashes = build_trashes(lv["rows"], lv["cols"])
                        ball_vx, ball_vy = 4, -lv["speed"]
                        state = "playing"
                else:                          # 输了 → 从头再来
                    level = 0
                    lv = LEVELS[level]
                    score, lives = 0, 3
                    trashes = build_trashes(lv["rows"], lv["cols"])
                    ball_vx, ball_vy = 4, -lv["speed"]
                    state = "playing"

    if state == "playing" and not win_all:
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

    # 画
    screen.fill((255, 226, 150) if win_all else (8, 8, 35))
    if win_all:
        screen.blit(big_font.render("全部疏通！", True, (180, 90, 20)), (230, 230))
        screen.blit(font.render(f"最终分数: {score}", True, (120, 70, 20)), (330, 320))
    elif state == "playing":
        for rect, color, hp, value in trashes:
            pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 200, 255), ship)
        pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
        screen.blit(font.render(f"第 {level + 1} 关   分数: {score}", True, (255, 255, 255)), (20, 555))
        screen.blit(font.render(f"生命: {'♥' * lives}", True, (255, 80, 120)), (660, 555))
    elif state == "win":
        screen.blit(big_font.render("过关！", True, (255, 215, 0)), (300, 230))
        screen.blit(font.render("按 空格 进入下一关", True, (255, 255, 255)), (300, 320))
    else:
        screen.blit(big_font.render("GAME OVER", True, (255, 60, 60)), (230, 250))
        screen.blit(font.render("按 空格 从第 1 关重来", True, (255, 255, 255)), (300, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 往 LEVELS 里加第 4 关：{"rows": 6, "cols": 11, "speed": 9}——你就是关卡设计师
#    2. LEVELS 里再加一个旋钮，比如 "hard": 2 表示每行都有硬垃圾（配合第 4 课挑战）
#    3. 思考：build_trashes 里 (W - 40) / cols 为什么能自动适配列数？
#       8 列和 10 列的垃圾块宽度分别约是多少？（print 算算）
