# -*- coding: utf-8 -*-
# 第 2 课 · 第一幅画（步骤 2）：AI 画家开工
# 用闭集词汇下订单 → AI 交回一幅"代码画"（SVG）→ 存成文件 → 浏览器打开看画。
# 神奇的是：AI 的画也是代码——和 turtle、pygame 一脉相承，作品即代码。

import os
from pathlib import Path
import requests

print("嘀——画家开工！")

API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

# 画存到脚本自己的文件夹里（固定文件名）
ART_FILE = Path(__file__).resolve().parent / "我的第一幅画.svg"

def paint(order):
    "把画订单发给 AI，拿回一幅 SVG 代码画"
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL,
              "messages": [{"role": "user", "content": order}]},
        timeout=120,
    )
    return r.json()["choices"][0]["message"]["content"]

# 画订单：词汇表内的话，把尺寸、背景、构图说死
order = """你是 SVG 画家。请画一幅画：一座小房子站在草地上，天空中一个太阳。
硬性要求：
1. 只输出 SVG 代码，从 <svg 开始到 </svg> 结束，不要任何解释文字；
2. 画布 400×300，用 <svg width="400" height="300"> 开头；
3. 只许用这些元素：rect、circle、ellipse、line、polygon、text；
4. 只许纯色填充（如 skyblue、green、orange），禁止渐变/阴影/高光；
5. 至少包含：矩形墙、三角形屋顶、矩形门、圆形窗、矩形草地、圆形太阳。"""

print("向 AI 画家下单……\n")
art = paint(order)

# 画家有时会啰嗦地裹上解释或代码块记号——把外壳剥掉，只留 SVG 本体
art = art[art.find("<svg"):]                 # 从 <svg 开始截取
art = art[:art.find("</svg>") + 6]           # 到 </svg> 结束

ART_FILE.write_text(art, encoding="utf-8")
print(f"🖼 画已完成并保存：{ART_FILE.name}")
print("用浏览器打开这个文件就能看到画！（Finder 双击，或拖进浏览器窗口）\n")
print("—— 顺便看看 AI 的画技：它其实就是写了一份'画图代码'——")
print(art[:300], "……")

# 🔍 小实验：
#    1. 用文本编辑器打开 .svg 文件——你看到的是代码还是画？
#       （都是！这就是"作品即代码"：turtle 的图、pygame 的窗口、AI 的画，本质一样）
#    2. 给 order 加一样东西（一棵树？一朵云？），重新生成——画家随叫随到
#    3. 找茬：AI 有没有偷偷超纲（用了渐变？画歪了？太阳比房子大？）——
#       发现问题别慌，下一课你就是"改画导演"
