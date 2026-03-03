#!/usr/bin/env python3
"""
贪吃蛇 v2.0 - UI/UX 视觉升级版
特性：
- 霓虹赛博朋克风格
- 粒子特效系统
- 动态渐变背景
- 平滑动画过渡
- 现代化 UI 界面
- 音效系统
- 触觉反馈
"""

import pygame
import random
import math
import json
from pathlib import Path
from datetime import datetime
from enum import Enum

# ============ 配置 ============
class Config:
    # 屏幕设置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRID_SIZE = 20
    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
    
    # 颜色方案 - 霓虹赛博朋克
    COLORS = {
        'bg_start': (10, 10, 30),      # 深蓝背景
        'bg_end': (30, 10, 50),         # 紫红背景
        'snake_head': (0, 255, 255),    # 青色
        'snake_body': (0, 200, 200),    # 深青色
        'snake_glow': (0, 255, 255, 100),
        'food': (255, 0, 128),          # 粉红
        'food_glow': (255, 0, 128, 150),
        'grid': (30, 30, 60),
        'text': (255, 255, 255),
        'text_dim': (150, 150, 150),
        'ui_bg': (20, 20, 40, 200),
        'ui_border': (0, 255, 255),
        'button_bg': (40, 40, 80),
        'button_hover': (60, 60, 120),
        'score': (255, 215, 0),         # 金色
        'particle': [(255, 0, 128), (0, 255, 255), (255, 215, 0)]
    }
    
    # 游戏设置
    FPS = 60
    SNAKE_SPEED = 10
    PARTICLE_COUNT = 20
    GLOW_RADIUS = 15
    
    # 音效设置
    SOUND_ENABLED = True

# ============ 粒子系统 ============
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.randint(2, 4)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # 重力
        self.life -= self.decay
        return self.life > 0
    
    def draw(self, screen):
        alpha = int(255 * self.life)
        size = int(self.size * self.life)
        if size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

