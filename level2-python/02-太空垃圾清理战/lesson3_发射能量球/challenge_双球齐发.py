# -*- coding: utf-8 -*-
# 第 3 课 · 挑战任务：双球齐发
# 一个球不过瘾？用列表管理多个球——每颗球自己一张身份证、自己一份速度。
# 下一课的垃圾砖块，用的正是这套"列表管角色"的手艺。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("能量球 · 双球齐发")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)

# 球名单：每颗球 = [身份证Rect, 横速, 竖速, 颜色]
balls = [
    [pygame.Rect(300, 510, 16, 16), 4, -5, (255, 255, 120)],
    [pygame.Rect(460, 510, 16, 16), -4, -6, (120, 220, 255)],
]

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

    # 算：每颗球独立运动、独立反弹
    for b in balls:
        rect, vx, vy, color = b[0], b[1], b[2], b[3]
        rect.x += vx
        rect.y += vy
        if rect.left < 0 or rect.right > W:
            b[1] = -vx
        if rect.top < 0:
            b[2] = -vy
        if rect.colliderect(ship) and b[2] > 0:
            b[2] = -vy
            rect.bottom = ship.top
        if rect.top > H:                       # 这颗球漏了
            rect.centerx = ship.centerx        # 回到飞船头顶重生
            rect.bottom = ship.top
            b[1] = 4
            b[2] = -5

    # 画
    screen.fill((8, 8, 35))
    pygame.draw.rect(screen, (0, 200, 255), ship)
    for b in balls:
        pygame.draw.circle(screen, b[3], b[0].center, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 往 balls 里再追加一颗球（照抄一行，改改位置速度颜色）——三球齐发！
#    2. 给两颗球不同速度组合：一颗快而直（vx=1, vy=-8），一颗慢而斜（vx=6, vy=-3）
#    3. 思考：撞墙时我们改的是 b[1]（名单里的速度），如果只写 vx = -vx 会怎样？
#       （提示：vx 只是"复印件"，改复印件，名单里的原版不会变）
