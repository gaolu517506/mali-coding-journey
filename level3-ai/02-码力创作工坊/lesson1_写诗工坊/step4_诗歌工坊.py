# -*- coding: utf-8 -*-
# 第 1 课 · 诗歌工坊（步骤 4）：AI 供货，人当主编
# 单件生产升级为流水线：一次让 AI 交三首不同的稿，
# 程序自动拆开编号，你来当主编——选一首"刊发"，写一句推荐语。

import os
import requests

print("嘀——工坊开门！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(order):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 一张订单要三件货：要求 AI 用固定分隔符隔开（方便程序拆分！）
order = """你是童诗供货商。写三首风格不同的小诗，主题都是"小机器人的家"：
第 1 首要温暖，第 2 首要好笑，第 3 首要有一点点感动。
每首四行、每行不超过 10 个字。
三首之间用一行"===="隔开。除三首诗之外不要输出任何别的文字。"""

print("向供货商下单……\n")
raw = ask(order)

# 拆货：按约定好的分隔符切开（AI 守不守约，拆一下就知道）
poems = [p.strip() for p in raw.split("====") if p.strip()]

if len(poems) < 3:
    print("⚠️ 供货商没按格式交货（只拆出", len(poems), "首）——这正是下一课'验证员'存在的意义")
else:
    for i, poem in enumerate(poems):
        print(f"═ 投稿 {i + 1} 号")
        print(poem, "\n")

    choice = input("主编，刊发几号？（输入 1/2/3）：")
    note = input("写一句推荐语：")
    picked = poems[int(choice) - 1] if choice in "123" else poems[0]

    print("\n════════ 本期创刊号 · 主编选定 ════════")
    print(picked)
    print(f"—— 主编推荐语：{note}")
    print("════════════════════════════════")

# 🔍 小实验：
#    1. 三首里没一首满意？合格主编的做法：不是自己憋，是带着意见重新下单
#    2. 把分隔符"===="换成"###"——记得 ask 的订单和 split 两处都要改（约定要双方一致）
#    3. 思考：为什么让 AI 一次交三首，比连下三次单好？（一次货更"多样"，还省两次请求）
