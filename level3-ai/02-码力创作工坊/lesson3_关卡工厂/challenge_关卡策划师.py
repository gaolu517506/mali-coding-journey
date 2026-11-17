# -*- coding: utf-8 -*-
# 第 3 课 · 挑战任务：关卡策划师
# 接一张"策划单"：客户要三个主题关卡（金字塔 / 笑脸 / 神秘图案），
# 你批量下单、批量验收、打分评级，最后把最优秀的一关存成文件交货。

import os
from pathlib import Path
import requests

print("嘀——关卡策划部接单！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

# 交付文件固定落在脚本自己的文件夹里
OUT_FILE = Path(__file__).resolve().parent / "交付关卡.txt"

def ask(order):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=120,
    )
    return r.json()["choices"][0]["message"]["content"]

def extract(raw):
    "剥壳：AI 交稿包装五花八门——层层剥（同 step3 的健壮版）"
    text = raw
    if "```" in text:
        for block in text.split("```"):
            if any(c in block for c in "GHJ"):
                text = block
                break
    for q in ('"""', "'''"):
        if q in text:
            for part in text.split(q):
                if any(c in part for c in "GHJ"):
                    text = part
                    break
    result = []
    for line in text.splitlines():
        compact = line.strip().replace(" ", "")   # AI 爱用空格对齐图案——空格在地图里无意义，压掉
        if compact and set(compact) <= set(".GHJ") and len(compact) >= 8:
            result.append(compact)
    return result

def check_level(lines):
    "验证员三条硬标准：行数合理、行长一致、字符合法（列数自适应，不跟 AI 的数数能力较劲）"
    problems = []
    if not (4 <= len(lines) <= 8):
        problems.append(f"行数应在 4~8 行，实际 {len(lines)}")
    if lines:
        width = len(lines[0])
        if width < 8:
            problems.append(f"每行至少 8 个字符，实际 {width}")
        for i, line in enumerate(lines):
            if len(line) != width:
                problems.append(f"第 {i + 1} 行长度（{len(line)}）与第 1 行（{width}）不一致")
            bad = set(line) - set(".GHJ")
            if bad:
                problems.append(f"第 {i + 1} 行出现非法字符：{bad}")
    return (len(problems) == 0), problems

def grade(lines):
    "给关卡打分：垃圾密度和金垃圾占比越高越'刺激'"
    total = sum(1 for line in lines for ch in line if ch in "GHJ")
    gold = sum(1 for line in lines for ch in line if ch == "J")
    density = total / (len(lines) * len(lines[0])) if lines else 0
    return total, gold, density

# ── 客户的策划单：三个主题 ──
themes = [
    ("金字塔", "阵型像埃及金字塔，底宽顶尖，左右严格对称"),
    ("笑脸", "用垃圾块拼出一张笑脸：两个圆眼睛（J），一个大弧线嘴（G）"),
    ("神秘图案", "一个有创意的对称图案，主题自定（爱心？火箭？五角星？）"),
]

best = None                                    # 记录最佳关卡

for name, brief in themes:
    order = f"""你是游戏关卡设计师。设计主题关卡"{name}"：{brief}。
格式要求：
1. 5 到 7 行，每一行的字符数必须完全一样（这一点最重要！字符之间不要加空格）；
2. 只允许 4 种字符：. 、G、H、J；
3. 左右对称（笑脸的嘴可以是弧线形）；
4. 只输出地图字符串（三引号包裹），无解释。"""
    art = extract(ask(order))
    ok, problems = check_level(art)
    if not ok:                                 # 不合格自动退回一次
        art = extract(ask(f"你的设计未通过校验：{'; '.join(problems)}。请重新输出：5~7 行、每行等长、只含 . G H J。"))
        ok, problems = check_level(art)

    print(f"═ 主题关卡：{name}  体检：{'✅' if ok else '❌'}")
    for line in art:
        print("   ", line)
    if ok:
        total, gold, density = grade(art)
        print(f"   策划部评分：{total} 块垃圾（含金垃圾 {gold}），密度 {density:.0%}\n")
        if best is None or total > best[2]:    # 密度最高的当选
            best = (name, art, total)

# ── 交货：最佳关卡存档 ──
if best:
    name, art, _ = best
    OUT_FILE.write_text("\n".join(art), encoding="utf-8")
    print(f"🏆 本批最佳：{name} 关——已存入 {OUT_FILE.name}")
    print("（把它的内容按'三步上货指引'装进第二站游戏即可开打）")

# 🔍 小实验：
#    1. grade 只看了密度——设计更专业的评分：硬垃圾占比、金垃圾是否藏在深处（行号越上越深）
#    2. 策划追加需求："三个关卡难度要递增"——怎么改订单让 AI 配合？（提示：指定每关的 H 数量下限）
#    3. 终极思考：这一课你一直在"指挥 AI 干活 + 亲自验收"——
#       未来最值钱的能力，也许不是画得比 AI 好，而是比 AI 会下单、比 AI 会验收
