# -*- coding: utf-8 -*-
# 第 1 课 · 第一次通话（步骤 2）：唤醒真艾芯
# 规则版艾芯只会查表。现在唤醒真正的大模型艾芯——
# 你的话将穿过网络抵达千里之外的大模型，再把回话带回来。

import os                       # 用来读取环境变量（key 藏在那里）
import requests                 # 用来发网络请求的"快递员"

print("嘀——艾芯上线！")

# ── 配置区：默认智谱 GLM（glm-4-flash 免费）；换别家只改这三行 ──
API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")   # 从环境变量读 key，绝不写进代码
MODEL = "glm-4-flash"
# 换别家？  DeepSeek: "https://api.deepseek.com" + DEEPSEEK_API_KEY + "deepseek-chat"
#          通　　义: "https://dashscope.aliyuncs.com/compatible-mode/v1" + DASHSCOPE_API_KEY + "qwen-plus"

# 对话清单：一条消息 = {角色: 谁说的, 内容: 说了什么}
messages = [
    {"role": "user", "content": "你好艾芯！请用一句话介绍你自己。"},
]

# 发请求：像寄一封挂号信——地址、门票(key)、信件(对话清单)
r = requests.post(
    API_BASE + "/chat/completions",              # 收件地址
    headers={"Authorization": "Bearer " + API_KEY},   # 门票：证明你是谁
    json={"model": MODEL, "messages": messages},      # 信件：用哪个模型 + 说什么
    timeout=60,                                  # 等回信最多 60 秒
)

answer = r.json()["choices"][0]["message"]["content"]  # 拆回信
print("艾芯：", answer)

# 🔍 小实验：
#    1. 把 content 换成任何问题试试——"3 乘 7 等于几？"（离线版答不上的，它秒答）
#    2. 在 print(answer) 前加一行 print(r.json())——看看完整的回信里还藏着什么
#       （模型名、用量 usage……回信比你看到的多）
#    3. 把 key 改成错的（比如 API_KEY = "abc"）再跑——看程序怎么告诉你门票无效
