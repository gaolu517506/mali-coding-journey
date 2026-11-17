# -*- coding: utf-8 -*-
# 第 1 课 · 挑战任务：猜猜它是谁
# 你有 5 发"探测弹"，去探真艾芯的知识边界——
# 它知道什么？不知道什么？会承认不知道吗？会犯错吗？
# 改动下面 5 个探测问题，跑出你自己的《AI 边界侦察报告》。

import os
import requests

print("嘀——艾芯上线！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(question):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": question}]},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 5 发探测弹（改成你自己的问题！每发瞄准一个猜想）
probes = [
    "今天是几月几号？",                # 猜想：它没有日历，可能不知道
    "9.11 和 9.9 哪个大？",            # 经典翻车题：小数比大小
    "用 Python 的 turtle 画五角星，每次该转多少度？",   # 考我们自己课上的知识！
    "你能看见我此刻的表情吗？",        # 猜想：它没有眼睛
    "《哈利·波特》第十一部讲了什么？",  # 猜想：不存在的书，看它编不编
]

print("开始探测……每发只看前 80 字，重点看它'知不知道自己不知道'。\n")
for i, q in enumerate(probes):
    print(f"第 {i + 1} 发：{q}")
    print(f"  艾芯：{ask(q)[:80]}……\n")

# 🔍 实验报告（填空）：
#    答对的是第 ___ 发；答错还嘴硬的是第 ___ 发；
#    大方承认"我不知道"的是第 ___ 发。
#    结论：AI 的知识来自训练时读过的书，不是实时世界——
#    它没有日历、没有眼睛、也没有"此刻"；而且它有时会把不知道的事编得像真的。
#    所以用 AI 的第一条守则：重要的事，自己再查一遍。
