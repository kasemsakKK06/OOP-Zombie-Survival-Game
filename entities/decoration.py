"""
Module: decoration.py

SOLID Principle — SRP (Single Responsibility Principle):
    class Decoration รับผิดชอบเฉพาะการแสดงผลของ object ตกแต่งฉาก
    เช่น หญ้า หรือ ถนน โดยไม่มี collision logic

SOLID Principle — LSP (Liskov Substitution Principle):
    class Grass และ Road สืบทอดจาก Decoration
    และสามารถใช้แทน Decoration ได้โดยไม่ทำให้ระบบผิดพลาด
"""

import pygame
import random


class Decoration(pygame.sprite.Sprite):
    """
    Base class สำหรับ object ตกแต่งฉาก
    """

    def __init__(self, x, y, width, height, dec_type="grass"):
        super().__init__()

        # decoration ไม่มี collision
        self.collidable = False

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

        # ─── Grass Decoration ──────────────────────────
        if dec_type == "grass":

            self.image.fill((0, 0, 0, 0))

            for _ in range(int((width * height) / 200)):
                gx = random.randint(0, width - 2)
                gy = random.randint(0, height - 2)

                color = random.choice([(34, 139, 34, 100), (0, 100, 0, 100)])

                pygame.draw.rect(self.image, color, (gx, gy, 4, 4))

        # ─── Road Decoration ───────────────────────────
        elif dec_type == "road":

            self.image.fill((80, 70, 60, 150))

            pygame.draw.rect(
                self.image, (60, 50, 40, 150), (4, 4, width - 8, height - 8), 2
            )

            for _ in range(10):
                rx = random.randint(0, width - 10)
                ry = random.randint(0, height - 10)

                pygame.draw.rect(
                    self.image,
                    (100, 90, 80, 180),
                    (rx, ry, random.randint(5, 15), random.randint(2, 5)),
                )


class Grass(Decoration):
    """
    LSP:
    Grass เป็น Decoration ชนิดหนึ่ง
    """

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "grass")


class Road(Decoration):
    """
    LSP:
    Road เป็น Decoration ชนิดหนึ่ง
    """

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "road")
