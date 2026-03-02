#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪吃蛇游戏 v1.2.0
新增：皮肤系统 - 多种颜色主题可选
"""

import pygame
import random
import sys
import json
from pathlib import Path

# 初始化 Pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
BASE_FPS = 10
MAX_FPS = 25

# 皮肤配置
SKINS = {
    'classic': {
        'name': '经典绿',
        'snake_head': (0, 200, 0),
        'snake_body': (0, 255, 0),
        'food': (255, 0, 0),
        'golden_food': (255, 215, 0),
        'bg': (0, 0, 0),
        'grid': (40, 40, 40)
    },
    'blue': {
        'name': '冰蓝',
        'snake_head': (0, 100, 255),
        'snake_body': (0, 200, 255),
        'food': (255, 100, 100),
        'golden_food': (255, 255, 100),
        'bg': (0, 10, 30),
        'grid': (20, 40, 60)
    },
    'purple': {
        'name': '紫魅',
        'snake_head': (180, 0, 255),
        'snake_body': (220, 100, 255),
        'food': (255, 0, 150),
        'golden_food': (255, 215, 0),
        'bg': (20, 0, 40),
        'grid': (50, 30, 60)
    },
    'orange': {
        'name': '橙热',
        'snake_head': (255, 100, 0),
        'snake_body': (255, 180, 0),
        'food': (0, 255, 100),
        'golden_food': (255, 255, 255),
        'bg': (30, 10, 0),
        'grid': (60, 40, 20)
    },
    'matrix': {
        'name': '黑客帝国',
        'snake_head': (0, 255, 100),
        'snake_body': (0, 200, 50),
        'food': (255, 50, 50),
        'golden_food': (255, 255, 255),
        'bg': (0, 20, 0),
        'grid': (0, 50, 0)
    },
    'dark': {
        'name': '暗黑',
        'snake_head': (150, 150, 150),
        'snake_body': (100, 100, 100),
        'food': (255, 50, 50),
        'golden_food': (255, 215, 0),
        'bg': (10, 10, 10),
        'grid': (30, 30, 30)
    }
}

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """蛇类"""
    
    def __init__(self, skin='classic'):
        self.skin = skin
        self.reset()
    
    def reset(self):
        """重置蛇的状态"""
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        """移动蛇"""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        """改变方向"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction
    
    def check_collision(self):
        """检测碰撞"""
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH:
            return True
        if head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False
    
    def draw(self, screen, skin_name='classic'):
        """绘制蛇"""
        colors = SKINS.get(skin_name, SKINS['classic'])
        
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            color = colors['snake_head'] if i == 0 else colors['snake_body']
            
            # 绘制蛇身
            pygame.draw.rect(screen, color, (x+1, y+1, GRID_SIZE-2, GRID_SIZE-2))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, GRID_SIZE, GRID_SIZE), 1)
            
            # 蛇头画眼睛
            if i == 0:
                eye_size = 3
                if self.direction == RIGHT:
                    eye1 = (x + GRID_SIZE - 6, y + 5)
                    eye2 = (x + GRID_SIZE - 6, y + GRID_SIZE - 8)
                elif self.direction == LEFT:
                    eye1 = (x + 4, y + 5)
                    eye2 = (x + 4, y + GRID_SIZE - 8)
                elif self.direction == UP:
                    eye1 = (x + 5, y + 4)
                    eye2 = (x + GRID_SIZE - 8, y + 4)
                else:
                    eye1 = (x + 5, y + GRID_SIZE - 7)
                    eye2 = (x + GRID_SIZE - 8, y + GRID_SIZE - 7)
                
                pygame.draw.circle(screen, (255, 255, 255), eye1, eye_size)
                pygame.draw.circle(screen, (255, 255, 255), eye2, eye_size)


