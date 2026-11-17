# -*- coding: utf-8 -*-
# 第 3 课 · 毕业作品（步骤 4）：AI 供货，第二站开打
# 三站大结局：AI 设计关卡 → 验证员把关 → 存成图纸文件 →
# 按打印的"三步上货指引"装进第二站《太空垃圾清理战》——AI 正式成为游戏供货商。

import os
import requests

print("嘀——关卡工厂毕业典礼！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

# ── 验证员（上一课的手艺，直接复用）──
def check_level(lines):
    "验证员三条硬标准：行数合理、行长一致、字符合法（列数由游戏自适应，不苛求 AI 数字符）"
    problems = []
    if not (4 <= len(lines) <= 8):
        problems.append(f"行数应在 4~8 行，实际 {len(lines)}")
    if lines:
        width = len(lines[0])
        if width < 8:
            problems.append(f"每行至少 8 个字符，实际 {width}")
        for i, line in enumerate(lines):
            if len(line) != width:
                problems.append(f"第 {i + 1} 行长度（{len(line)}）与第 1 行（{width}）不一致——游戏按第一行算列数")
            bad = set(line) - set(".GHJ")
            if bad:
                problems.append(f"第 {i + 1} 行出现非法字符：{bad}")
    return (len(problems) == 0), problems

def ask(order):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=180,
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

# ── 下单：第 4 关（比游戏里三关更难的新关卡）──
order = """你是游戏关卡设计师。为"太空垃圾清理战"设计第 4 关（难度高于前三关）。
格式要求：
1. 5 到 7 行，每一行的字符数必须完全一样（这一点最重要！字符之间不要加空格）；
2. 只允许 4 种字符：. 、G、H、J；
3. 第一、二行以 H（硬垃圾）为主，中部穿插 J（金垃圾）奖励高手；
4. 阵型左右对称；
5. 只输出地图字符串（用三引号 ''' 包起来），不要任何解释。"""

art = extract(ask(order))
ok, problems = check_level(art)

retry = 0
while not ok and retry < 2:
    retry += 1
    art = extract(ask(f"""你设计的关卡未通过校验：
{chr(10).join(problems)}

请重新输出：5~7 行、每行等长、只含 . G H J，三引号包裹，无解释。"""))
    ok, problems = check_level(art)

if not ok:
    print("❌ AI 多次交稿仍不合格——毕业彩蛋：连 AI 也需要人类兜底，重跑一次吧")
else:
    print("═ 第 4 关设计稿（已通过验证员体检）═\n")
    for line in art:
        print("   ", line)

    # ── 存成图纸文件：这就是给第二站的"货" ──
    map_text = "\n".join(art)
    print(f"""
═ 三步上货指引（把 AI 的关卡装进第二站游戏）═

1. 打开第二站文件：level2-python/02-太空垃圾清理战/lesson5_轨道疏通/challenge_关卡设计师.py
2. 把文件里的 LEVEL_MAP 四行字符串，换成下面这些（AI 刚设计的）：

LEVEL_MAP = [
'''{map_text}'''.splitlines(),
]

   （就是删旧的四行引号字符串，粘上这一段）
3. 运行那个文件——你打的正是 AI 设计的第 4 关！
""")

    # ── 毕业统计：这张关卡的数值 ──
    total, score = 0, 0
    value = {"G": 10, "H": 30, "J": 50}
    for line in art:
        for ch in line:
            if ch in value:
                total += 1
                score += value[ch]
    print(f"关卡数值：{total} 块垃圾，通关满分 {score} 分——去打打看，能给这个设计打几分？")

# 🔍 毕业检查单（三站大结局，全部打勾你就是"全栈小工程师"）：
#    □ 第一站手艺：turtle 画出过五角星和星空（航线与画笔）
#    □ 第二站手艺：pygame 打通过三关（主循环与碰撞）
#    □ 第三站手艺：指挥 AI 写诗、画画、设计关卡（订单与验证）
#    □ 体系彩蛋：你用第一站学的提示词守则管住 AI，用第二站的游戏验收它的货
#    码力完成了任务，向太空发出信号："回家吧。"——而你，学会了让它回家的全部技能。
