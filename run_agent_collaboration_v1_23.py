#!/usr/bin/env python3
"""
运行真正的智能体协作 - v1.23 版本规划
使用阿里云百炼 Coding Plan API
"""

from pathlib import Path
from dashscope_llm_integration import DashScopeClient, DashScopeCollaborationPlatform

# 使用用户提供的 API Key
API_KEY = "sk-sp-4c6bc141469d4ed7be788c9cb0e6af39"

print("="*70)
print("🤖 贪吃蛇游戏 - 智能体协作开发 v1.23")
print("="*70)

# 创建协作平台
platform = DashScopeCollaborationPlatform(
    project_dir=Path('/home/firefly/snake_game'),
    api_key=API_KEY
)

# 运行协作
platform.run_collaboration()
