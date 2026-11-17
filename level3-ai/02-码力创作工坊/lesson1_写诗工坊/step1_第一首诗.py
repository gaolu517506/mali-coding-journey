# -*- coding: utf-8 -*-
# 第 1 课 · 第一首诗（步骤 1）：模糊订单 vs 精确订单
# 工坊开工第一课：让 AI 写诗。但你随口说"写首诗"，它就随口写——
# 本步骤同一主题下两份订单同台对比：模糊的 vs 精确的，差距一目了然。

import os
import requests

print("嘀——工坊开门！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(order):
    "把订单发给 AI，拿回成品"
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 订单 A：随手一句（大多数人第一次用 AI 的样子）
order_a = "写一首关于春天的诗。"

# 订单 B：像下订单一样说清楚（主题/格式/风格/字数四要素）
order_b = """写一首关于春天的小诗。
要求：一共四行，每行不超过 10 个字；
风格是孩子的口吻，天真一点；
第三行必须出现"小机器人"；
不要标题，不要解释，直接给诗。"""

print("═ 订单 A（模糊）：写一首关于春天的诗。")
print(ask(order_a), "\n")

print("═ 订单 B（精确）：主题 + 格式 + 风格 + 字数 + 特殊要求")
print(ask(order_b))

# 🔍 小实验：
#    1. 对比两首：哪首更"像你想要的"？差距来自哪——AI 读不到你心里的话，
#       订单写得多清楚，成品就有多准。这就是提示词工程的第一课
#    2. 把订单 B 里"第三行必须出现'小机器人'"改成你自己指定的词
#    3. 思考：订单 B 里的五条要求，哪条去掉后成品会崩得最厉害？（逐条删着试）
