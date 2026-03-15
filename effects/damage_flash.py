"""
Module: damage_flash.py

SOLID Principle — SRP (Single Responsibility Principle):
    class DamageFlash รับผิดชอบเฉพาะ visual effect
    ที่ทำให้หน้าจอกระพริบสีแดงเมื่อ player โดนโจมตี
"""

import pygame


class DamageFlash:
    """
    Screen damage flash effect

    SRP:
        class นี้ดูแลเฉพาะ visual feedback
        เมื่อผู้เล่นได้รับ damage
    """

    def __init__(self, screen_size):
        self.max_duration = 20
        self.duration = 0

        self.surface = pygame.Surface(screen_size, pygame.SRCALPHA)

    def trigger(self):
        """เรียกใช้เมื่อ player โดนโจมตี"""
        self.duration = self.max_duration

    def update(self):
        """อัปเดตความจางของ effect"""
        if self.duration > 0:

            alpha = int(120 * (self.duration / self.max_duration))

            self.surface.fill((0, 0, 0, 0))

            self.surface.fill((255, 0, 0, alpha))

            self.duration -= 1

    def draw(self, screen):
        """วาด effect ลงหน้าจอ"""
        if self.duration > 0:
            screen.blit(self.surface, (0, 0))
