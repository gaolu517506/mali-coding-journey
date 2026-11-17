# -*- coding: utf-8 -*-
# 第 2 课 · 挑战任务：给码力画朋友
# 用闭集约束做真正的角色设计：给艾芯设计一个新伙伴（AI 大脑二号机？）。
# 设计公式 = 词汇表内的形状 + 三处可辨认特征 + 一个名字。

import os
from pathlib import Path
import requests

print("嘀——角色设计部开工！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

ART_FILE = Path(__file__).resolve().parent / "新角色设计稿.svg"

def paint(order):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=120,
    )
    reply = r.json()["choices"][0]["message"]["content"]
    reply = reply[reply.find("<svg"):]
    return reply[:reply.find("</svg>") + 6]

# ── 你的角色设定（改这三行！）──
ROLE_NAME = "芯豆"                       # 名字：也要像"码力/艾芯"一样有巧思
ROLE_TRAITS = "头上一根小小的天线（一条竖线加一个小圆），胸口一颗绿色的爱心（两个圆加一个三角形拼成），圆滚滚的身体"
ROLE_COLOR = "薄荷绿 body、白色脸、粉色爱心"

order = f"""你是角色设计师。请画一个原创小机器人的正面全身像。
角色名：{ROLE_NAME}。
外形特征：{ROLE_TRAITS}。
配色：{ROLE_COLOR}。背景纯白色。
硬性要求：
1. 只输出 SVG 代码，从 <svg 开始到 </svg> 结束，不要任何解释；
2. 画布 300×400，角色居中、占画面高度约一半；
3. 只许用：rect、circle、ellipse、line、polygon、text；
4. 只许纯色填充，禁止渐变/阴影/高光；
5. 在角色脚边用 <text> 写上它的名字"{ROLE_NAME}"。"""

print(f"设计部下单：{ROLE_NAME}……\n")
art = paint(order)
ART_FILE.write_text(art, encoding="utf-8")
print(f"✅ 设计稿已存：{ART_FILE.name}（浏览器打开验收）\n")

# ── 设计师验收清单 ──
print("═ 角色设计师验收单 ═")
print("□ 三处特征都在吗？（天线 / 爱心 / 圆身体）")
print("□ 配色对吗？")
print("□ 名字写对了吗？（AI 写中文字偶尔会写错字——正好抓它一个现行）")
print("□ 有没有偷偷超纲（渐变/阴影）？")
print("□ 全部打勾 → 角色定稿！想想它的性格（下一站提示词课的手艺）")

# 🔍 小实验：
#    1. 换一个你自己的角色名和三处特征，重新生成——三处特征是"可辨认"的最低配，
#       太少认不出，太多 AI 会画丢
#    2. 复杂度实验：把特征改成五处，看 AI 会漏画几处——
#       结论：订单越复杂，验收越重要（AI 不是不会画，是会画丢）
#    3. 给码力家族画全家福：把码力（黄）、艾芯（蓝）、{ROLE_NAME}（绿）
#       写进同一张订单——试试 AI 的"群像"功力
