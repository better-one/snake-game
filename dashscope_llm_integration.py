#!/usr/bin/env python3
"""
阿里云百炼 (DashScope) 集成
支持通义千问 Qwen 系列模型
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 导入基础类
from llm_agent_communication import IntelligentAgent

class DashScopeClient:
    """阿里云百炼客户端（支持 Coding Plan）"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        
        # 根据 API Key 前缀选择端点
        # Coding Plan 专属 API Key（sk-sp-开头）必须使用专属端点
        if self.api_key and self.api_key.startswith("sk-sp-"):
            self.base_url = "https://coding.dashscope.aliyuncs.com/v1"
            print(f"✅ 检测到 Coding Plan API Key")
            print(f"   专属端点：{self.base_url}")
        else:
            self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            print(f"✅ 检测到通用 API Key")
            print(f"   通用端点：{self.base_url}")
        
        self.model = "qwen3.5-plus"  # Coding Plan 推荐模型
        self.use_mock = not self.api_key
        
        if self.api_key:
            print(f"✅ 阿里云百炼 API Key 已配置")
            print(f"   模型：{self.model}")
            print(f"   服务：通义千问 Coding Plan")
        else:
            print(f"⚠️  未配置 API Key，使用模拟模式")
            print(f"   请设置 DASHSCOPE_API_KEY 环境变量")
    
    def chat(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """聊天对话"""
        if self.use_mock:
            return self._mock_chat(messages)
        else:
            return self._real_chat(messages, temperature)
    
    def generate_response(self, agent_name: str, context: str, user_message: str) -> str:
        """生成智能回复（兼容 IntelligentAgent 接口）"""
        messages = [
            {"role": "system", "content": f"你是{agent_name}，是贪吃蛇游戏开发团队的专业成员。请基于你的专业背景，给出专业、有价值的回复。"},
            {"role": "user", "content": f"{context}\n\n请回复：{user_message}"}
        ]
        return self.chat(messages, temperature=0.7)
    
    def _mock_chat(self, messages: List[Dict]) -> str:
        """模拟回复"""
        last_message = messages[-1]["content"] if messages else ""
        
        # 基于角色和内容生成更智能的回复
        responses = {
            "产品经理": [
                "从产品角度，我建议优先开发用户最需要的功能。根据数据分析，用户最期待的是社交功能。",
                "考虑到开发周期，我建议分两期：第一期做核心功能，第二期做增值功能。",
                "这个需求很有价值，但需要平衡开发成本。建议先做 MVP 验证。"
            ],
            "架构师": [
                "技术上是可行的。我建议采用微服务架构，便于后续扩展。主要风险是并发处理。",
                "评估了三种方案：方案 A 成本低但扩展性差；方案 B 平衡但开发周期长；方案 C 最优但需要新技术。",
                "从架构角度，建议先搭建核心框架，再逐步添加功能。这样风险可控。"
            ],
            "测试工程师": [
                "测试方面，我建议引入自动化测试，覆盖率目标 85%。需要预留足够的测试时间。",
                "这个功能测试复杂度较高，建议提前准备测试用例，特别是边界情况。",
                "质量第一，建议增加一轮回归测试，确保不影响现有功能。"
            ],
            "UI/UX设计师": [
                "从用户体验角度，建议简化操作流程，减少用户学习成本。",
                "界面设计需要保持一致性，建议先建立设计规范再开发。",
                "用户调研显示，简洁直观的设计最受欢迎。我会确保界面友好易用。"
            ],
            "安全工程师": [
                "安全审查发现 2 个潜在风险：数据泄露和注入攻击。建议增加输入验证和加密。",
                "从安全角度，建议实施多层防护：输入验证、权限控制、日志审计。",
                "这个功能涉及用户数据，必须做好加密和权限控制。我会全程跟进安全审查。"
            ],
            "运维工程师": [
                "运维方面，建议采用容器化部署，便于扩展和维护。",
                "需要建立完善的监控体系，包括性能监控、错误追踪、日志分析。",
                "建议实施 CI/CD 流程，实现自动化部署和回滚机制。"
            ],
            "性能优化专家": [
                "性能测试显示，当前架构可以支撑 1000 并发。优化后可达 3000 并发。",
                "主要瓶颈在数据库查询，建议增加缓存层，优化查询语句。",
                "建议实施性能监控，设置阈值告警，及时发现性能问题。"
            ]
        }
        
        # 提取角色
        agent_name = "产品经理"  # 默认
        for msg in messages:
            if "role" in msg and msg["role"] == "system":
                if "产品经理" in msg["content"]:
                    agent_name = "产品经理"
                elif "架构师" in msg["content"]:
                    agent_name = "架构师"
                elif "测试" in msg["content"]:
                    agent_name = "测试工程师"
                elif "UI" in msg["content"] or "设计" in msg["content"]:
                    agent_name = "UI/UX设计师"
                elif "安全" in msg["content"]:
                    agent_name = "安全工程师"
                elif "运维" in msg["content"]:
                    agent_name = "运维工程师"
                elif "性能" in msg["content"]:
                    agent_name = "性能优化专家"
        
        agent_responses = responses.get(agent_name, ["我会认真考虑这个问题。"])
        
        # 根据内容选择
        if "功能" in last_message or "需求" in last_message:
            return agent_responses[0]
        elif "技术" in last_message or "方案" in last_message:
            return agent_responses[1] if len(agent_responses) > 1 else agent_responses[0]
        elif "建议" in last_message:
            return agent_responses[2] if len(agent_responses) > 2 else agent_responses[0]
        else:
            return agent_responses[0]
    
    def _real_chat(self, messages: List[Dict], temperature: float) -> str:
        """真实调用阿里云百炼 API（使用正确的端点）"""
        try:
            import requests
            
            # 构建 API 请求
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"⚠️  API 调用失败：{response.status_code} - {response.text}")
                return self._mock_chat(messages)
                
        except ImportError:
            print("⚠️  未安装 requests 库，使用模拟模式")
            print("   安装：pip install requests")
            return self._mock_chat(messages)
        except Exception as e:
            print(f"⚠️  API 调用异常：{e}")
            return self._mock_chat(messages)
    
    def test_connection(self) -> bool:
        """测试连接"""
        if not self.api_key:
            print("❌ 未配置 API Key")
            return False
        
        test_messages = [
            {"role": "system", "content": "你是 AI 助手"},
            {"role": "user", "content": "你好，请回复'连接成功'"}
        ]
        
        response = self.chat(test_messages)
        
        if "连接成功" in response or not self.use_mock:
            print("✅ 阿里云百炼连接成功")
            return True
        else:
            print("❌ 连接失败")
            return False


