# -*- coding: utf-8 -*-
# 第 1 课 · 满天星野（步骤 4）：用列表管理一群角色
# 一颗星要三个数（x、y、大小），六十颗星呢？
# 用列表装起来——以后游戏里的垃圾砖块、能量球，都是这样"装进列表统一管理"的。

import pygame
import random

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("码力的舷窗 · 星野")
clock = pygame.time.Clock()

# 造星野：每颗星是一个 [x, y, 大小] 的小口袋，全部装进 stars 大名单
stars = []
for i in range(60):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    size = random.randint(1, 4)
    stars.append([x, y, size])          # 追加进名单末尾

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画背景
    screen.fill((8, 8, 35))

    # 画星野：挨个从名单里取出小口袋，画一颗星
    for x, y, size in stars:            # 一次从口袋掏出三个数（星空站学过的！）
        pygame.draw.circle(screen, (255, 255, 255), (x, y), size)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 把 60 改成 150——星野的密度你说了算
#    2. 飞行感：在主循环"听"的下面加两行，让整片星野往左飘——
#       for star in stars: star[0] -= 1
#       for star in stars:
#           if star[0] < 0: star[0] = 800
#       飞船原地，星空倒退——这就是太空电影的手法
#    3. 想想看：这 60 颗星如果不用列表、一颗一行写要写多少行？
