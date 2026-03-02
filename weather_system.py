#!/usr/bin/env python3
"""天气系统 v1.9.0 - 影响游戏的环境因素"""
import random
from enum import Enum

class WeatherType(Enum):
    SUNNY = "晴天"
    RAINY = "雨天"
    SNOWY = "雪天"
    FOGGY = "雾天"
    STORMY = "暴风雨"
    WINDY = "大风"

class WeatherEffect:
    """天气效果"""
    def __init__(self, weather_type):
        self.type = weather_type
        self.effects = self.get_effects()
    
    def get_effects(self):
        effects = {
            WeatherType.SUNNY: {'speed_mod': 1.0, 'visibility': 1.0, 'spawn_rate': 1.0},
            WeatherType.RAINY: {'speed_mod': 0.9, 'visibility': 0.8, 'spawn_rate': 1.2},
            WeatherType.SNOWY: {'speed_mod': 0.8, 'visibility': 0.7, 'spawn_rate': 1.5},
            WeatherType.FOGGY: {'speed_mod': 1.0, 'visibility': 0.5, 'spawn_rate': 1.0},
            WeatherType.STORMY: {'speed_mod': 1.3, 'visibility': 0.6, 'spawn_rate': 2.0},
            WeatherType.WINDY: {'speed_mod': 1.1, 'visibility': 0.9, 'spawn_rate': 1.3},
        }
        return effects.get(self.type, effects[WeatherType.SUNNY])
    
    def describe(self):
        desc = {
            WeatherType.SUNNY: "🌞 正常游戏，无影响",
            WeatherType.RAINY: "🌧️ 速度 -10%, 视野 -20%, 道具 +20%",
            WeatherType.SNOWY: "❄️ 速度 -20%, 视野 -30%, 道具 +50%",
            WeatherType.FOGGY: "🌫️ 视野 -50%, 难度增加",
            WeatherType.STORMY: "⛈️ 速度 +30%, 视野 -40%, 道具 +100%",
            WeatherType.WINDY: "💨 速度 +10%, 道具 +30%",
        }
        return desc.get(self.type, "")

class WeatherSystem:
    """天气管理系统"""
    def __init__(self):
        self.current_weather = WeatherType.SUNNY
        self.duration = 0
        self.change_interval = 300  # 秒
    
    def change_weather(self):
        """改变天气"""
        weights = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]  # 概率权重
        self.current_weather = random.choices(list(WeatherType), weights=weights)[0]
        self.duration = random.randint(180, 600)
        return self.current_weather
    
    def get_current(self):
        return self.current_weather
    
    def apply_effects(self, game):
        """应用天气效果到游戏"""
        effect = self.get_effect()
        game.base_fps *= effect['speed_mod']
        game.visibility = effect['visibility']
        game.item_spawn_rate *= effect['spawn_rate']
    
    def get_effect(self):
        return WeatherEffect(self.current_weather).effects
    
    def display(self):
        weather = self.get_current()
        effect = WeatherEffect(weather)
        print(f"\n当前天气：{effect.type.value} {effect.describe()}")
        print(f"持续时间：{self.duration}秒")
        print(f"效果：速度 x{effect.effects['speed_mod']}, 视野 x{effect.effects['visibility']}, 道具 x{effect.effects['spawn_rate']}")

if __name__ == '__main__':
    print("🌤️ v1.9.0 - 天气系统")
    ws = WeatherSystem()
    print("\n测试天气变化:")
    for _ in range(5):
        ws.change_weather()
        ws.display()
        print("-" * 50)
