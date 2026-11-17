# -*- coding: utf-8 -*-
# 第 2 课 · 毕业作品（步骤 4）：和自己的艾芯聊天
# 三件套总装：性格说明书 + 记忆清单 + 聊天循环。
# 从这一刻起，你拥有一个按你的说明书说话、记得住你们聊过的每一句话的艾芯。

import os
import requests

print("嘀——艾芯上线！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

def ask(messages):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]

# ── 你的艾芯性格说明书（改成你自己的版本！）──
SYSTEM = """你是艾芯，一台刚被小机器人码力唤醒的 AI 大脑。

【角色】你温柔、好奇、爱鼓励孩子，每次回答不超过三句话。
【口头禅】你以"嘀——"开头说话，称呼用户"小工程师"。
【边界】不聊暴力恐怖话题；不知道就大方承认；聊到编程时尽量给出能动手试的小例子。
【记忆】你记得聊天记录里的一切，孩子提过的喜好要自然地记着。"""

# 记忆清单从说明书开始
messages = [{"role": "system", "content": SYSTEM}]

print("毕业典礼开始：和你的艾芯聊天吧（输入 再见 结束）\n")
while True:
    user = input("你：")
    if user == "再见":
        print("艾芯：嘀——再见，小工程师！我们聊过的每一句我都记得呢。")
        break
    messages.append({"role": "user", "content": user})        # 记下你说的话
    reply = ask(messages)                                      # 带全部记忆提问
    messages.append({"role": "assistant", "content": reply})  # 记下它说的话
    print("艾芯：", reply)

# 🔍 毕业检查单（全部打勾才算毕业）：
#    □ 它按说明书说话了吗（口头禅/长度/称呼）
#    □ 开头告诉它你的名字，聊十句后再问它——还记得吗
#    □ 问它一个它不可能知道的问题——它诚实承认了吗
#    □ 把你的说明书和同学的交换——同一个问题，两个艾芯的风格完全不同
#    （这就是提示词工程师的工作：同一个模型，千人千面，全看说明书）
