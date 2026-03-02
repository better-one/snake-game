#!/usr/bin/env python3
"""
智能体优化器
根据测试结果自动优化智能体配置和能力
"""

import json
from pathlib import Path
from datetime import datetime

class AgentOptimizer:
    """智能体优化器"""
    
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.agents_dir = project_dir / "agents"
        self.optimization_history = []
    
    def load_test_results(self):
        """加载最新测试结果"""
        test_reports_dir = self.project_dir / "test_reports"
        if not test_reports_dir.exists():
            return None
        
        reports = sorted(test_reports_dir.glob("agent_test_*.json"))
        if not reports:
            return None
        
        with open(reports[-1], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def optimize_agent(self, agent_name, suggestions):
        """优化单个智能体"""
        print(f"\n{'='*60}")
        print(f"🔧 优化：{agent_name}")
        print(f"{'='*60}")
        
        # 读取智能体配置
        agent_file = self.agents_dir / f"{self.get_agent_filename(agent_name)}.md"
        if not agent_file.exists():
            print(f"  ❌ 配置文件不存在")
            return False
        
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 应用优化
        optimizations_applied = []
        for suggestion in suggestions:
            print(f"\n  优化项：{suggestion}")
            
            # 根据优化建议更新配置
            if "增加" in suggestion or "添加" in suggestion:
                # 添加新能力描述
                new_section = f"\n### 新增能力\n- {suggestion}"
                if "## 核心能力" in content:
                    content = content.replace("## 核心能力", f"## 核心能力\n- {suggestion}")
                    optimizations_applied.append(suggestion)
                    print(f"    ✅ 已添加")
                else:
                    print(f"    ⚠️ 跳过（无合适位置）")
        
        # 保存优化后的配置
        if optimizations_applied:
            with open(agent_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n  ✅ 应用了 {len(optimizations_applied)} 项优化")
            
            # 记录优化历史
            self.optimization_history.append({
                'agent': agent_name,
                'timestamp': datetime.now().isoformat(),
                'optimizations': optimizations_applied
            })
            
            return True
        else:
            print(f"\n  ⚠️ 未应用任何优化")
            return False
    
    def get_agent_filename(self, agent_name):
        """获取智能体文件名"""
        mapping = {
            '产品经理': 'product_manager',
            '架构师': 'architect',
            '测试工程师': 'qa_engineer',
            'UI/UX设计师': 'ui_ux_designer',
            '安全工程师': 'security_engineer',
            '性能优化专家': 'performance_expert',
            '技术文档工程师': 'documentation_engineer',
            '代码审查员': 'code_reviewer',
            '数据分析师': 'data_analyst',
            '发布经理': 'release_manager',
            '运维工程师': 'devops_engineer'
        }
        return mapping.get(agent_name, agent_name.lower())
    
    def run_optimization(self):
        """执行优化流程"""
        print("\n" + "="*60)
        print("🔧 智能体优化器 v1.0")
        print("="*60)
        print(f"优化时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 加载测试结果
        test_results = self.load_test_results()
        if not test_results:
            print("❌ 未找到测试结果，请先运行测试套件")
            return False
        
        print(f"\n📊 加载测试结果:")
        print(f"   测试时间：{test_results['timestamp']}")
        print(f"   总体得分：{test_results['avg_score']:.1f}/100")
        print(f"   优化建议：{len(test_results['optimizations'])} 条")
        
        # 按智能体分组优化建议
        agent_suggestions = {}
        for opt in test_results['optimizations']:
            agent = opt['agent']
            if agent not in agent_suggestions:
                agent_suggestions[agent] = []
            if opt['suggestion']:  # 只处理有建议的
                agent_suggestions[agent].append(opt['suggestion'])
        
        # 执行优化
        print(f"\n🚀 开始优化 {len(agent_suggestions)} 个智能体...")
        
        optimized_count = 0
        for agent, suggestions in agent_suggestions.items():
            if self.optimize_agent(agent, suggestions):
                optimized_count += 1
        
        # 生成优化报告
        self.generate_optimization_report(test_results, optimized_count)
        
        print(f"\n✅ 优化完成！共优化 {optimized_count}/{len(agent_suggestions)} 个智能体")
        
        return True
    
    def generate_optimization_report(self, test_results, optimized_count):
        """生成优化报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'before_score': test_results['avg_score'],
            'optimized_agents': optimized_count,
            'history': self.optimization_history,
            'next_steps': [
                "重新运行测试套件验证优化效果",
                "对比优化前后得分",
                "持续迭代优化"
            ]
        }
        
        report_file = self.project_dir / "optimization_reports" / f"optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 优化报告已保存：{report_file}")
        
        # 打印优化摘要
        print(f"\n{'='*60}")
        print("📋 优化摘要")
        print(f"{'='*60}")
        
        for opt in self.optimization_history:
            print(f"\n{opt['agent']}:")
            for item in opt['optimizations']:
                print(f"  + {item}")

if __name__ == '__main__':
    optimizer = AgentOptimizer(Path('/home/firefly/snake_game'))
    optimizer.run_optimization()
