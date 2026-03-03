#!/usr/bin/env python3
"""
简单测试 API 响应时间
"""

import time
from dashscope_llm_integration import DashScopeClient

API_KEY = "sk-sp-4c6bc141469d4ed7be788c9cb0e6af39"

client = DashScopeClient(api_key=API_KEY)

print("\n测试 API 响应时间...\n")

start = time.time()

messages = [
    {"role": "system", "content": "你是产品经理，负责贪吃蛇游戏的产品规划。"},
    {"role": "user", "content": "请为贪吃蛇 v1.23 版本提出 3 个新功能建议。"}
]

print("发送请求...")
response = client.chat(messages)

end = time.time()

print(f"\n💬 AI 回复：\n{response}")
print(f"\n⏱️  响应时间：{end - start:.2f}秒")
