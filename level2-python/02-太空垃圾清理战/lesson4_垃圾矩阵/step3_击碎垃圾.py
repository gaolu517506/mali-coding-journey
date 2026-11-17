# -*- coding: utf-8 -*-
# 第 4 课 · 击碎垃圾（步骤 3）：碰撞消除 + 计分
# 本课大招：球撞到垃圾块 → 这块垃圾从名单里删掉（消失）→ 球反弹 → 加分。
# 打砖块的"打"，就是"碰撞 + 删除"。

import pygame

print("嘀——码力启动！")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("轨道垃圾 · 击碎")
clock = pygame.time.Clock()

W, H = 800, 600
ship = pygame.Rect(350, 540, 100, 18)
ball = pygame.Rect(392, 510, 16, 16)
ball_vx, ball_vy = 4, -5
score = 0                        # 分数：从 0 开始，每碎一块垃圾 +10

ROW_COLORS = [(255, 80, 80), (255, 150, 60), (255, 210, 60), (120, 200, 120)]
trashes = []
for row in range(4):
    for col in range(8):
        r = pygame.Rect(20 + col * 96, 60 + row * 40, 80, 30)
        trashes.append([r, ROW_COLORS[row]])

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
        ball.centerx = ship.centerx
        ball.bottom = ship.top
        ball_vx, ball_vy = 4, -5

    # 算：球 vs 每一块垃圾
    # ⚠️ 边遍历边删是大坑：一边数名单一边划掉名字会数乱——
    #    先复印一份名单（trashes[:]）来数，原件上放心删
    for trash in trashes[:]:
        if ball.colliderect(trash[0]):          # 球撞上这块垃圾
            trashes.remove(trash)               # 从名单里删掉（它消失了）
            ball_vy = -ball_vy                  # 球反弹（简化：竖速反向）
            score += 10                         # 加分！
            print("轰！+10 分，当前", score)    # 终端同步战报

    # 画
    screen.fill((8, 8, 35))
    for trash, color in trashes:
        pygame.draw.rect(screen, color, trash)
    pygame.draw.rect(screen, (0, 200, 255), ship)
    pygame.draw.circle(screen, (255, 255, 120), ball.center, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# 🔍 小实验：
#    1. 打掉几块垃圾，看终端冒出的战报——分数真的在涨
#    2. 把 trashes[:] 改成 trashes 再玩：撞碎某块时会漏删或报错——
#       这就是"边数边删"的坑（教师演示用，学生知道用 [:] 就好）
#    3. 思考：球速很快时，一帧可能穿过一整块垃圾（没检测到碰撞）——
#       这叫"穿隧"。把 tick(60) 的球速放慢能缓解，彻底解决要"分步移动"（课后探索）
