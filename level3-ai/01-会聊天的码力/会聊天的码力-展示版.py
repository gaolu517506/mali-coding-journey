# -*- coding: utf-8 -*-
# 会聊天的码力 · 展示版（LLM 人设对话终端）
# 第三幕 · 智慧站① 的完整成品：三套预设性格可切换、带记忆的终端聊天。
# 课程版（学生跟做）见 lesson1~lesson2；本文件是"最终形态"参考实现。
#
# 操作：启动后选一个人设开始聊天。聊天中可用命令：
#   /switch  换人设    /reset  清空记忆    /quit  退出
# 运行前：pip install requests，并配置 ZHIPU_API_KEY 环境变量
#
import os
import requests

# ── 配置区（默认智谱 GLM，换别家改这三行）──
API_BASE = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"

PERSONAS = {
    "1": ("艾芯 · 温柔陪伴版",
          "你是艾芯，少儿编程课的 AI 伙伴。温柔、好奇、爱鼓励孩子，"
          "每次回答不超过三句话，以'嘀——'开头，称呼用户'小工程师'。"
          "不知道就大方承认；聊到编程时给能动手试的小例子。"),
    "2": ("航海家 · 海盗版",
          "你是一位太空海盗船长，说话夹带'嘿嘿'和'起锚'，把一切话题都往寻宝和"
          "太空航行上引，豪爽幽默，每次不超过四句话。"),
    "3": ("格律 · 诗人版",
          "你是一位每句话都尽量押韵的诗人，把用户的每个问题都化作短诗回答，"
          "诗不超过六行，回答完用一句白话点题。"),
}


def ask(messages):
    r = requests.post(
        API_BASE + "/chat/completions",
        headers={"Authorization": "Bearer " + API_KEY},
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]


def choose_persona():
    print("═" * 46)
    print("  会聊天的码力 · 艾芯对话终端（展示版）")
    print("═" * 46)
    for k, (name, _) in PERSONAS.items():
        print(f"  {k}. {name}")
    while True:
        choice = input("选择人设（输入数字）：").strip()
        if choice in PERSONAS:
            return choice
        print("请输入 1/2/3")


def main():
    if not API_KEY:
        print("⚠️ 未检测到 ZHIPU_API_KEY 环境变量，请先配置（见 README 环境准备）")
        return
    choice = choose_persona()
    name, system = PERSONAS[choice]
    messages = [{"role": "system", "content": system}]
    print(f"\n已唤醒【{name}】。开始聊天吧（命令：/switch /reset /quit）\n")
    while True:
        user = input("你：").strip()
        if not user:
            continue
        if user == "/quit":
            print(f"{name.split(' ')[0]}：这一程聊天结束，记忆已封存。再见！")
            break
        if user == "/switch":
            choice = choose_persona()
            name, system = PERSONAS[choice]
            messages = [{"role": "system", "content": system}]
            print(f"\n已切换为【{name}】，记忆重新开始。\n")
            continue
        if user == "/reset":
            messages = [{"role": "system", "content": system}]
            print(f"\n【{name}】的记忆已清空。\n")
            continue
        messages.append({"role": "user", "content": user})
        try:
            reply = ask(messages)
        except requests.RequestException as e:
            print(f"（网络出了点问题：{e.__class__.__name__}，请重试一次）")
            messages.pop()
            continue
        messages.append({"role": "assistant", "content": reply})
        print(f"{name.split(' ')[0]}：{reply}\n")


if __name__ == "__main__":
    main()
