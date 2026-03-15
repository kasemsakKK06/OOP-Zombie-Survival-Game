"""
Module: obstacle.py

SOLID Principle — SRP (Single Responsibility Principle):
    class Obstacle รับผิดชอบเฉพาะข้อมูลและการแสดงผลของสิ่งกีดขวาง
    เช่น กำแพง หิน หรือสิ่งปลูกสร้าง

SOLID Principle — LSP (Liskov Substitution Principle):
    Obstacle สืบทอดจาก pygame.sprite.Sprite
    จึงสามารถใช้แทน Sprite ในระบบ collision ของ pygame ได้
"""

import pygame


class Obstacle(pygame.sprite.Sprite):
    """Entity สำหรับสิ่งกีดขวางในแผนที่"""

    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # วาดขอบเพื่อให้ดูเป็นกำแพง
        pygame.draw.rect(
            self.image,
            (
                max(0, color[0] - 30),
                max(0, color[1] - 30),
                max(0, color[2] - 30),
            ),
            (0, 0, width, height),
            3,
        )

        self.rect = self.image.get_rect(topleft=(x, y))
