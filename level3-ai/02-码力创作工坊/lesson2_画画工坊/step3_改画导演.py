# -*- coding: utf-8 -*-
# 第 2 课 · 改画导演（步骤 3）：提意见，不改代码
# 第一稿很少完美。但导演不碰代码——导演提意见，画家重画。
# 本步骤两幅画对比：初稿 → 带意见重画（换色 + 加元素）。

import os
from pathlib import Path
import requests

print("嘀——导演上岗！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

BASE_RULES = """硬性要求：
1. 只输出 SVG 代码，从 <svg 开始到 </svg> 结束，不要任何解释文字；
2. 画布 400×300；
3. 只许用：rect、circle、ellipse、line、polygon、text；
4. 只许纯色填充，禁止渐变/阴影/高光。"""

def paint(order):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=120,
    )
    reply = r.json()["choices"][0]["message"]["content"]
    reply = reply[reply.find("<svg"):]              # 剥壳：只留 SVG 本体
    return reply[:reply.find("</svg>") + 6]

def save(art, filename):
    path = Path(__file__).resolve().parent / filename
    path.write_text(art, encoding="utf-8")
    print(f"  已存：{filename}")

# ── 初稿：夜景小屋 ──
art_v1 = paint(f"""画一幅画：夜晚的小木屋，深蓝天空挂着一轮满月。
{BASE_RULES}""")
print("初稿完成")
save(art_v1, "画作-初稿.svg")

# ── 改稿：带着初稿提意见，重画 ──
# 导演意见：太冷清——把夜色调暖一点，加两扇亮灯的窗和几颗星星
art_v2 = paint(f"""这是之前的画：
{art_v1}

在它的基础上修改重画：
1. 天空从深蓝改成偏紫的夜色，月亮旁加 5 颗小星星（小圆点）；
2. 木屋加两扇亮着暖黄色光的窗户（用黄色矩形表示灯光）；
3. 其余构图保持不变。
{BASE_RULES}""")
print("改稿完成（暖夜版）")
save(art_v2, "画作-改稿.svg")

print("\n两张画都在脚本文件夹里：浏览器分别打开，对比初稿和改稿。")
print("导演全程没写一行 SVG——只写了意见。这就是人机协作里的'导演位'。")

# 🔍 小实验：
#    1. 当一回真正的导演：写第三轮意见（比如"加一只萤火虫""树呢？"），
#       把 art_v2 嵌进订单再改一版（f-string 嵌 {art_v2}，老手艺）
#    2. 翻车预案：如果 AI 返回里找不到 <svg（剥壳会出错），说明它没按格式交货——
#       重跑一次就好。顺便想想：程序怎么自动发现这种"不交货"？（下一课揭晓）
#    3. 思考：改稿订单里为什么要附上初稿代码？不附行不行？（试试看效果差多少）
