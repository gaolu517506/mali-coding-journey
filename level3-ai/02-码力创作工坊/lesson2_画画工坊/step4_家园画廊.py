# -*- coding: utf-8 -*-
# 第 2 课 · 家园画廊（步骤 4）：三联画展览
# 毕业小作：为"重建家园"画三联画——日出开工、种下树苗、星空下的家。
# 程序自动搭一间"画廊"（网页），把三幅画挂上去，浏览器一开就是展览。

import os
from pathlib import Path
import requests

print("嘀——画廊布展中！")

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
    reply = reply[reply.find("<svg"):]
    return reply[:reply.find("</svg>") + 6]

# 三联画订单：同一个主题的三个时刻（构图提示词各不相同）
arts = {
    "画廊1-日出开工.svg": "清晨的工地：半圆形太阳从地平线升起（橙色），一台简单的吊车（几根矩形和线条拼成）。",
    "画廊2-种下树苗.svg": "种树时刻：绿色草地上一个小树苗（一根线条加一个椭圆树冠），旁边放一把小铲子（线条加矩形）。",
    "画廊3-星空下的家.svg": "夜晚的家：深蓝天空许多小圆点星星，中间一座亮着暖黄窗户的小房子。",
}

folder = Path(__file__).resolve().parent
for filename, subject in arts.items():
    art = paint(f"画一幅画：{subject}\n{BASE_RULES}")
    (folder / filename).write_text(art, encoding="utf-8")
    print(f"  ✅ {filename} 完成")

# 搭画廊：生成一个网页，把三幅画挂成一排
gallery = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>重建家园 · 三联画</title></head>
<body style="background:#11224a; color:white; font-family:sans-serif; text-align:center;">
  <h1>重建家园 · 码力与艾芯的三联画</h1>
  <p>AI 画家供货 · 策展人：你</p>
  <div style="display:flex; justify-content:center; gap:24px; flex-wrap:wrap;">
"""
for filename in arts:
    gallery += f'    <figure><img src="{filename}" width="400"><figcaption>{filename[3:-4]}</figcaption></figure>\n'
gallery += """  </div>
</body>
</html>
"""
(folder / "画廊.html").write_text(gallery, encoding="utf-8")
print("\n🖼 画廊已布展：画廊.html（浏览器打开它，三幅画一排挂好）")

# 🔍 小实验：
#    1. 给三联画加第四幅（比如"码力与艾芯的合影"）——订单和画名清单各加一行
#    2. 用文本编辑器打开 画廊.html——原来"网页"也只是代码（全体系一脉相承）
#    3. 策展人验收：三幅画风一致吗？太阳的画法统一吗？——AI 每次画都"重新想"，
#       所以细节不统一很正常。想统一怎么办？给订单加更死的约束（比如规定太阳的坐标）