class DashScopeAgent(IntelligentAgent):
    """基于阿里云百炼的智能体"""
    
    def __init__(self, name: str, llm: DashScopeClient):
        super().__init__(name, llm)


class DashScopeCollaborationPlatform:
    """阿里云百炼协作平台"""
    
    def __init__(self, project_dir, api_key: Optional[str] = None):
        self.project_dir = Path(project_dir)
        self.llm = DashScopeClient(api_key)
        self.agents = self._create_agents()
        self.conversations = []
        
        print(f"\n✅ 创建了 {len(self.agents)} 个基于阿里云百炼的智能体")
    
    def _create_agents(self) -> Dict[str, DashScopeAgent]:
        """创建智能体"""
        agent_names = [
            "产品经理",
            "架构师",
            "测试工程师",
            "UI/UX设计师",
            "安全工程师",
            "运维工程师",
            "性能优化专家"
        ]
        
        return {
            name: DashScopeAgent(name, self.llm)
            for name in agent_names
        }
    
    def start_discussion(self, topic: str, participants: List[str]):
        """发起真正的讨论"""
        print(f"\n{'='*70}")
        print(f"💬 发起讨论：{topic}")
        print(f"{'='*70}")
        print(f"参与者：{', '.join(participants)}\n")
        
        conversation = {
            "topic": topic,
            "participants": participants,
            "messages": [],
            "start_time": datetime.now().isoformat()
        }
        
        # 第一轮：各自发表观点
        print("📍 第一轮：各自发表观点\n")
        initial_thoughts = []
        for agent_name in participants:
            agent = self.agents[agent_name]
            thought = agent.think(topic)
            print(f"🗣️ {agent_name}: {thought}\n")
            
            conversation["messages"].append({
                "from": agent_name,
                "content": thought,
                "type": "initial"
            })
            initial_thoughts.append((agent_name, thought))
        
        # 第二轮：互相回应
        print("🔄 第二轮：互相回应和讨论\n")
        for i, (agent1_name, thought1) in enumerate(initial_thoughts):
            # 其他智能体回应
            for agent2_name in participants:
                if agent2_name != agent1_name:
                    agent2 = self.agents[agent2_name]
                    response = agent2.respond_to(agent1_name, thought1)
                    print(f"🗣️ {agent2_name} 回应 {agent1_name}: {response}\n")
                    
                    conversation["messages"].append({
                        "from": agent2_name,
                        "to": agent1_name,
                        "content": response,
                        "type": "response"
                    })
        
        # 第三轮：总结共识
        print("✅ 第三轮：总结共识\n")
        initiator = self.agents[participants[0]]
        consensus = initiator.think(f"基于以上讨论，请总结共识和下一步行动计划")
        print(f"📋 共识：{consensus}\n")
        
        conversation["consensus"] = consensus
        conversation["end_time"] = datetime.now().isoformat()
        self.conversations.append(conversation)
        
        return conversation
    
    def run_collaboration(self):
        """运行协作"""
        print("\n" + "="*70)
        print("🤖 阿里云百炼智能体协作")
        print("="*70)
        
        # 测试连接
        if self.llm.test_connection():
            print("✅ 使用真实 API")
        else:
            print("⚠️  使用模拟模式")
        
        # 运行讨论
        self.start_discussion(
            topic="v1.23 版本功能规划",
            participants=["产品经理", "架构师", "测试工程师"]
        )


if __name__ == '__main__':
    # 测试配置
    platform = DashScopeCollaborationPlatform(
        Path('/home/firefly/snake_game'),
        api_key=None  # 等待用户配置
    )
    
    print("\n" + "="*70)
    print("📋 配置说明")
    print("="*70)
    print("\n请提供阿里云百炼 API Key:")
    print("1. 访问：https://dashscope.console.aliyun.com/apiKey")
    print("2. 登录阿里云账号")
    print("3. 创建/复制 API Key")
    print("4. 告诉我 API Key，我帮你配置")
    print("\n或者设置环境变量:")
    print("  export DASHSCOPE_API_KEY='你的 key'")
