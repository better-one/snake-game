#!/usr/bin/env python3
"""成就系统 v1.7.0"""
import json
from datetime import datetime
from pathlib import Path

ACHIEVEMENTS = {
    'first_blood': {'name': '首血', 'desc': '首次达到 100 分', 'condition': lambda s: s>=100, 'icon': '🥉'},
    'snake_novice': {'name': '新手', 'desc': '首次达到 200 分', 'condition': lambda s: s>=200, 'icon': '🥈'},
    'snake_expert': {'name': '专家', 'desc': '首次达到 300 分', 'condition': lambda s: s>=300, 'icon': '🥇'},
    'snake_master': {'name': '大师', 'desc': '首次达到 400 分', 'condition': lambda s: s>=400, 'icon': '👑'},
    'snake_legend': {'name': '传奇', 'desc': '首次达到 500 分', 'condition': lambda s: s>=500, 'icon': '🐍'},
    'speed_demon': {'name': '速度恶魔', 'desc': '达到 10 级', 'condition': lambda s,l: l>=10, 'icon': '⚡'},
    'golden_eater': {'name': '美食家', 'desc': '吃到 50 个金色食物', 'condition': lambda s,g: g>=50, 'icon': '🍎'},
    'ghost_rider': {'name': '幽灵', 'desc': '使用穿墙道具通过 10 次墙', 'condition': lambda s,w: w>=10, 'icon': '👻'},
    'double_kill': {'name': '双杀', 'desc': '双人模式获胜', 'condition': lambda s,w: w>0, 'icon': '⚔️'},
    'marathon': {'name': '马拉松', 'desc': '单局游戏超过 10 分钟', 'condition': lambda s,t: t>=600, 'icon': '⏱️'}
}

class AchievementSystem:
    def __init__(self, save_file='achievements.json'):
        self.save_file = Path(save_file)
        self.player_data = self.load()
    
    def load(self):
        if self.save_file.exists():
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return {'unlocked': [], 'stats': {'games':0, 'total_score':0, 'golden_foods':0, 'wall_passes':0, 'dual_wins':0, 'max_time':0}}
    
    def save(self):
        self.save_file.parent.mkdir(exist_ok=True)
        with open(self.save_file, 'w') as f:
            json.dump(self.player_data, f, indent=2, ensure_ascii=False)
    
    def check_achievements(self, score, level=1, golden=0, walls=0, dual_wins=0, play_time=0):
        newly_unlocked = []
        for ach_id, ach in ACHIEVEMENTS.items():
            if ach_id in self.player_data['unlocked']:
                continue
            try:
                if ach['condition'](score, level, golden, walls, dual_wins, play_time):
                    self.player_data['unlocked'].append(ach_id)
                    newly_unlocked.append(ach)
            except: pass
        if newly_unlocked:
            self.save()
        return newly_unlocked
    
    def display(self):
        print(f"\n{'='*60}")
        print(f"🏆 成就系统 ({len(self.player_data['unlocked'])}/{len(ACHIEVEMENTS)})")
        print(f"{'='*60}")
        print("\n已解锁:")
        for ach_id in self.player_data['unlocked']:
            ach = ACHIEVEMENTS[ach_id]
            print(f"  {ach['icon']} {ach['name']}: {ach['desc']}")
        print("\n未解锁:")
        for ach_id, ach in ACHIEVEMENTS.items():
            if ach_id not in self.player_data['unlocked']:
                print(f"  🔒 {ach['name']}: {ach['desc']}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    ach = AchievementSystem()
    # 模拟解锁
    print("测试成就解锁...")
    unlocked = ach.check_achievements(score=350, level=5, golden=10, walls=5, dual_wins=1, play_time=300)
    if unlocked:
        print(f"\n🎉 新解锁 {len(unlocked)} 个成就:")
        for a in unlocked:
            print(f"  {a['icon']} {a['name']}")
    ach.display()
