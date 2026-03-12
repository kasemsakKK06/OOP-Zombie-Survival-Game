"""
Module: ui_components.py
SOLID Principle — SRP (Single Responsibility Principle):
    แยกหน้าที่ออกเป็น:
      - Free functions: draw_text(), draw_text_left(), draw_panel() — รับผิดชอบการวาด UI ทั่วไป
      - class Button: รับผิดชอบเฉพาะพฤติกรรมปุ่มกด
      - class InputBox: รับผิดชอบเฉพาะพฤติกรรมช่องป้อนข้อความ

SOLID Principle — OCP (Open/Closed Principle):
    สามารถ extend Button หรือ InputBox ด้วย subclass ได้
    โดยไม่ต้องแก้ไข class เดิม (เช่น IconButton, PasswordBox)

SOLID Principle — ISP (Interface Segregation Principle):
    Button และ InputBox แยก interface กัน — ผู้ใช้ Button ไม่ต้องรู้จัก InputBox และกลับกัน
"""

import pygame
from core.settings import BLACK, WHITE, GREEN, LIME, DARK_GREEN, GREY, CYAN
from core.fonts import font_small, font_tiny


# ─── Free Functions (SRP: แต่ละ function ดูแลการวาด UI หนึ่งอย่าง) ──────────


def draw_text(surf, text, font, color, cx, cy, shadow=True):
    """SRP: function นี้ทำหน้าที่เดียว คือ วาดข้อความแบบ center-aligned พร้อม shadow"""
    if shadow:
        s = font.render(text, True, BLACK)
        surf.blit(s, s.get_rect(center=(cx + 2, cy + 2)))
    r = font.render(text, True, color)
    surf.blit(r, r.get_rect(center=(cx, cy)))


def draw_text_left(surf, text, font, color, x, y):
    """SRP: function นี้ทำหน้าที่เดียว คือ วาดข้อความแบบ left-aligned"""
    r = font.render(text, True, color)
    surf.blit(r, (x, y))


def draw_panel(surf, rect, color=(20, 35, 20), border=GREEN, alpha=200):
    """SRP: function นี้ทำหน้าที่เดียว คือ วาด panel พื้นหลังแบบ semi-transparent"""
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    s.fill((*color, alpha))
    surf.blit(s, (rect[0], rect[1]))
    pygame.draw.rect(surf, border, rect, 2, border_radius=8)


# ─── Button Class ────────────────────────────────────────────────────────────


class Button:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ จัดการปุ่มกด (แสดงผล, ตรวจ hover, ตรวจคลิก)
    OCP: สามารถ extend ด้วย subclass ได้ (เช่น IconButton, AnimatedButton)
    ISP: แยก interface จาก InputBox — ผู้ใช้ Button ไม่ต้องรู้จัก InputBox
    """

    def __init__(self, x, y, w, h, text, color=DARK_GREEN, hover_color=GREEN):
        """SRP: constructor จัดการแค่การกำหนดค่าเริ่มต้นของปุ่ม"""
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surf):
        """SRP: method นี้ทำหน้าที่เดียว คือ วาดปุ่มลงบน surface"""
        col = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=8)
        border_col = GREEN if self.hovered else LIME
        pygame.draw.rect(surf, border_col, self.rect, 2, border_radius=8)
        draw_text(
            surf, self.text, font_small, WHITE, self.rect.centerx, self.rect.centery
        )

    def update(self, mx, my):
        """SRP: method นี้ทำหน้าที่เดียว คือ ตรวจสอบสถานะ hover ของเมาส์"""
        self.hovered = self.rect.collidepoint(mx, my)

    def clicked(self, event):
        """SRP: method นี้ทำหน้าที่เดียว คือ ตรวจสอบว่าปุ่มถูกคลิกหรือไม่"""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            event.pos
        )


# ─── InputBox Class ──────────────────────────────────────────────────────────


class InputBox:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ จัดการช่องป้อนข้อความ (รับ input, แสดงผล)
    OCP: สามารถ extend ด้วย subclass ได้ (เช่น NumericInputBox, EmailInputBox)
    ISP: แยก interface จาก Button — ผู้ใช้ InputBox ไม่ต้องรู้จัก Button
    """

    def __init__(self, x, y, w, h, placeholder="", password=False):
        """SRP: constructor จัดการแค่การกำหนดค่าเริ่มต้นของช่อง input"""
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.password = password

    def handle(self, event):
        """SRP: method นี้ทำหน้าที่เดียว คือ จัดการ event ที่เกี่ยวกับ input"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.text) < 20:
                self.text += event.unicode

    def draw(self, surf):
        """SRP: method นี้ทำหน้าที่เดียว คือ วาดช่อง input ลงบน surface"""
        border = CYAN if self.active else GREY
        pygame.draw.rect(surf, (10, 20, 10), self.rect, border_radius=6)
        pygame.draw.rect(surf, border, self.rect, 2, border_radius=6)
        show = "*" * len(self.text) if self.password else self.text
        if self.text:
            t = font_small.render(show, True, WHITE)
        else:
            t = font_small.render(self.placeholder, True, GREY)
        surf.blit(t, (self.rect.x + 8, self.rect.centery - t.get_height() // 2))
