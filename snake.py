#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪吃蛇游戏 v1.1.0
新增：难度递增系统 - 随着分数提高，蛇移动速度加快
"""

import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
BASE_FPS = 10  # 基础速度
MAX_FPS = 25   # 最高速度

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GRAY = (40, 40, 40)

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """蛇类"""
    
    def __init__(self):
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
        """改变方向（不能直接反向）"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction
    
    def check_collision(self):
        """检测碰撞"""
        head = self.body[0]
        
        # 撞墙
        if head[0] < 0 or head[0] >= GRID_WIDTH:
            return True
        if head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        
        # 撞自己
        if head in self.body[1:]:
            return True
        
        return False
    
    def draw(self, screen):
        """绘制蛇"""
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            # 蛇头颜色深一些
            color = DARK_GREEN if i == 0 else GREEN
            
            # 绘制圆角矩形效果
            pygame.draw.rect(screen, color, (x+1, y+1, GRID_SIZE-2, GRID_SIZE-2))
            pygame.draw.rect(screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 1)
            
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
                else:  # DOWN
                    eye1 = (x + 5, y + GRID_SIZE - 7)
                    eye2 = (x + GRID_SIZE - 8, y + GRID_SIZE - 7)
                
                pygame.draw.circle(screen, WHITE, eye1, eye_size)
                pygame.draw.circle(screen, WHITE, eye2, eye_size)


class Food:
    """食物类"""
    
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)
        self.type = 'normal'  # normal, golden
    
    def spawn(self, snake_body, food_type='normal'):
        """在随机位置生成食物"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                self.type = food_type
                return (x, y)
    
    def draw(self, screen):
        """绘制食物"""
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        
        if self.type == 'golden':
            color = GOLD
        else:
            color = RED
        
        # 绘制圆形食物
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
        radius = GRID_SIZE // 2 - 2
        pygame.draw.circle(screen, color, center, radius)
        pygame.draw.circle(screen, WHITE, center, radius, 1)


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇 v1.1.0 - 难度递增')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset()
    
    def reset(self):
        """重置游戏"""
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.level = 1
        self.games_played = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.current_fps = BASE_FPS
    
    def calculate_speed(self):
        """根据分数计算游戏速度"""
        # 每 50 分升一级，速度增加
        new_level = (self.score // 50) + 1
        if new_level > self.level:
            self.level = new_level
        
        # 速度随等级提升，最高到 MAX_FPS
        self.current_fps = min(BASE_FPS + (self.level - 1) * 2, MAX_FPS)
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.games_played += 1
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.reset()
                else:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
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
        if self.game_over or self.paused:
            return
        
        self.snake.move()
        
        # 检测吃食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            points = 20 if self.food.type == 'golden' else 10
            self.score += points
            
            # 10% 概率生成金色食物（双倍分数）
            food_type = 'golden' if random.random() < 0.1 else 'normal'
            self.food = Food(self.snake.body, food_type)
            
            # 计算新速度
            self.calculate_speed()
        
        # 检测碰撞
        if self.snake.check_collision():
            self.game_over = True
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        # 绘制网格
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # 绘制游戏对象
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        # 绘制 UI 信息
        self.draw_ui()
        
        # 游戏结束提示
        if self.game_over:
            self.draw_game_over()
        
        # 暂停提示
        if self.paused and not self.game_over:
            self.draw_pause()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """绘制 UI 信息"""
        # 分数
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 等级
        level_text = self.small_font.render(f'Level: {self.level}', True, GOLD)
        self.screen.blit(level_text, (10, 45))
        
        # 速度
        speed_text = self.small_font.render(f'Speed: {self.current_fps} FPS', True, WHITE)
        self.screen.blit(speed_text, (10, 65))
        
        # 最高分
        high_score_text = self.small_font.render(f'Best: {self.high_score}', True, WHITE)
        self.screen.blit(high_score_text, (WINDOW_WIDTH - 120, 10))
        
        # 金色食物说明
        if self.food.type == 'golden':
            golden_text = self.small_font.render('Golden Food! (+20)', True, GOLD)
            self.screen.blit(golden_text, (WINDOW_WIDTH - 180, 45))
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.font.render('GAME OVER', True, RED)
        text_rect1 = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
        self.screen.blit(game_over_text, text_rect1)
        
        # 分数
        score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        text_rect2 = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(score_text, text_rect2)
        
        # 重新开始提示
        restart_text = self.small_font.render('Press SPACE to restart', True, WHITE)
        text_rect3 = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        self.screen.blit(restart_text, text_rect3)
    
    def draw_pause(self):
        """绘制暂停界面"""
        pause_text = self.font.render('PAUSED', True, WHITE)
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(pause_text, text_rect)
    
    def run(self):
        """运行游戏主循环"""
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
    print("🐍 贪吃蛇游戏 v1.1.0")
    print("新增功能：难度递增系统")
    print("控制：方向键或 WASD 移动，空格暂停，ESC 退出")
    print("=" * 50)
    print("特性：")
    print("  • 每 50 分升一级，速度提升")
    print("  • 10% 概率出现金色食物（+20 分）")
    print("  • 显示当前等级和速度")
    print("  • 记录最高分")
    print("=" * 50)
    
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
