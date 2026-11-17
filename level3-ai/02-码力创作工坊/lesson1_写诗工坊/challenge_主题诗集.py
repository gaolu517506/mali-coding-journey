# -*- coding: utf-8 -*-
# 第 1 课 · 挑战任务：主题诗集
# 一首诗不过瘾——出一本迷你诗集：定一个总主题，让 AI 供四首"栏目诗"，
# 程序排版成目录 + 正文，你就是这本诗集的主编兼出版人。

import os
from pathlib import Path               # pathlib：更现代的文件路径工具
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

# 诗集总主题（改成你自己的！）
TOPIC = "地球重新变绿"

# 出版文件：固定落在脚本自己的文件夹里（主题不进文件名，写进扉页）
BOOK_FILE = Path(__file__).resolve().parent / "我的诗集.txt"

# 四个栏目：同一主题的四个角度
sections = ["清晨", "劳作", "伙伴", "夜晚"]

poems = {}
for section in sections:
    order = f"""写一首四行小诗。
主题：{TOPIC}——{section}。
要求：孩子的口吻，每行不超过 10 个字，第 {sections.index(section) + 1} 首里要出现"码力"或"艾芯"。
只输出诗，不要标题和解释。"""
    poems[section] = ask(order)
    print(f"· 《{section}》已收稿")

# 出版：扉页 + 目录 + 正文 + 版权页（写进文本文件，这就是你的"书"）
book = f"《{TOPIC}》—— 一本人机合著的小诗集\n"
book += "═" * 30 + "\n\n"
book += "目 录\n"
for i, section in enumerate(sections):
    book += f"  {i + 1}. {section}\n"
book += "\n" + "═" * 30 + "\n\n"
for section in sections:
    book += f"【{section}】\n{poems[section]}\n\n"
book += "═" * 30 + "\n"
book += "AI 供货 · 主编：你\n"

BOOK_FILE.write_text(book, encoding="utf-8")
print(f"\n📖 诗集已出版：{BOOK_FILE.name}（在脚本文件夹里，用记事本打开看看；下一课请 AI 画封面）")

# 🔍 小实验：
#    1. 四个栏目就是四个角度——换成你的栏目（春/夏/秋/冬？出发/迷路/朋友/回家？）
#    2. 数一数：出这本书一共发了几次请求？每次都在花 token——好主编会算成本
#    3. 出版进阶：让 AI 再写一段 50 字的"编者的话"放进目录后面