class Food:
    """食物类"""
    
    def __init__(self, snake_body, skin='classic'):
        self.skin = skin
        self.spawn(snake_body)
    
    def spawn(self, snake_body, food_type='normal'):
        """生成食物"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                self.type = food_type
                return (x, y)
    
    def draw(self, screen, skin_name='classic'):
        """绘制食物"""
        colors = SKINS.get(skin_name, SKINS['classic'])
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        
        color = colors['golden_food'] if self.type == 'golden' else colors['food']
        
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
        radius = GRID_SIZE // 2 - 2
        pygame.draw.circle(screen, color, center, radius)
        pygame.draw.circle(screen, (255, 255, 255), center, radius, 1)


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 加载设置
        self.settings_file = Path('/home/firefly/snake_game/settings.json')
        self.load_settings()
        
        self.reset()
    
    def load_settings(self):
        """加载设置"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.current_skin = settings.get('skin', 'classic')
                self.high_score = settings.get('high_score', 0)
        else:
            self.current_skin = 'classic'
            self.high_score = 0
    
    def save_settings(self):
        """保存设置"""
        settings = {
            'skin': self.current_skin,
            'high_score': self.high_score
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)
    
    def reset(self):
        """重置游戏"""
        self.snake = Snake(self.current_skin)
        self.food = Food(self.snake.body, self.current_skin)
        self.score = 0
        self.level = 1
        self.games_played = 0
        self.game_over = False
        self.paused = False
        self.current_fps = BASE_FPS
        self.show_skin_menu = False
    
    def calculate_speed(self):
        """计算速度"""
        new_level = (self.score // 50) + 1
        if new_level > self.level:
            self.level = new_level
        self.current_fps = min(BASE_FPS + (self.level - 1) * 2, MAX_FPS)
    
    def change_skin(self, skin_name):
        """更换皮肤"""
        if skin_name in SKINS:
            self.current_skin = skin_name
            self.save_settings()
            # 重新创建游戏对象以应用新皮肤
            self.snake = Snake(self.current_skin)
            self.food = Food(self.snake.body, self.current_skin)
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_skin_menu:
                        self.show_skin_menu = False
                    else:
                        return False
                
                if self.show_skin_menu:
                    # 皮肤选择菜单
                    skin_keys = list(SKINS.keys())
                    if event.key == pygame.K_1:
                        self.change_skin(skin_keys[0])
                    elif event.key == pygame.K_2:
                        self.change_skin(skin_keys[1])
                    elif event.key == pygame.K_3:
                        self.change_skin(skin_keys[2])
                    elif event.key == pygame.K_4:
                        self.change_skin(skin_keys[3])
                    elif event.key == pygame.K_5:
                        self.change_skin(skin_keys[4])
                    elif event.key == pygame.K_6:
                        self.change_skin(skin_keys[5])
                    self.show_skin_menu = False
                elif self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.games_played += 1
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_settings()
                        self.reset()
                else:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_m:
                        self.show_skin_menu = True
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(RIGHT)
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused or self.show_skin_menu:
            return
        
        self.snake.move()
        
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            points = 20 if self.food.type == 'golden' else 10
            self.score += points
            food_type = 'golden' if random.random() < 0.1 else 'normal'
            self.food = Food(self.snake.body, self.current_skin, )
            self.calculate_speed()
        
        if self.snake.check_collision():
            self.game_over = True
    
    def draw(self):
        """绘制游戏画面"""
        colors = SKINS.get(self.current_skin, SKINS['classic'])
        self.screen.fill(colors['bg'])
        
        # 绘制网格
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, colors['grid'], (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, colors['grid'], (0, y), (WINDOW_WIDTH, y))
        
        # 绘制游戏对象
        self.food.draw(self.screen, self.current_skin)
        self.snake.draw(self.screen, self.current_skin)
        
        # 绘制 UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        
        if self.paused and not self.game_over:
            self.draw_pause()
        
        if self.show_skin_menu:
            self.draw_skin_menu()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """绘制 UI"""
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.small_font.render(f'Level: {self.level}', True, SKINS[self.current_skin]['golden_food'])
        self.screen.blit(level_text, (10, 45))
        
        speed_text = self.small_font.render(f'Speed: {self.current_fps} FPS', True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 65))
        
        high_score_text = self.small_font.render(f'Best: {self.high_score}', True, (255, 255, 255))
        self.screen.blit(high_score_text, (WINDOW_WIDTH - 120, 10))
        
        skin_name = SKINS[self.current_skin]['name']
        skin_text = self.small_font.render(f'Skin: {skin_name}', True, (200, 200, 200))
        self.screen.blit(skin_text, (WINDOW_WIDTH - 150, 45))
        
        hint_text = self.small_font.render('M: Change Skin', True, (150, 150, 150))
        self.screen.blit(hint_text, (WINDOW_WIDTH - 150, 65))
    
    def draw_game_over(self):
        """绘制游戏结束"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render('GAME OVER', True, (255, 0, 0))
        text_rect1 = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
        self.screen.blit(game_over_text, text_rect1)
        
        score_text = self.font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        text_rect2 = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(score_text, text_rect2)
        
        restart_text = self.small_font.render('Press SPACE to restart', True, (255, 255, 255))
        text_rect3 = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        self.screen.blit(restart_text, text_rect3)
    
    def draw_pause(self):
        """绘制暂停"""
        pause_text = self.font.render('PAUSED', True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(pause_text, text_rect)
    
    def draw_skin_menu(self):
        """绘制皮肤选择菜单"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        title_text = self.font.render('Choose Skin (1-6)', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title_text, title_rect)
        
        # 列出所有皮肤
        y_offset = 130
        skin_keys = list(SKINS.keys())
        for i, key in enumerate(skin_keys):
            skin = SKINS[key]
            num = i + 1
            text = f'{num}. {skin["name"]}'
            
            # 当前选中的皮肤高亮
            if key == self.current_skin:
                text += ' (Current)'
                color = skin['golden_food']
            else:
                color = (255, 255, 255)
            
            skin_text = self.small_font.render(text, True, color)
            text_rect = skin_text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            self.screen.blit(skin_text, text_rect)
            
            # 显示颜色预览
            preview_x = WINDOW_WIDTH//2 - 100
            pygame.draw.rect(self.screen, skin['snake_body'], (preview_x, y_offset - 10, 20, 20))
            
            y_offset += 35
        
        hint_text = self.small_font.render('Press ESC to cancel', True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH//2, y_offset + 20))
        self.screen.blit(hint_text, hint_rect)
    
    def run(self):
        """运行游戏"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.current_fps)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    print("🐍 贪吃蛇游戏 v1.2.0")
    print("新增功能：皮肤系统")
    print("控制：方向键/WASD 移动，空格暂停，M 换皮肤，ESC 退出")
    print("=" * 50)
    print("可用皮肤:")
    for key, skin in SKINS.items():
        print(f"  • {skin['name']} ({key})")
    print("=" * 50)
    
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
