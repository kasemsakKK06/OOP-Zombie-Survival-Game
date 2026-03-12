"""
Module: powerup.py
SOLID Principle — SRP (Single Responsibility Principle):
    class PowerUp รับผิดชอบหน้าที่เดียว คือ จัดการไอเทมเก็บของในเกม
    (สร้างตามประเภท, แสดงผล, นับเวลาหมดอายุ)

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเพิ่มประเภท power-up ใหม่ได้โดยเพิ่มข้อมูลใน TYPES list
    โดยไม่ต้องแก้ไข logic ใน __init__ หรือ update

SOLID Principle — LSP (Liskov Substitution Principle):
    PowerUp สืบทอดจาก pygame.sprite.Sprite และสามารถใช้แทน Sprite ได้ทุกที่
    เช่น spritecollide(), Group operations ฯลฯ
"""

import pygame
import random
from core.settings import RED, CYAN, YELLOW, WHITE, BLACK
from core.fonts import font_tiny


class PowerUp(pygame.sprite.Sprite):
    """
    SRP: class นี้รับผิดชอบเฉพาะ "power-up" — สร้างตามประเภท, แสดงผล, หมดอายุ
    OCP: เพิ่มประเภท power-up ใหม่ได้ผ่าน TYPES list โดยไม่แก้ logic
    LSP: สืบทอด Sprite — ใช้แทน Sprite ได้ใน spritecollide(), Group ฯลฯ
    """

    # OCP: เพิ่มประเภท power-up ใหม่ได้โดยเพิ่ม dict เข้า list นี้
    # OCP + Data-Driven Design:
    # ประเภทของ power-up ถูกกำหนดเป็นข้อมูล
    # ทำให้สามารถเพิ่มชนิดใหม่ได้โดยไม่ต้องแก้ logic ของ class
    TYPES = [
        {"label": "HP", "color": RED, "effect": "hp"},
        {"label": "SPD", "color": CYAN, "effect": "speed"},
        {"label": "RFR", "color": YELLOW, "effect": "rapid"},
    ]

    def __init__(self, x, y):
        """
        SRP: constructor จัดการแค่การสร้าง power-up ตามประเภทแบบสุ่ม
        OCP: ใช้ TYPES list จึงเพิ่มประเภทใหม่ได้โดยไม่แก้ method นี้
        """
        super().__init__()
        t = random.choice(self.TYPES)
        self.effect = t["effect"]
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, t["color"], (0, 0, 28, 28), border_radius=5)
        pygame.draw.rect(self.image, WHITE, (0, 0, 28, 28), 2, border_radius=5)

        # SRP: แสดง label ของ power-up เพื่อให้ผู้เล่นรู้ว่าไอเทมนี้คืออะไร
        lbl = font_tiny.render(t["label"], True, BLACK)
        self.image.blit(lbl, (14 - lbl.get_width() // 2, 14 - lbl.get_height() // 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 300

    def update(self):
        """SRP: method นี้ทำหน้าที่เดียว คือ นับเวลาและลบตัวเองเมื่อหมดอายุ"""
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            # LSP: ใช้ method ของ pygame.sprite.Sprite
            # เพื่อลบ object ออกจาก sprite groups ทั้งหมด
