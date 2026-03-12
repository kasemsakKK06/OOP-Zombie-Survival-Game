"""
Module: particle.py

SOLID Principle — SRP (Single Responsibility Principle):
    class Particle รับผิดชอบเฉพาะ visual particle effect
    เช่น การสร้าง การเคลื่อนที่ และการวาดอนุภาค

SOLID Principle — OCP (Open/Closed Principle):
    สามารถสร้าง subclass เพื่อเพิ่มรูปแบบ particle ใหม่ได้
    โดยไม่ต้องแก้ไข class Particle เดิม
"""

import pygame
import random
import math


class Particle:
    """
    Base particle class
    """

    def __init__(self, x, y, color):
        # position
        self.x, self.y = float(x), float(y)

        # velocity
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, 1)

        # lifetime
        self.life = random.randint(20, 40)

        self.color = color
        self.size = random.randint(2, 5)

    def update(self):
        """Update particle physics"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.life -= 1

    def draw(self, surf):
        """Render particle with alpha fading"""
        alpha = max(0, int(255 * self.life / 40))

        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            s,
            (*self.color, alpha),
            (self.size, self.size),
            self.size,
        )

        surf.blit(s, (int(self.x) - self.size, int(self.y) - self.size))


class BloodParticle(Particle):
    """
    Specialized particle for blood splatter
    """

    def __init__(self, x, y, color, direction_angle, speed_mult=1.0):

        self.x, self.y = float(x), float(y)

        angle_rad = math.radians(direction_angle) + random.uniform(-0.5, 0.5)
        speed = random.uniform(2, 6) * speed_mult

        self.vx = math.cos(angle_rad) * speed
        self.vy = math.sin(angle_rad) * speed

        self.life = random.randint(40, 70)
        self.max_life = self.life

        self.color = color
        self.size = random.uniform(2, 6)

        self.gravity = 0.15

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity
        self.life -= 1

        # air resistance
        self.vx *= 0.98

        # shrink over time
        self.size = max(0, self.size - 0.08)

    def draw(self, surf):
        if self.life <= 0 or self.size <= 0:
            return

        alpha = int(255 * (self.life / self.max_life) ** 1.5)

        current_size = int(self.size)

        pygame.draw.rect(
            surf,
            (*self.color, alpha),
            (self.x, self.y, current_size, current_size),
        )
