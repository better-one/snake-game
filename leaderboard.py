#!/usr/bin/env python3
"""在线排行榜系统 v1.6.0"""
import json
from datetime import datetime
from pathlib import Path

class Leaderboard:
    def __init__(self, db_file='leaderboard.json'):
        self.db_file = Path(db_file)
        self.scores = self.load()
    
    def load(self):
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {'single': [], 'dual': []}
    
    def save(self):
        self.db_file.parent.mkdir(exist_ok=True)
        with open(self.db_file, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def add_score(self, mode, name, score, level=1):
        entry = {
            'name': name,
            'score': score,
            'level': level,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.scores[mode].append(entry)
        self.scores[mode].sort(key=lambda x: x['score'], reverse=True)
        self.scores[mode] = self.scores[mode][:100]  # 保留前 100
        self.save()
        return self.get_rank(mode, score)
    
    def get_rank(self, mode, score):
        for i, entry in enumerate(self.scores[mode], 1):
            if entry['score'] == score:
                return i
        return len(self.scores[mode]) + 1
    
    def get_top(self, mode, limit=10):
        return self.scores[mode][:limit]
    
    def display(self, mode='single'):
        print(f"\n{'='*50}")
        print(f"🏆 {mode.upper()} 排行榜 TOP 10")
        print(f"{'='*50}")
        for i, entry in enumerate(self.get_top(mode), 1):
            print(f"{i:2}. {entry['name']:15} {entry['score']:6}分  Level{entry['level']}  {entry['date']}")
        print(f"{'='*50}\n")

if __name__ == '__main__':
    lb = Leaderboard()
    # 测试数据
    test_data = [
        ('single', 'Player1', 500, 5),
        ('single', 'SnakeKing', 450, 4),
        ('single', 'Gamer', 400, 4),
        ('dual', 'P1_Master', 380, 3),
        ('dual', 'P2_Pro', 350, 3),
    ]
    for mode, name, score, level in test_data:
        rank = lb.add_score(mode, name, score, level)
        print(f"Added: {name} - {score}分 (Rank #{rank})")
    lb.display('single')
    lb.display('dual')
