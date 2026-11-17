# -*- coding: utf-8 -*-
# 太空垃圾清理战 · 展示版（pygame 打砖块）
# 第二幕 · 造物站② 的完整成品：3 关、3 条命、控球、硬垃圾、金垃圾、暂停与通关结算。
# 课程版（学生跟做）见 lesson1~lesson5；本文件是"最终形态"参考实现。
#
# 操作：←/→ 驾驶飞船   空格 开始/继续   P 暂停   F12 截图存档   ESC 退出
# 运行前请安装：pip install pygame-ce  （Thonny 用户：工具 → 管理软件包 → 搜 pygame-ce）

import pygame

print("嘀——码力启动！")

# ── 配置区 ────────────────────────────────────────────
W, H = 800, 600
FPS = 60
BG = (8, 8, 35)
GOLD = (255, 215, 0)
LEVELS = [
    {"rows": 3, "cols": 8, "speed": 5, "hard": False},
    {"rows": 4, "cols": 9, "speed": 6, "hard": True},
    {"rows": 5, "cols": 10, "speed": 7, "hard": True},
]
ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120), (150, 120, 220)]

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("太空垃圾清理战 · 码力回家 第二幕")
clock = pygame.time.Clock()
font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 30)   # 中文水笔：名单里谁在用谁
big_font = pygame.font.SysFont("microsoftyahei,hiraginosansgb,arialunicode", 64, bold=True)

# ── 角色与状态 ────────────────────────────────────────
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5
score, lives, level = 0, 3, 0
trashes = []
stars = [(pygame.Vector2(20 + i * 61 % W, (i * 97) % H), 1 + i % 3) for i in range(40)]
state = "start"        # start / playing / win / over / final / paused


def build_trashes(lv):
    """按关卡参数生成垃圾阵：hard 关卡的第 0 行放硬垃圾，隔列放金垃圾"""
    gap = (W - 40) / lv["cols"]
    result = []
    for row in range(lv["rows"]):
        for col in range(lv["cols"]):
            r = pygame.Rect(int(20 + col * gap), 60 + row * 40, int(gap) - 16, 30)
            if lv["hard"] and row == 0 and col % 4 == 1:
                result.append([r, (140, 140, 150), 2, 30])     # 硬垃圾
            elif lv["hard"] and row == lv["rows"] - 1 and col % 5 == 2:
                result.append([r, GOLD, 1, 50])                # 金垃圾
            else:
                result.append([r, ROW_COLORS[row % len(ROW_COLORS)], 1, 10])
    return result


def start_level(n):
    """进入第 n 关（0 起）"""
    global level, trashes, ball_vx, ball_vy
    level = n
    trashes = build_trashes(LEVELS[n])
    ball.centerx, ball.bottom = ship.centerx, ship.top
    ball_vx, ball_vy = 4, -LEVELS[n]["speed"]


def draw_center(text, f, color, y):
    screen.blit(f.render(text, True, color), (W // 2 - f.render(text, True, color).get_width() // 2, y))


# ── 主循环：听 → 算 → 画 → 等 ──────────────────────────
running = True
while running:
    # 1. 听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_F12:                        # 截图彩蛋
                pygame.image.save(screen, "screenshot_清理战.png")
                print("📸 画面已存到 screenshot_清理战.png")
            if event.key == pygame.K_SPACE:
                if state == "start":
                    score, lives = 0, 3
                    start_level(0)
                    state = "playing"
                elif state in ("win", "over", "final"):
                    score, lives = 0, 3
                    start_level(0)
                    state = "playing"
            if event.key == pygame.K_p and state in ("playing", "paused"):
                state = "paused" if state == "playing" else "playing"

    # 2. 算
    if state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.x -= 6
        if keys[pygame.K_RIGHT]:
            ship.x += 6
        ship.x = max(0, min(ship.x, W - ship.width))

        ball.x += ball_vx
        ball.y += ball_vy
        if ball.left < 0 or ball.right > W:
            ball_vx = -ball_vx
        if ball.top < 0:
            ball_vy = -ball_vy
        if ball.colliderect(ship) and ball_vy > 0:               # 控球反弹
            hit = max(-1, min(1, (ball.centerx - ship.centerx) / (ship.width / 2)))
            ball_vx = int(7 * hit)
            ball_vy = -max(3, 7 - abs(int(7 * hit)))
            ball.bottom = ship.top
        if ball.top > H:                                          # 漏球
            lives -= 1
            if lives <= 0:
                state = "over"
            else:
                ball.centerx, ball.bottom = ship.centerx, ship.top
                ball_vx, ball_vy = 4, -LEVELS[level]["speed"]

        for trash in trashes[:]:                                 # 打垃圾
            rect, color, hp, value = trash
            if ball.colliderect(rect):
                trash[2] -= 1
                ball_vy = -ball_vy
                if trash[2] <= 0:
                    trashes.remove(trash)
                    score += value
                else:
                    trash[1] = (90, 90, 100)                      # 硬垃圾裂纹
        if len(trashes) == 0:
            if level + 1 >= len(LEVELS):
                state = "final"
            else:
                state = "win"

    # 3. 画
    screen.fill(BG)
    if state == "start":
        for pos, size in stars:
            pygame.draw.circle(screen, (60, 60, 90), (int(pos.x), int(pos.y)), size)
        draw_center("太空垃圾清理战", big_font, GOLD, 170)
        draw_center("第二幕 · 造物站② ｜ pygame 打砖块", font, (200, 200, 200), 250)
        draw_center("←/→ 驾驶飞船   P 暂停   F12 截图   ESC 退出", font, (200, 200, 200), 330)
        draw_center("按 空格 出击", font, (255, 255, 120), 420)
    elif state == "paused":
        draw_center("已暂停", big_font, (150, 150, 150), 250)
        draw_center("按 P 继续", font, (200, 200, 200), 330)
    elif state == "win":
        draw_center(f"第 {level + 1} 关 过！", big_font, GOLD, 220)
        draw_center(f"当前分数: {score}", font, (255, 255, 255), 300)
        draw_center("按 空格 进入下一关", font, (200, 200, 200), 360)
    elif state == "over":
        draw_center("GAME OVER", big_font, (255, 60, 60), 220)
        draw_center(f"分数: {score}   打到第 {level + 1} 关", font, (255, 255, 255), 300)
        draw_center("按 空格 从头再战", font, (200, 200, 200), 360)
    elif state == "final":
        screen.fill((255, 226, 150))
        draw_center("轨道全部疏通！", big_font, (180, 90, 20), 200)
        draw_center("阳光重回地面，人类回家的路亮了", font, (120, 70, 20), 290)
        draw_center(f"最终分数: {score}", font, (120, 70, 20), 350)
        draw_center("按 空格 再战一轮", font, (120, 70, 20), 410)
    else:
        for pos, size in stars:
            pygame.draw.circle(screen, (60, 60, 90), (int(pos.x), int(pos.y)), size)
        for rect, color, hp, value in trashes:
            pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 200, 255), ship)
        pygame.draw.rect(screen, (255, 255, 255), (ship.centerx - 1, ship.y, 2, 18))  # 瞄准线
        pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)
        screen.blit(font.render(f"第 {level + 1} 关   分数: {score}", True, (255, 255, 255)), (20, 560))
        screen.blit(font.render(f"生命: {'♥' * lives}   P 暂停", True, (255, 80, 120)), (580, 560))

    pygame.display.flip()
    # 4. 等
    clock.tick(FPS)

pygame.quit()
print(f"本局分数: {score}  —— 轨道因你更干净了一点点。")
