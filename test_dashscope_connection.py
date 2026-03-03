#!/usr/bin/env python3
"""
测试阿里云百炼 API 连接
使用 Coding Plan 专属端点
"""

from dashscope_llm_integration import DashScopeClient

# 使用用户提供的 API Key
API_KEY = "sk-sp-4c6bc141469d4ed7be788c9cb0e6af39"

print("="*70)
print("🧪 测试阿里云百炼 API 连接")
print("="*70)

# 创建客户端
client = DashScopeClient(api_key=API_KEY)

print("\n" + "="*70)
print("📡 测试 API 调用")
print("="*70)

# 测试消息
test_messages = [
    {"role": "system", "content": "你是 AI 助手，请用简洁的语言回复。"},
    {"role": "user", "content": "你好，请简单介绍一下你自己。"}
]

print("\n发送测试消息...")
response = client.chat(test_messages, temperature=0.7)

print(f"\n💬 AI 回复：\n{response}")

print("\n" + "="*70)
print("✅ 测试完成")
print("="*70)
