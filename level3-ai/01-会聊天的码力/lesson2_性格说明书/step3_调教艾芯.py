# -*- coding: utf-8 -*-
# 第 2 课 · 调教艾芯（步骤 3）：提示词工程 = 迭代，不是许愿
# 第一版说明书几乎不会完美。专业做法：测试 → 挑毛病 → 改说明书 → 再测。
# 本步骤用同一组测试题，现场走两轮迭代，看说明书怎么一版比一版好。

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

# 测试题固定不变（变量只有一个：说明书——科学实验要控制变量）
TESTS = ["用两句话介绍你自己", "我数学考了 59 分，有点难过", "讲个笑话"]

def test(system, label):
    "跑一组测试并打印——每版说明书都要过同一套题"
    print(f"═══ {label} ═══")
    for q in TESTS:
        print(f"你：{q}")
        print("艾芯：", ask(system, q), "\n")

# V1：随手写的一句话（大多数人的起点）
v1 = "你是一个帮助小学生学编程的 AI 助手。"
test(v1, "说明书 V1（随手写）")
# 挑毛病：太普通，没人设没温度；考 59 分那题大概只会说"加油"；笑话可能太长

# V2：针对毛病逐条改——加角色温度、加回应方式、加格式约束
v2 = """你是艾芯，小学生编程课的 AI 伙伴，性格温柔爱鼓励人。

【说话规矩】每次不超过三句话，以"嘀——"开头。
【回应规矩】孩子说成绩不好时：先共情（说出他的心情），再给一个小建议，最后给一句鼓励。
【讲笑话规矩】笑话不超过五行，讲完自己补一句"嘿嘿"。"""
test(v2, "说明书 V2（迭代后）")
# 对比 V1 和 V2 的三题答案——同一颗大脑，两份说明书写出两个艾芯

# 🔍 小实验：
#    1. 写出你的 V3：从 V2 的答案里再挑一个毛病（比如笑话还是不好笑？），只改对应那一段
#    2. 每版只改一两个地方——一次改五处，你就说不清是哪处起了作用（控制变量！）
#    3. 把 V1→V3 的每次改动记在一旁——这就是真实的提示词工程师工作日志
