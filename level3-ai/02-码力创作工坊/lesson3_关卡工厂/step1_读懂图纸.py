# -*- coding: utf-8 -*-
# 第 3 课 · 读懂图纸（步骤 1）：关卡字符地图
# 工坊最后一课：给第二站的《太空垃圾清理战》供货新关卡！
# 先学会读"图纸"——第二站关卡设计师用的字符地图：
#   . = 空位   G = 普通垃圾(10分)   H = 硬垃圾(2条命,30分)   J = 金垃圾(50分)
# 本步骤零依赖：手工画一张图纸，程序帮你"预览"它长什么样。

# ── 一张关卡图纸：每行字符数要一样长！──
LEVEL_MAP = [
    "....JJJJ....",
    "..GGGGGGGG..",
    ".HH.HH.HH.HH",      # ← 第三行少一个字符！先跑一遍看会发生什么
    "GG.G.G.G.G.G",
]

# 字符 → 含义对照表（和第二站游戏里的规则一致）
KINDS = {
    "G": ("普通垃圾", 10),
    "H": ("硬垃圾(2条命)", 30),
    "J": ("金垃圾", 50),
}

print("═ 关卡图纸预览 ═\n")
for row in LEVEL_MAP:
    line = ""
    for ch in row:
        if ch == ".":
            line += "·"               # 空位画成小点
        elif ch == "G":
            line += "▓"               # 普通垃圾
        elif ch == "H":
            line += "█"               # 硬垃圾（厚）
        elif ch == "J":
            line += "★"               # 金垃圾
        else:
            line += "?"               # 不认识的字符（画问号提醒）
    print("   " + line)

# 图纸体检：行数、行长、垃圾总数、满分
print("\n═ 图纸体检报告 ═")
widths = [len(row) for row in LEVEL_MAP]
print(f"行数：{len(LEVEL_MAP)} 行，各行长度：{widths}")
if len(set(widths)) != 1:
    bad = widths.index(min(widths)) + 1
    print(f"❌ 行长不一致！第 {bad} 行短了——游戏按第一行的长度算列数，短行会'缺一块'")
else:
    print("✅ 行长全部一致")

total, score = 0, 0
for row in LEVEL_MAP:
    for ch in row:
        if ch in KINDS:
            total += 1
            score += KINDS[ch][1]
print(f"垃圾总数：{total} 块，通关满分：{score} 分")

# 🔍 小实验：
#    1. 修复第三行（补一个字符），重跑直到体检全绿
#    2. 设计你自己的阵型：金字塔？笑脸？你的名字缩写？（改 LEVEL_MAP 四行字符串）
#    3. 算难度：满分除以垃圾总数是"平均每块价值"——数值越高关卡越"刺激"
#       （想想第二站：H 要打两下，J 又远又贵——图纸就是关卡设计的一切）
