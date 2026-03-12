"""
Module: settings.py

SOLID Principle — SRP (Single Responsibility Principle):
    โมดูลนี้มีหน้าที่เดียว คือเก็บค่าคงที่ (constants) และการตั้งค่าพื้นฐานของเกม
    แบ่งออกเป็น 3 ส่วน:
        1) Screen / Game configuration
        2) Color palette
        3) Pygame display initialization

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเพิ่มค่า config หรือสีใหม่ได้โดยไม่ต้องแก้ไข logic ที่มีอยู่
"""

import pygame

# ─── 1) Screen & Game Configuration ──────────────────────────────────────────
SCREEN_W, SCREEN_H = 1200, 750
FPS = 60
DATA_FILE = "data/players.json"

# ─── 2) Color Palette ───────────────────────────────────────────────────────
# OCP: สามารถเพิ่มสีใหม่ได้โดยไม่ต้องแก้ logic ส่วนอื่น
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 30, 30)
GREEN = (50, 200, 50)
DARK_GREEN = (20, 100, 20)
LIME = (100, 255, 50)
ORANGE = (255, 140, 0)
YELLOW = (255, 220, 0)
GREY = (80, 80, 80)
DARK = (15, 20, 15)
BLOOD = (140, 0, 0)
CYAN = (0, 220, 220)
PURPLE = (150, 0, 200)

# ─── Game Settings (Runtime Config) ─────────────────────────────────────────
# ใช้สำหรับค่าที่ผู้เล่นสามารถปรับได้ เช่น เสียง
GAME_SETTINGS = {
    "music_volume": 0.3,
    "sfx_volume": 0.5,
}

# ─── 3) Pygame Display Initialization ───────────────────────────────────────
# SRP: ส่วนนี้ดูแลการสร้างหน้าต่างเกมเท่านั้น
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Zombie Survival")
clock = pygame.time.Clock()
