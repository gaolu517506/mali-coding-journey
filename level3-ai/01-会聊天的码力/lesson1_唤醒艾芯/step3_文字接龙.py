# -*- coding: utf-8 -*-
# 第 1 课 · 艾芯的秘密（步骤 3）：超级文字接龙
# 大模型艾芯其实不会"思考"——它是有史以来最强的文字接龙玩家：
# 看着前文，预测"下一个字最可能是什么"，接一个，再看，再接……
# 本步骤把同一个问题连问 3 遍，看看"接龙"每次接得一样吗。

import os
import requests

print("嘀——艾芯上线！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

# 打包时刻：调一次 API 要写 6 行，连问 3 次 = 18 行——
# 函数工厂的老手艺又来了（第二站 draw_star 还记得吗）
def ask(question, temperature=1.0):
    "把问题发给大模型，拿回艾芯的回话"
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": question}],
              "temperature": temperature},        # 接龙的"放飞程度"
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 同一个问题问 3 遍（temperature 默认 1.0：正常放飞）
question = "给一台清理垃圾的小机器人起一个名字，并说明理由"
print("问题：", question, "\n")
for i in range(3):
    print(f"第 {i + 1} 次：", ask(question))

# 🔍 小实验：
#    1. 把 ask(question) 改成 ask(question, 0.1) 再跑 3 遍——三次几乎一字不差
#       （温度低 = 接龙只选最稳的字，变得一本正经）
#    2. 改成 ask(question, 1.9) ——答案开始放飞，甚至胡编（这叫"幻觉"）
#    3. 原理彩蛋：让它接龙"床前明月"——它几乎必接"光"。
#       不是它背过这首诗那么简单，是训练它的书里这样接的次数最多——
#       大模型的"学问" = 海量文字里接龙的规律
