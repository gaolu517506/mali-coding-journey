# -*- coding: utf-8 -*-
# 第 1 课 · 挑战任务：流星雨
# 星野是"背景"，流星是"角色"——每颗流星有自己的位置和速度，
# 每帧算一步、飞出屏幕就回到顶上重生。你已具备全部手艺。

import pygame
import random

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的舷窗 · 流星雨")
clock = pygame.time.Clock()

# 背景星野（静态）
stars = []
for i in range(70):
    stars.append([random.randint(0, 800), random.randint(0, 600), random.randint(1, 3)])

# 流星名单：每颗 = [x, y, 每帧横速, 每帧竖速, 大小]
meteors = []
for i in range(8):
    meteors.append([
        random.randint(0, 800),          # x：随机出生点
        random.randint(-600, 0),         # y：从屏幕上方外面出发
        random.randint(2, 6),            # 横速：往右下斜着飞
        random.randint(4, 9),            # 竖速
        random.randint(2, 4),            # 大小
    ])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 算：每颗流星飞一步，出界就回顶部重生
    for m in meteors:
        m[0] += m[2]                     # x 挪
        m[1] += m[3]                     # y 挪
        if m[1] > 600 or m[0] > 800:     # 飞出底部或右侧
            m[0] = random.randint(-200, 600)   # 重新出生
            m[1] = random.randint(-600, -20)

    # 画：先星野后流星（角色画在背景上面）
    screen.fill((8, 8, 35))
    for x, y, size in stars:
        pygame.draw.circle(screen, (60, 60, 90), (x, y), size)
    for m in meteors:
        pygame.draw.circle(screen, (200, 230, 255), (m[0], m[1]), m[4])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把流星加到 20 颗——今晚有流星暴
#    2. 给流星加"尾巴"：在流星位置先画一个大而暗的圆，再画小而亮的圆，
#       两层叠出微光尾巴（三层更明显）
#    3. 思考：流星为什么不能只检查 y > 600 一个条件就重生？
#       （提示：有的流星横得快，先从右边飞出去了）
