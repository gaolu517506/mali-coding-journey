# -*- coding: utf-8 -*-
# 第 2 课 · 挑战任务：双胞胎艾芯
# 同一颗大脑，两份相反的说明书——热情鼓励派 vs 严厉教练派。
# 同一个问题分别问两个"艾芯"，看说明书能把模型调教出多大的差别。
# 最后回答那个真正的问题：哪个对你更有用？

import os
import requests

print("嘀——双胞胎艾芯上线！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(system, question):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 双胞胎的两份说明书
SWEET = """你是"暖芯"，热情鼓励派 AI 伙伴。
孩子说什么你都能找到值得夸的地方，语气温暖，每次不超过三句话，
先共情，再鼓励，坚信每个孩子都会越来越好。"""

STRICT = """你是"严芯"，严厉教练派 AI 导师。
你相信对孩子真正的好是指出问题。回答直接、具体、不绕弯，
每次先明确指出孩子的问题在哪，再给一条立刻能做的改进动作，
不说空话夸奖，但结尾永远留一句"我相信你能做到"。"""

# 三个真实难题，分别问双胞胎
questions = [
    "我数学考了 59 分，怎么办？",
    "我学 Python 两周了还写不对循环，是不是没天赋？",
    "帮我决定：周末学画画还是继续练编程？",
]

for q in questions:
    print(f"═ 你：{q}")
    print("暖芯：", ask(SWEET, q))
    print("严芯：", ask(STRICT, q), "\n")

# 🔍 实验报告：
#    1. 同一颗大脑，两个回答的"价值观"差多远？——说明书就是价值观的开关
#    2. 你更喜欢哪个？答案没有对错——提示词设计没有标准答案，只有"适合谁、用来干什么"
#    3. 终极挑战：造"混合芯"——先共情两句，再指出一条问题，最后给一个动作。
#       写出它的说明书并测试（提示：把两份说明书的优点各抄一段）
