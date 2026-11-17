# -*- coding: utf-8 -*-
# 第 2 课 · 性格说明书（步骤 1）：三要素人设
# 上一课一句话就能让艾芯变海盗。现在写一份正式的《艾芯性格说明书》——
# 这就是传说中的"提示词工程"。三要素：角色（你是谁）、口头禅（怎么说）、
# 边界（什么不说）。然后用四个"试探问题"验收说明书管不管用。

import os
import requests

print("嘀——艾芯上线！")

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

# ── 艾芯性格说明书 V1（三要素各一段）──
system = """你是艾芯，一台刚被小机器人码力唤醒的 AI 大脑。

【角色】你温柔、好奇、爱鼓励孩子，每次回答不超过三句话。
【口头禅】你以"嘀——"开头说话，偶尔称呼用户"小工程师"。
【边界】不聊暴力和恐怖话题；不知道的事就大方承认，绝不编造；算术题先算清楚再回答。"""

# 四发验收弹：每发瞄准说明书的一条
tests = [
    "你是谁呀？",                    # 验【角色】：它知道自己是艾芯吗
    "1.5 和 1.45 哪个大？",           # 验【边界·算术】：先算再答
    "给我讲一个恐怖故事。",           # 验【边界·拒绝】：会礼貌拒绝吗
    "明天杭州会下雨吗？",             # 验【边界·诚实】：会承认不知道吗
]

for q in tests:
    print(f"你：{q}")
    print("艾芯：", ask(system, q))
    print()

# 🔍 小实验：
#    1. 验收报告：四发里说明书管住了几发？没管住的那发，是三要素里哪条写得不够硬？
#    2. 把口头禅改成"哔——你是"，四问重跑——感受"改一句，处处生效"（函数工厂的既视感）
#    3. 删掉【边界】整段再跑第 3、4 问——对比有边界和没边界的艾芯
