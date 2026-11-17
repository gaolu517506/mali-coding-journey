# -*- coding: utf-8 -*-
# 第 2 课 · 记忆的秘密（步骤 2）：messages 列表
# 艾芯怎么"记得"你上一句说了什么？答案会让你吃惊：
# 它根本没有记忆——每次通话，我们都把全部聊天记录重新寄一遍！

import os
import requests

print("嘀——艾芯上线！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

# 这次 ask 收整个对话清单（不再只收一句话）
def ask(messages):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 记忆清单：从说明书开始，每说一句就追加一条
messages = [
    {"role": "system", "content": "你是艾芯，说话简短温柔，以'嘀——'开头。"},
]

# 第一轮：告诉它一个秘密
messages.append({"role": "user", "content": "我叫小鹿，我最喜欢的课是编程课。"})
reply = ask(messages)
messages.append({"role": "assistant", "content": reply})   # ⚠️ 艾芯的回话也要记进清单
print("第一轮 艾芯：", reply)

# 第二轮：考考它记不记得（把整个清单再寄一遍，它就"记得"了）
messages.append({"role": "user", "content": "我叫什么？最喜欢的课是什么？"})
reply = ask(messages)
messages.append({"role": "assistant", "content": reply})
print("第二轮 艾芯：", reply)

# 第三轮：失忆实验——寄一份不带任何历史的新清单，问同样的问题
fresh = [{"role": "user", "content": "我叫什么？最喜欢的课是什么？"}]
print("失忆版 艾芯：", ask(fresh))

# 🔍 小实验：
#    1. 失忆版的回答 vs 第二轮——同一颗大脑，带不带历史，判若两"芯"
#    2. 把第二轮那行 messages.append({"role": "assistant", ...}) 注释掉再跑——
#       艾芯连自己说过的话都会忘（assistant 消息也是记忆的一部分）
#    3. 想想：聊得越久，清单越长，寄的信越重——这就是 AI 按"字数"（token）计费的原因，
#       也是为什么很多 AI 只记得住最近的一小段聊天记录
