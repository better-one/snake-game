#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多智能体协作系统 - 自动化迭代开发 v2
修复：正确传递 project_dir
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_section(text, color=Colors.OKBLUE):
    print(f"\n{color}{Colors.BOLD}▶ {text}{Colors.ENDC}")
    print(f"{color}{'-'*50}{Colors.ENDC}")


# ==================== 产品经理智能体 ====================
class ProductManagerAgent:
    def __init__(self, project_dir):
        self.name = "产品经理"
        self.color = Colors.OKGREEN
        self.project_dir = project_dir
    
    def analyze_current_version(self):
        print_section(f"{self.name}: 分析当前产品状态", self.color)
        readme_path = self.project_dir / "README.md"
        current_version = "v1.2.0"
        
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "v1.2.0" in content:
                    current_version = "v1.2.0"
        
        print(f"  当前版本：{current_version}")
        print(f"  核心功能：6 种皮肤、难度递增、金色食物")
        print(f"  代码行数：~500 行")
        
        return {"version": current_version, "features": ["皮肤系统", "难度递增", "金色食物"], "lines_of_code": 500}
    
    def market_analysis(self):
        print_section(f"{self.name}: 市场分析", self.color)
        print("""
竞品分析:
  • 传统贪吃蛇：功能单一，缺乏创新
  • 现代版本：多数缺少个性化定制
  • 我们的优势：多皮肤、平滑难度曲线

用户反馈预测:
  ✅ 优点：皮肤系统受欢迎、难度适中
  ⚠️ 痛点：缺少音效、无法自定义、无社交功能
  💡 机会：道具系统、关卡模式、在线排行
""")
    
    def generate_requirements(self):
        print_section(f"{self.name}: 生成产品需求文档 (PRD)", self.color)
        
        prd = {
            "version": "v1.3.0",
            "title": "道具系统与音效",
            "priority": "High",
            "features": [
                {"id": "F1", "name": "道具系统", "description": "游戏中随机出现道具", "priority": "P0"},
                {"id": "F2", "name": "音效系统", "description": "添加游戏音效和 BGM", "priority": "P1"},
                {"id": "F3", "name": "暂停菜单优化", "description": "改进暂停界面", "priority": "P2"}
            ],
            "timeline": "1-2 天"
        }
        
        print(f"  版本：{prd['version']}")
        print(f"  标题：{prd['title']}")
        print(f"  功能数：{len(prd['features'])}")
        
        # 保存 PRD
        docs_dir = self.project_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        prd_file = docs_dir / "PRD_v1.3.json"
        with open(prd_file, 'w', encoding='utf-8') as f:
            json.dump(prd, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ PRD 已保存：{prd_file}")
        
        return prd
    
    def run(self):
        print_header("📊 产品经理智能体工作流程")
        current = self.analyze_current_version()
        self.market_analysis()
        prd = self.generate_requirements()
        return {"current_version": current, "prd": prd}


# ==================== 架构师智能体 ====================
class ArchitectAgent:
    def __init__(self, project_dir):
        self.name = "架构师"
        self.color = Colors.OKCYAN
        self.project_dir = project_dir
    
    def review_current_code(self):
        print_section(f"{self.name}: 代码审查", self.color)
        snake_file = self.project_dir / "snake.py"
        if not snake_file.exists():
            print("  ❌ snake.py 不存在")
            return None
        
        with open(snake_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        print(f"  代码行数：{len(lines)}")
        print(f"  类数量：{content.count('class ')}")
        print(f"  函数数量：{content.count('def ')}")
        
        review = {
            "strengths": ["✅ 模块化设计清晰", "✅ 配置驱动", "✅ 用户体验好"],
            "improvements": ["⚠️ 缺少音效模块", "⚠️ 道具系统未实现", "⚠️ 代码注释不足"]
        }
        
        print("\n  优点:")
        for s in review["strengths"]: print(f"    {s}")
        print("\n  改进建议:")
        for i in review["improvements"]: print(f"    {i}")
        
        return review
    
    def design_architecture(self, prd):
        print_section(f"{self.name}: 架构设计", self.color)
        print("""
新增模块:
1. ItemSystem (道具系统) - Item 类、ItemSpawner、EffectManager
2. SoundManager (音效系统) - load_sounds()、play()、toggle_music()
3. ConfigManager (配置管理) - 统一管理配置

数据结构:
class Item:
    def __init__(self, item_type, position):
        self.type = item_type  # 'speed', 'slow', 'ghost', 'double'
        self.position = position
        self.duration = 5
""")
    
    def generate_implementation_plan(self, prd):
        print_section(f"{self.name}: 实现计划", self.color)
        
        plan = {
            "steps": [
                {"step": 1, "task": "创建 ConfigManager", "time": "30 分钟"},
                {"step": 2, "task": "实现 ItemSystem", "time": "1 小时"},
                {"step": 3, "task": "实现 SoundManager", "time": "45 分钟"},
                {"step": 4, "task": "集成到主游戏", "time": "45 分钟"},
                {"step": 5, "task": "测试和优化", "time": "30 分钟"}
            ],
            "total_time": "3.5 小时"
        }
        
        print(f"  总步骤：{len(plan['steps'])}")
        print(f"  预计时间：{plan['total_time']}")
        
        # 保存计划
        plan_file = self.project_dir / "docs" / "implementation_plan.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ 实现计划已保存：{plan_file}")
        
        return plan
    
    def run(self, prd):
        print_header("🏗️ 架构师智能体工作流程")
        review = self.review_current_code()
        self.design_architecture(prd)
        plan = self.generate_implementation_plan(prd)
        return {"review": review, "plan": plan}


# ==================== 测试工程师智能体 ====================
class QAEngineerAgent:
    def __init__(self, project_dir):
        self.name = "测试工程师"
        self.color = Colors.WARNING
        self.project_dir = project_dir
    
    def create_test_plan(self, prd):
        print_section(f"{self.name}: 创建测试计划", self.color)
        
        test_plan = {
            "version": prd['version'],
            "test_types": [
                {"type": "功能测试", "cases": 5},
                {"type": "回归测试", "cases": 4},
                {"type": "性能测试", "cases": 3}
            ]
        }
        
        total = sum(t['cases'] for t in test_plan['test_types'])
        print(f"  测试类型：{len(test_plan['test_types'])}")
        print(f"  测试用例：{total}")
        
        # 保存
        test_file = self.project_dir / "docs" / "test_plan.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_plan, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ 测试计划已保存：{test_file}")
        
        return test_plan
    
    def generate_test_script(self):
        print_section(f"{self.name}: 生成自动化测试脚本", self.color)
        
        test_code = '''#!/usr/bin/env python3
"""贪吃蛇游戏自动化测试"""
import pytest

class TestItemSystem:
    def test_item_spawn(self): pass
    def test_speed_effect(self): pass
    def test_ghost_effect(self): pass

class TestSoundSystem:
    def test_sound_load(self): pass
    def test_sound_play(self): pass

class TestRegression:
    def test_movement(self): pass
    def test_collision(self): pass

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
'''
        
        test_file = self.project_dir / "test_game.py"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)
        print(f"  ✅ 测试脚本已生成：{test_file}")
        return test_file
    
    def run_tests(self):
        print_section(f"{self.name}: 执行测试（模拟）", self.color)
        
        results = {
            "total": 12, "passed": 10, "failed": 2, "skipped": 0,
            "details": [
                {"id": "TC001", "status": "PASS", "msg": "道具生成正常"},
                {"id": "TC002", "status": "PASS", "msg": "道具效果正确"},
                {"id": "TC003", "status": "FAIL", "msg": "持续时间偏差"},
                {"id": "PT003", "status": "FAIL", "msg": "启动时间 3.5s"}
            ]
        }
        
        print(f"\n  总测试数：{results['total']}")
        print(f"  {Colors.OKGREEN}通过：{results['passed']}{Colors.ENDC}")
        print(f"  {Colors.FAIL}失败：{results['failed']}{Colors.ENDC}")
        
        # 保存结果
        result_file = self.project_dir / "docs" / "test_results.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ 测试结果已保存：{result_file}")
        
        return results
    
    def run(self, prd):
        print_header("🧪 测试工程师智能体工作流程")
        test_plan = self.create_test_plan(prd)
        self.generate_test_script()
        results = self.run_tests()
        return {"test_plan": test_plan, "results": results}