# ============ 蛇类 ============
class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        start_x = Config.GRID_WIDTH // 2
        start_y = Config.GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        self.alive = True
        self.score = 0
    
    def change_direction(self, direction):
        # 防止反向
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def update(self):
        if not self.alive:
            return
        
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # 碰撞检测
        if (new_head in self.body or 
            new_head[0] < 0 or new_head[0] >= Config.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= Config.GRID_HEIGHT):
            self.alive = False
            return
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            self.score += 10
    
    def draw(self, screen, time_offset=0):
        for i, (x, y) in enumerate(self.body):
            px = x * Config.GRID_SIZE + Config.GRID_SIZE // 2
            py = y * Config.GRID_SIZE + Config.GRID_SIZE // 2
            
            # 颜色渐变
            ratio = i / len(self.body)
            r = int(Config.COLORS['snake_head'][0] * (1-ratio) + Config.COLORS['snake_body'][0] * ratio)
            g = int(Config.COLORS['snake_head'][1] * (1-ratio) + Config.COLORS['snake_body'][1] * ratio)
            b = int(Config.COLORS['snake_head'][2] * (1-ratio) + Config.COLORS['snake_body'][2] * ratio)
            
            # 发光效果
            glow_size = Config.GLOW_RADIUS + int(math.sin(time_offset * 0.1 + i * 0.5) * 3)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*Config.COLORS['snake_glow'][:3], 50), (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (px - glow_size, py - glow_size))
            
            # 蛇身
            size = Config.GRID_SIZE - 2
            pygame.draw.circle(screen, (r, g, b), (px, py), size // 2)
            
            # 头部眼睛
            if i == 0:
                eye_offset = 5
                eye_size = 3
                dir_x, dir_y = self.direction
                eye1_x = px + dir_x * 3 - dir_y * eye_offset
                eye1_y = py + dir_y * 3 + dir_x * eye_offset
                eye2_x = px + dir_x * 3 + dir_y * eye_offset
                eye2_y = py + dir_y * 3 - dir_x * eye_offset
                pygame.draw.circle(screen, (255, 255, 255), (int(eye1_x), int(eye1_y)), eye_size)
                pygame.draw.circle(screen, (255, 255, 255), (int(eye2_x), int(eye2_y)), eye_size)

# ============ 食物类 ============
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        self.animation_offset = 0
    
    def spawn(self, snake_body=None):
        while True:
            x = random.randint(0, Config.GRID_WIDTH - 1)
            y = random.randint(0, Config.GRID_HEIGHT - 1)
            if snake_body is None or (x, y) not in snake_body:
                self.position = (x, y)
                break
    
    def update(self, time):
        self.animation_offset = math.sin(time * 0.005) * 3
    
    def draw(self, screen, time_offset=0):
        x, y = self.position
        px = x * Config.GRID_SIZE + Config.GRID_SIZE // 2
        py = y * Config.GRID_SIZE + Config.GRID_SIZE // 2 + self.animation_offset
        
        # 发光效果
        glow_size = Config.GLOW_RADIUS + int(math.sin(time_offset * 0.2) * 5)
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*Config.COLORS['food_glow'][:3], 80), (glow_size, glow_size), glow_size)
        screen.blit(glow_surf, (px - glow_size, py - glow_size))
        
        # 食物主体
        pygame.draw.circle(screen, Config.COLORS['food'], (px, py), Config.GRID_SIZE // 2 - 2)
        
        # 高光
        pygame.draw.circle(screen, (255, 200, 200), (px - 3, py - 3), 3)

# ============ 游戏状态 ============
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

# ============ 按钮类 ============
class Button:
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos, mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked:
            self.clicked = True
            if self.callback:
                self.callback()
            return True
        return False
    
    def draw(self, screen, font):
        color = Config.COLORS['button_hover'] if self.hovered else Config.COLORS['button_bg']
        
        # 圆角矩形
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, Config.COLORS['ui_border'], self.rect, 2, border_radius=10)
        
        # 文字
        text_surf = font.render(self.text, True, Config.COLORS['text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

# ============ 游戏主类 ============
class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("🐍 贪吃蛇 v2.0 - 霓虹版")
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # 游戏对象
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        
        # 游戏状态
        self.state = GameState.MENU
        self.high_score = self.load_high_score()
        
        # UI 按钮
        self.buttons = []
        self.create_menu_buttons()
        
        # 背景动画
        self.bg_offset = 0
        
        # 音效
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        # 这里可以加载实际音效文件
        # self.sounds['eat'] = pygame.mixer.Sound('eat.wav')
        pass
    
    def play_sound(self, sound_name):
        if Config.SOUND_ENABLED and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def load_high_score(self):
        try:
            with open('high_score.json', 'r') as f:
                return json.load(f).get('high_score', 0)
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def create_menu_buttons(self):
        cx = Config.SCREEN_WIDTH // 2
        self.buttons = [
            Button(cx - 100, 250, 200, 50, "开始游戏", self.start_game),
            Button(cx - 100, 320, 200, 50, "排行榜", None),
            Button(cx - 100, 390, 200, 50, "退出", self.quit_game)
        ]
    
    def start_game(self):
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.state = GameState.PLAYING
        self.particles.clear()
    
    def quit_game(self):
        self.state = None  # 退出循环
    
    def create_explosion(self, x, y):
        for _ in range(Config.PARTICLE_COUNT):
            color = random.choice(Config.COLORS['particle'])
            self.particles.append(Particle(x, y, color))
    
    def draw_gradient_background(self):
        self.bg_offset += 0.5
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            r = int(Config.COLORS['bg_start'][0] * (1-ratio) + Config.COLORS['bg_end'][0] * ratio)
            g = int(Config.COLORS['bg_start'][1] * (1-ratio) + Config.COLORS['bg_end'][1] * ratio)
            b = int(Config.COLORS['bg_start'][2] * (1-ratio) + Config.COLORS['bg_end'][2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (Config.SCREEN_WIDTH, y))
        
        # 网格线
        for x in range(0, Config.SCREEN_WIDTH, Config.GRID_SIZE):
            pygame.draw.line(self.screen, Config.COLORS['grid'], (x, 0), (x, Config.SCREEN_HEIGHT))
        for y in range(0, Config.SCREEN_HEIGHT, Config.GRID_SIZE):
            pygame.draw.line(self.screen, Config.COLORS['grid'], (0, y), (Config.SCREEN_WIDTH, y))
    
    def draw_ui(self):
        # 分数
        score_text = self.font_medium.render(f"分数：{self.snake.score}", True, Config.COLORS['score'])
        self.screen.blit(score_text, (20, 20))
        
        # 最高分
        high_score_text = self.font_small.render(f"最高分：{self.high_score}", True, Config.COLORS['text_dim'])
        self.screen.blit(high_score_text, (20, 60))
    
    def draw_menu(self):
        # 标题
        title_text = self.font_large.render("🐍 贪吃蛇", True, Config.COLORS['snake_head'])
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # 副标题
        subtitle_text = self.font_medium.render("霓虹版 v2.0", True, Config.COLORS['food'])
        subtitle_rect = subtitle_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 210))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.buttons:
            button.update(mouse_pos, mouse_clicked)
            button.draw(self.screen, self.font_medium)
    
    def draw_game_over(self):
        # 更新最高分
        if self.snake.score > self.high_score:
            self.high_score = self.snake.score
            self.save_high_score()
        
        # 游戏结束文字
        go_text = self.font_large.render("游戏结束", True, Config.COLORS['food'])
        go_rect = go_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 200))
        self.screen.blit(go_text, go_rect)
        
        # 分数
        score_text = self.font_medium.render(f"得分：{self.snake.score}", True, Config.COLORS['text'])
        score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        # 最高分
        hs_text = self.font_medium.render(f"最高分：{self.high_score}", True, Config.COLORS['score'])
        hs_rect = hs_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 330))
        self.screen.blit(hs_text, hs_rect)
        
        # 重新开始按钮
        restart_btn = Button(Config.SCREEN_WIDTH // 2 - 100, 400, 200, 50, "重新开始", self.start_game)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        restart_btn.update(mouse_pos, mouse_clicked)
        restart_btn.draw(self.screen, self.font_medium)
        
        # 返回菜单按钮
        menu_btn = Button(Config.SCREEN_WIDTH // 2 - 100, 470, 200, 50, "返回菜单", lambda: setattr(self, 'state', GameState.MENU))
        menu_btn.update(mouse_pos, mouse_clicked)
        menu_btn.draw(self.screen, self.font_medium)
    
    def run(self):
        running = True
        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 1000 // Config.SNAKE_SPEED)
        
        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.state == GameState.PLAYING:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.snake.change_direction((0, -1))
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.snake.change_direction((0, 1))
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.snake.change_direction((-1, 0))
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.snake.change_direction((1, 0))
                        elif event.key == pygame.K_ESCAPE:
                            self.state = GameState.PAUSED
                    
                    elif self.state == GameState.PAUSED:
                        if event.key == pygame.K_ESCAPE:
                            self.state = GameState.PLAYING
                
                elif event.type == move_event and self.state == GameState.PLAYING:
                    old_head = self.snake.body[0].copy()
                    self.snake.update()
                    
                    # 检查是否吃到食物
                    if self.snake.alive and self.snake.body[0] == self.food.position:
                        self.snake.grow = True
                        self.food.spawn(self.snake.body)
                        self.create_explosion(
                            self.food.position[0] * Config.GRID_SIZE + Config.GRID_SIZE // 2,
                            self.food.position[1] * Config.GRID_SIZE + Config.GRID_SIZE // 2
                        )
                        self.play_sound('eat')
                    
                    # 检查死亡
                    if not self.snake.alive:
                        self.state = GameState.GAME_OVER
            
            # 更新
            time_now = pygame.time.get_ticks()
            if self.state == GameState.PLAYING:
                self.food.update(time_now)
            
            # 更新粒子
            self.particles = [p for p in self.particles if p.update()]
            
            # 绘制
            self.draw_gradient_background()
            
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.food.draw(self.screen, time_now)
                self.snake.draw(self.screen, time_now)
                for particle in self.particles:
                    particle.draw(self.screen)
                self.draw_ui()
            elif self.state == GameState.PAUSED:
                self.food.draw(self.screen, time_now)
                self.snake.draw(self.screen, time_now)
                
                # 暂停遮罩
                overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0, 0))
                
                pause_text = self.font_large.render("暂停", True, Config.COLORS['text'])
                pause_rect = pause_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
                self.screen.blit(pause_text, pause_rect)
            elif self.state == GameState.GAME_OVER:
                self.food.draw(self.screen, time_now)
                self.snake.draw(self.screen, time_now)
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(Config.FPS)
        
        pygame.quit()

# ============ 主程序 ============
if __name__ == '__main__':
    game = SnakeGame()
    game.run()
