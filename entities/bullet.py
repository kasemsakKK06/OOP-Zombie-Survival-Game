"""
Module: bullet.py

SOLID Principle — SRP (Single Responsibility Principle):
    class Bullet รับผิดชอบเฉพาะพฤติกรรมของกระสุน
    เช่น การสร้าง การคำนวณทิศทาง และการเคลื่อนที่

SOLID Principle — LSP (Liskov Substitution Principle):
    Bullet สืบทอดจาก pygame.sprite.Sprite
    จึงสามารถใช้แทน Sprite ได้ใน pygame.sprite.Group
"""

import pygame
import math
from core.settings import YELLOW


class Bullet(pygame.sprite.Sprite):
    """
    Bullet entity

    SRP:
        class นี้ดูแลเฉพาะพฤติกรรมของกระสุน
        (spawn, movement, out-of-map removal)

    LSP:
        สืบทอดจาก pygame.sprite.Sprite
        จึงสามารถใช้ร่วมกับระบบ sprite ของ pygame ได้
    """

    # ระยะ offset จากศูนย์กลางผู้เล่นไปปลายปืน
    GUN_TIP_OFFSET = 26

    def __init__(self, player_cx, player_cy, target_x, target_y, damage=20):
        """
        สร้างกระสุนและคำนวณทิศทางการยิง
        """
        super().__init__()

        length = 14
        thickness = 3
        speed = 12

        # คำนวณทิศทางยิง
        dx = target_x - player_cx
        dy = target_y - player_cy
        dist = math.hypot(dx, dy) or 1

        dir_x = dx / dist
        dir_y = dy / dist

        # จุด spawn ที่ปลายปืน
        spawn_x = player_cx + dir_x * self.GUN_TIP_OFFSET
        spawn_y = player_cy + dir_y * self.GUN_TIP_OFFSET

        # สร้าง sprite กระสุน
        base_image = pygame.Surface((length, thickness), pygame.SRCALPHA)
        pygame.draw.rect(base_image, YELLOW, (0, 0, length, thickness))

        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(base_image, angle)
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))

        # velocity
        self.vx = dir_x * speed
        self.vy = dir_y * speed
        self.damage = damage

    def update(self, map_rect):
        """
        อัปเดตตำแหน่งกระสุน และลบเมื่อออกนอกแผนที่
        """
        self.rect.x += self.vx
        self.rect.y += self.vy

        if not map_rect.colliderect(self.rect):
            self.kill()
