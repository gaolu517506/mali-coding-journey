# -*- coding: utf-8 -*-
# 第 3 课 · AI 画图纸（步骤 2）：让 AI 当关卡设计师
# 关卡图纸 = 一小段文字。这正好是 AI 的主场！
# 关键在订单：格式约束必须说死（行数、每行长度、字符集），否则 AI 会自由发挥。

import os
import requests

print("嘀——AI 设计师上岗！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(order):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=120,
    )
    return r.json()["choices"][0]["message"]["content"]

# 设计订单：把格式说死到没有发挥空间
order = """你是游戏关卡设计师。为"太空垃圾清理战"（打砖块游戏）设计一张关卡字符地图。

格式硬性要求（一条都不能违反）：
1. 恰好 5 行，每行恰好 12 个字符；
2. 只允许这 4 种字符（字符之间不要加空格）：. （空位）、G（普通垃圾）、H（硬垃圾）、J（金垃圾）；
3. 第一行放 J（金垃圾）为主，最后一行不要放垃圾（留给玩家瞄准的空间）；
4. 阵型要左右对称，像一座金字塔；
5. 输出格式：只输出 5 行字符串（用三引号 ''' 包起来），不要任何解释。"""

print("向 AI 设计师下单（金字塔阵型）……\n")
raw = ask(order)

# 剥壳：AI 交稿的包装五花八门（代码块、三引号、赋值语句……）——层层剥，见 step3
if "```" in raw:                              # 先剥 Markdown 代码块
    for block in raw.split("```"):
        if any(c in block for c in "GHJ"):
            raw = block
            break
if "'''" in raw or '"""' in raw:              # 再剥三引号（单/双都认）
    for q in ('"""', "'''"):
        if q in raw:
            for part in raw.split(q):
                if any(c in part for c in "GHJ"):
                    raw = part
                    break

# 拆成行，只保留"纯地图行"（全部由 . G H J 组成的行，长度 8 以上防误捞）
lines = [line.strip() for line in raw.splitlines()
         if line.strip() and set(line.strip()) <= set(".GHJ") and len(line.strip()) >= 8]

print("═ AI 设计师交稿 ═")
for line in lines:
    print("   ", line)

# 快速体检（详细校验下一课专门做）
print("\n═ 快速体检 ═")
print(f"行数：{len(lines)} 行（要求 5 行）")
widths = [len(line) for line in lines]
print(f"各行长度：{widths}（要求全部 12）")
bad_chars = set("".join(lines)) - set(".GHJ")
print(f"非法字符：{bad_chars if bad_chars else '无'}")

if len(lines) == 5 and set(widths) == {12} and not bad_chars:
    print("✅ 格式全对——AI 这单活儿干得漂亮！")
else:
    print("❌ 格式没全对——正常现象！AI 会犯错，怎么办？下一课：验证员上岗")

# 🔍 小实验：
#    1. 换个阵型主题重下单："笑脸"、"一道门"、"之字形"（改第 4 条）
#    2. 故意刁难 AI：把行数改成 7 行、每行 15 字符——它还守得住格式吗？
#    3. 多跑几次：同一订单，AI 每次设计的阵型一样吗？（temperature 在起作用）
