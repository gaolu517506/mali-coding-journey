# -*- coding: utf-8 -*-
# 第 2 课 · 造飞船（步骤 1）：Rect——角色的身份证
# 舷窗有了、星空有了，主角登场：码力的清理飞船。
# pygame 给每个角色发一张"身份证"（Rect）：上面记着它的位置和大小。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的飞船")
clock = pygame.time.Clock()

# 飞船的身份证：Rect(x, y, 宽, 高)——(350, 540) 是左上角，停在屏幕底部
ship = pygame.Rect(350, 540, 100, 18)
SHIP_COLOR = (0, 200, 255)       # 青色船身

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画：深夜底 + 星野 + 飞船
    screen.fill((8, 8, 35))
    pygame.draw.circle(screen, (255, 255, 255), (150, 120), 3)
    pygame.draw.circle(screen, (255, 255, 255), (650, 300), 2)
    pygame.draw.circle(screen, (255, 255, 255), (420, 80), 4)

    pygame.draw.rect(screen, SHIP_COLOR, ship)            # 船身：矩形
    cockpit = pygame.Rect(ship.x + 40, ship.y - 10, 20, 12)  # 驾驶舱叠上去
    pygame.draw.rect(screen, (255, 215, 0), cockpit)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 改身份证上的数字：x 改 100，飞船挪到左边；宽改 140，飞船变宽
#    2. 身份证上还藏着信息：print(ship.centerx) 试试——不用自己算，中心点它知道
#    3. 给飞船加一对推进器（船身下面两个小矩形，画红色）
