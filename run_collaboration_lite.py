#!/usr/bin/env python3
"""
运行精简版智能体协作 - v1.23 版本规划
使用阿里云百炼 Coding Plan API
"""

from pathlib import Path
from dashscope_llm_integration import DashScopeClient, DashScopeCollaborationPlatform

# 使用用户提供的 API Key
API_KEY = "sk-sp-4c6bc141469d4ed7be788c9cb0e6af39"

print("="*70)
print("🤖 贪吃蛇游戏 - 智能体协作开发 v1.23 (精简版)")
print("="*70)

# 创建协作平台
platform = DashScopeCollaborationPlatform(
    project_dir=Path('/home/firefly/snake_game'),
    api_key=API_KEY
)

print("\n" + "="*70)
print("🤖 阿里云百炼智能体协作")
print("="*70)

# 测试连接
if platform.llm.test_connection():
    print("✅ 使用真实 API")
else:
    print("⚠️  使用模拟模式")

# 运行简化讨论 - 只邀请 3 个关键角色
print("\n" + "="*70)
print("💬 讨论主题：v1.23 版本功能规划")
print("="*70)
print("参与者：产品经理、架构师、测试工程师\n")

# 手动运行简化版讨论
from datetime import datetime

conversation = {
    "topic": "v1.23 版本功能规划",
    "participants": ["产品经理", "架构师", "测试工程师"],
    "messages": [],
    "start_time": datetime.now().isoformat()
}

topic = "请为贪吃蛇 v1.23 版本提出功能规划建议。考虑因素：用户需求、技术可行性、测试复杂度。"

# 第一轮：各自发表观点（只调用 3 次 API）
print("📍 第一轮：各自发表观点\n")
for agent_name in ["产品经理", "架构师", "测试工程师"]:
    agent = platform.agents[agent_name]
    print(f"⏳ {agent_name} 正在思考...")
    thought = agent.think(topic)
    print(f"🗣️ {agent_name}: {thought}\n")
    
    conversation["messages"].append({
        "from": agent_name,
        "content": thought,
        "type": "initial"
    })

# 第二轮：总结共识（只调用 1 次 API）
print("\n✅ 总结共识\n")
initiator = platform.agents["产品经理"]
print("⏳ 产品经理 正在总结...")
consensus = initiator.think("基于以上 3 位专家的观点，请总结 v1.23 版本的功能优先级和下一步行动计划。")
print(f"📋 共识：{consensus}\n")

conversation["consensus"] = consensus
conversation["end_time"] = datetime.now().isoformat()

print("\n" + "="*70)
print("✅ 讨论完成")
print("="*70)