# ==================== 主协调器 ====================
class MultiAgentCoordinator:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.pm = ProductManagerAgent(self.project_dir)
        self.architect = ArchitectAgent(self.project_dir)
        self.qa = QAEngineerAgent(self.project_dir)
    
    def run_iteration(self):
        print_header("🤖 多智能体协作 - 自动化迭代开发")
        print(f"项目目录：{self.project_dir}")
        print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 产品经理
        pm_output = self.pm.run()
        
        # 2. 架构师
        arch_output = self.architect.run(pm_output['prd'])
        
        # 3. 测试工程师
        qa_output = self.qa.run(pm_output['prd'])
        
        # 4. 生成报告
        self.generate_iteration_report(pm_output, arch_output, qa_output)
        
        print_header("✅ 多智能体协作完成")
        print("\n下一步:")
        print("  1. 审查生成的文档")
        print("  2. 根据实现计划编码")
        print("  3. 运行测试验证")
        print("  4. Git 提交新版本")
        
        return {"pm": pm_output, "architect": arch_output, "qa": qa_output}
    
    def generate_iteration_report(self, pm, arch, qa):
        print_section("📝 生成迭代报告", Colors.OKGREEN)
        
        report = f"""# 自动化迭代报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**目标版本**: {pm['prd']['version']}

## 产品经理输出
- 当前版本：{pm['current_version']['version']}
- 新功能：{len(pm['prd']['features'])} 个

## 架构师输出
- 代码审查：完成
- 实现计划：{len(arch['plan']['steps'])} 步

## 测试工程师输出
- 测试用例：12 个
- 模拟测试：{qa['results']['passed']}/{qa['results']['total']} 通过

## 下一步
1. 实现道具系统
2. 实现音效系统
3. 集成测试
4. 发布 v{pm['prd']['version']}
"""
        
        report_file = self.project_dir / "docs" / "iteration_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"  ✅ 迭代报告已保存：{report_file}")
        print("\n" + report)


def main():
    project_dir = Path('/home/firefly/snake_game')
    if not project_dir.exists():
        print(f"❌ 项目目录不存在：{project_dir}")
        sys.exit(1)
    
    coordinator = MultiAgentCoordinator(project_dir)
    coordinator.run_iteration()

if __name__ == '__main__':
    main()
