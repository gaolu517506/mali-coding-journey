# -*- coding: utf-8 -*-
# 第 5 课 · 挑战任务：关卡设计师
# 高级玩法：用"字符地图"设计关卡——每个字符是一格：
#   . 空位   G 普通垃圾   H 硬垃圾（2 命）   J 金垃圾（50 分）
# 你画的形状就是轨道上的垃圾阵。改地图 = 改游戏，一行逻辑都不用碰。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道疏通 · 关卡设计师")
clock = pygame.time.Clock()

W, H = 800, 600
font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 32)   # 中文水笔
big_font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 60)

# ── 你的设计图纸：想怎么摆就怎么改这三行字符串 ──
LEVEL_MAP = [
    "..HHHH..HHHH..",
    ".GGGGGGGGGGGG.",
    "JJ.GGGGGGGG.JJ",
    "..G.G.G.G.G...",
]

# 字符 → (颜色, 生命, 分值) 对照表
KINDS = {
    "G": ((255, 150, 60), 1, 10),     # 普通垃圾
    "H": ((140, 140, 150), 2, 30),    # 硬垃圾：2 条命
    "J": ((255, 215, 0), 1, 50),      # 金垃圾：高分
}

def build_from_map(level_map):
    "把字符地图翻译成垃圾名单"
    cols = len(level_map[0])              # 列数 = 第一行字符数
    gap = (W - 40) / cols
    result = []
    for row, line in enumerate(level_map):
        for col, ch in enumerate(line):
            if ch in KINDS:               # 是垃圾字符才放
                color, hp, value = KINDS[ch]
                r = pygame.Rect(int(20 + col * gap), 60 + row * 40, int(gap) - 8, 30)
                result.append([r, color, hp, value])
    return result

trashes = build_from_map(LEVEL_MAP)
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -6
score, lives = 0, 3
state = "playing"

def rebuild():
    "重开局"
    global trashes, score, lives, state, ball_vx, ball_vy
    trashes = build_from_map(LEVEL_MAP)
    score, lives, state = 0, 3, "playing"
    ball_vx, ball_vy = 4, -6
    ball.centerx = ship.centerx
    ball.bottom = ship.top

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and state != "playing":
            if event.key == pygame.K_SPACE:
                rebuild()

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
            ball_vy = -ball_vy
            ball.bottom = ship.top
        if ball.top > H:
            lives -= 1
            if lives <= 0:
                state = "over"
            else:
                ball.centerx = ship.centerx
                ball.bottom = ship.top
                ball_vx, ball_vy = 4, -6

        for trash in trashes[:]:
            rect, color, hp, value = trash
            if ball.colliderect(rect):
                trash[2] -= 1
                ball_vy = -ball_vy
                if trash[2] <= 0:
                    trashes.remove(trash)
                    score += value
                else:
                    trash[1] = (90, 90, 100)     # 硬垃圾挨了一打：变裂纹色
        if len(trashes) == 0:
            state = "win"

    # 画
    screen.fill((8, 8, 35))
    if state == "playing":
        for rect, color, hp, value in trashes:
            pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 200, 255), ship)
        pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
        screen.blit(font.render(f"分数: {score}", True, (255, 255, 255)), (20, 555))
        screen.blit(font.render(f"生命: {'♥' * lives}", True, (255, 80, 120)), (660, 555))
    elif state == "win":
        screen.blit(big_font.render("设计关卡被清空！", True, (255, 215, 0)), (180, 230))
        screen.blit(font.render("按 空格 再战你设计的关", True, (255, 255, 255)), (290, 320))
    else:
        screen.blit(big_font.render("GAME OVER", True, (255, 60, 60)), (230, 250))
        screen.blit(font.render("按 空格 重来", True, (255, 255, 255)), (330, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把 LEVEL_MAP 改成你设计的阵型——笑脸？金字塔？你的名字缩写？
#       （注意每行字符数要一样长，地图才整齐）
#    2. 加新品种：KINDS 里加 "B": ((80, 200, 120), 1, -20)——绿色毒垃圾，打中扣分！
#    3. 终极预告：第三幕「码力创作工坊」里，AI 会帮你生成新的关卡地图——
#       你现在打的地基，将来 AI 来盖楼
