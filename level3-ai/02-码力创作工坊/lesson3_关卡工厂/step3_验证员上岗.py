# -*- coding: utf-8 -*-
# 第 3 课 · 验证员上岗（步骤 3）：AI 会犯错，验证是程序员的工作
# 上一课看到 AI 交稿"大概没问题"。工程上"大概"不够——
# 专业做法：写一个验证员程序，AI 每次交稿都过一遍机器体检；
# 体检不过，就把报错原样发回给 AI，让它自己修——这才是真实的人机协作。

import os
import requests

print("嘀——验证员上岗！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

# ── 验证员：机器体检，一个标准都不放行 ──
def check_level(lines, want_rows, want_cols):
    "按三条硬标准校验关卡，返回 (是否合格, 问题清单)"
    problems = []
    if len(lines) != want_rows:
        problems.append(f"行数应为 {want_rows}，实际 {len(lines)}")
    for i, line in enumerate(lines):
        if len(line) != want_cols:
            problems.append(f"第 {i + 1} 行长度应为 {want_cols}，实际 {len(line)}")
        bad = set(line) - set(".GHJ")
        if bad:
            problems.append(f"第 {i + 1} 行出现非法字符：{bad}")
    return (len(problems) == 0), problems

# ── 先拿一张"故意写坏"的地图试刀：验证员抓得住吗？──
print("═ 试刀：故意写坏的地图 ═")
bad_map = [
    "..JJJJ....",      # 10 个字符（要求 12）
    ".GGGGGGGG.XX",    # XX 是非法字符
    "HH.HH",
]
ok, problems = check_level(bad_map, want_rows=5, want_cols=12)
print("合格：" , "✅" if ok else "❌")
for p in problems:
    print("   ·", p)

# ── 正戏：AI 交稿 → 体检 → 不过就把报错发回去让它修 ──
print("\n═ 正戏：AI 交稿 + 验证员把关 ═")

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
    "剥壳：AI 交稿包装五花八门（```代码块 / '''或\"\"\"三引号 / 变量赋值）——层层剥"
    text = raw
    if "```" in text:                          # 第一层：Markdown 代码块
        for block in text.split("```"):
            if any(c in block for c in "GHJ"):
                text = block
                break
    for q in ('"""', "'''"):                   # 第二层：三引号（单/双）
        if q in text:
            for part in text.split(q):
                if any(c in part for c in "GHJ"):
                    text = part
                    break
    # 终极兜底：不管包装成什么样，只保留"纯地图行"（全部由 . G H J 组成）
    result = []
    for line in text.splitlines():
        compact = line.strip().replace(" ", "")   # AI 爱用空格对齐图案——空格在地图里无意义，压掉
        if compact and set(compact) <= set(".GHJ") and len(compact) >= 8:
            result.append(compact)
    return result

ORDER = """你是游戏关卡设计师。为打砖块游戏设计关卡字符地图。
硬性要求：
1. 恰好 5 行，每行恰好 12 个字符；
2. 只允许 4 种字符（字符之间不要加空格）：. 、G、H、J；
3. 第一行以 J 为主，最后一行全是 . ；
4. 阵型左右对称，像金字塔；
5. 只输出 5 行字符串（用三引号 ''' 包起来），不要任何解释。"""

art = extract(ask(ORDER))
ok, problems = check_level(art, 5, 12)
print("第一次交稿体检：", "✅ 直接合格" if ok else "❌ 有问题")

retry = 0
while not ok and retry < 2:                      # 最多退回重修 2 次
    retry += 1
    print(f"\n── 把体检报告发回给 AI，第 {retry} 次退回重修 ──")
    feedback = "\n".join(problems)
    art = extract(ask(f"""你之前设计的关卡没有通过格式校验，问题如下：
{feedback}

原稿：
'''{chr(10).join(art)}'''

请严格按要求重新输出：恰好 5 行、每行恰好 12 个字符、只含 . G H J、
只输出三引号包裹的 5 行字符串，不要解释。"""))
    ok, problems = check_level(art, 5, 12)
    print("重修后体检：", "✅ 合格" if ok else "❌ 仍有问题")

print("\n═ 最终交稿 ═")
for line in art:
    print("   ", line)
print("\n结论：AI 负责「想」，验证员负责「查」，不合格就退回——",
      f"本次共退回 {retry} 次。" if retry else "本次一次过！")

# 🔍 小实验：
#    1. 把 retry 上限改成 0 再跑——AI 交稿偶尔真会不合格，这就是为什么要验证员
#    2. 给验证员加第四条标准：金垃圾 J 的数量不能超过 4 个（防止 AI 设计"金币雨"）
#    3. 思考：为什么"AI + 验证员"比"只有 AI"专业？（人也一样——所以代码要测试）
