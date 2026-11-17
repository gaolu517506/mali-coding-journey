# -*- coding: utf-8 -*-
# 第 1 课 · 导演的三个回合（步骤 3）：迭代出好作品
# 人机协作的铁律：人是导演，AI 是剧组——第一遍很少一条过。
# 导演的工作是看成品、提意见、让剧组重拍。本步骤同一首诗迭代三个回合。

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

# ── 回合一：初稿 ──
order_1 = """写一首四行小诗，主题是"重建家园"，孩子的口吻，每行不超过 10 个字。"""
draft_1 = ask(order_1)
print("═ 回合一（初稿订单）")
print(draft_1, "\n")

# ── 回合二：导演提意见，剧组重拍 ──
# 导演的看法：第一稿太"口号"，缺一个具体的画面
order_2 = f"""这是一首诗的初稿：
{draft_1}
我的意见：太空洞，像喊口号。请重写：保留主题"重建家园"，
但必须出现一个具体的画面（比如种下第一棵树苗），
仍然四行、每行不超过 10 个字、孩子的口吻。"""
draft_2 = ask(order_2)
print("═ 回合二（提意见重拍）")
print(draft_2, "\n")

# ── 回合三：再精修一处 ──
# 导演的看法：画面有了，结尾想留一个"望向天空"的钩子
order_3 = f"""这是第二稿：
{draft_2}
最后修一处：把最后一行改成一个望向天空/星空的画面，
其余三行保持不变。只输出最终四行。"""
draft_3 = ask(order_3)
print("═ 回合三（精修一处）")
print(draft_3)

# 🔍 导演笔记（本步骤的灵魂）：
#    1. 三个回合用的是同一个 f-string 技巧：把上一稿嵌进新订单（{draft_1}）——
#       "带着上一稿提意见"，AI 才知道改什么
#    2. 每回合只提一个主要意见——一次提五条，剧组会改丢三条
#    3. 你的回合：对第三稿再提一条意见，写你的"回合四"
