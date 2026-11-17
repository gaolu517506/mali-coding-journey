# -*- coding: utf-8 -*-
# 第 1 课 · 订单模板（步骤 2）：结构化提示词四件套
# 零散的要求容易漏。专业提示词是一张结构化订单，四件套：
#   ① 角色（你是谁）② 任务（做什么）③ 约束（守什么规矩）④ 示例（照这个样子）
# 本步骤把订单模板化——以后写诗改两行就能用。

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

# ── 订单模板：四件套各占一段（三引号字符串，会换行）──
order = """【角色】你是一位给孩子写诗的诗人，擅长把科技元素写进童趣的画面里。
【任务】写一首关于"小机器人在星空下画画"的四行小诗。
【约束】每行不超过 10 个字；不押韵也可以，但读起来要顺口；不要标题和解释。
【示例】参考这种味道（不要照抄）：
  铅笔换成光线
  画布铺满夜晚
  一颗星星探出头
  说：这里要有光"""

print("═ 订单（四件套）")
print(order, "\n")
print("═ 成品")
print(ask(order))

# 🔍 小实验：
#    1. 只改【任务】里的主题（比如"小机器人在垃圾山上种花"），四件套结构不动——
#       模板的意义：换货不换单
#    2. 把【示例】整段删掉再跑——味道是不是变了？示例是"定味器"
#    3. 【约束】里再加一条你自己想的规矩（比如"第二行必须有个问号"），验收 AI 守没守
