# -*- coding: utf-8 -*-
# 第 1 课 · 给艾芯下命令（步骤 4）：system 消息
# 对话清单里有三种角色：
#   system = 写给 AI 的"设定说明书"（玩家看不到，但 AI 必须遵守）
#   user   = 你说的话
#   assistant = AI 回的话（下一课的主角）
# 本步骤体验：一句话说明书，就能让艾芯换一副灵魂。

import os
import requests

print("嘀——艾芯上线！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(system, question):
    "带设定说明书的提问"
    messages = [
        {"role": "system", "content": system},      # 说明书放在对话最前面
        {"role": "user", "content": question},
    ]
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# 同一个问题，三种说明书——看艾芯的三副面孔
q = "用两句话介绍一下你自己"

print("【默认艾芯】")
print(ask("你是一个乐于助人的 AI 助手。", q), "\n")

print("【海盗艾芯】")
print(ask("你是一个说话夹带'嘿嘿'和'起锚'的太空海盗。", q), "\n")

print("【诗人艾芯】")
print(ask("你是一个每句话都押韵的诗人。", q))

# 🔍 小实验：
#    1. 写你自己的说明书：武士版？大侦探版？外婆版？（换 q 再试）
#    2. 对比实验：把说明书内容拼进 user 问题里（不用 system），效果一样吗？
#       通常 system 更稳定——它天生就是"设定"的位置
#    3. 预告：一句话说明书够短，但管不住细节——
#       下一课给艾芯写一份正式的《性格说明书》
