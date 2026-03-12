"""
Module: fonts.py

Purpose:
    จัดการ Font ของโปรเจกต์ผ่าน FontManager เพื่อให้ส่วนอื่นของเกม
    สามารถสร้าง font ได้ง่าย โดยไม่ต้องเขียน logic ซ้ำ

SOLID Principles
----------------
SRP (Single Responsibility Principle)
    FontManager มีหน้าที่เดียว คือ ค้นหาและสร้าง pygame font objects

OCP (Open/Closed Principle)
    สามารถเพิ่ม font path ใหม่ได้ผ่าน `_FONT_CANDIDATES`
    และเพิ่ม fallback fonts ผ่าน `_FALLBACK_FONTS`
    โดยไม่ต้องแก้ไข logic ภายใน method
"""

import os
import pygame


class FontManager:
    """
    Font resource manager ของโปรเจกต์

    SRP:
        รับผิดชอบเฉพาะการค้นหาและสร้าง font objects

    OCP:
        สามารถเพิ่ม font path หรือ fallback fonts ใหม่ได้
        โดยไม่ต้องแก้ logic ภายใน class
    """

    # Candidate fonts สำหรับรองรับหลาย OS
    _FONT_CANDIDATES = [
        # Recommended (Game UI)
        "/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansThai-Regular.ttf",
        # Windows
        "C:/Windows/Fonts/leelawad.ttf",
        # Linux
        "/usr/share/fonts/opentype/tlwg/Loma.otf",
        "/usr/share/fonts/opentype/tlwg/Loma-Bold.otf",
        "/usr/share/fonts/truetype/tlwg/Loma.ttf",
        # macOS
        "/Library/Fonts/Thonburi.ttf",
        # Final fallback
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/angsana.ttc",
    ]

    # Fallback system fonts
    _FALLBACK_FONTS = ["tahoma", "arial", "freesans", "dejavusans"]

    def __init__(self):
        """ค้นหา Thai font path ครั้งเดียวและเก็บไว้ใช้ซ้ำ"""
        self._thai_font_path = self._find_thai_font()

    def _find_thai_font(self):
        """
        ค้นหา Thai font จาก candidate paths
        """
        for path in self._FONT_CANDIDATES:
            if os.path.exists(path):
                return path
        return None

    def make_font(self, size: int, bold: bool = False):
        """
        สร้าง pygame.font.Font object

        Args:
            size: ขนาดตัวอักษร
            bold: ใช้ font หนาหรือไม่

        Returns:
            pygame.font.Font
        """

        # ใช้ Thai font ถ้าพบ
        if self._thai_font_path:
            try:
                return pygame.font.Font(self._thai_font_path, size)
            except Exception:
                pass

        # ลอง fallback system fonts
        for name in self._FALLBACK_FONTS:
            try:
                return pygame.font.SysFont(name, size, bold=bold)
            except Exception:
                continue

        # fallback สุดท้าย
        return pygame.font.Font(None, size)


# ──────────────────────────────────────────────
# Shared FontManager instance (Singleton-like)
# ใช้ instance เดียวทั้งโปรเจกต์
# ──────────────────────────────────────────────

_font_manager = FontManager()


# Predefined fonts สำหรับ UI
font_big = _font_manager.make_font(46, bold=True)
font_med = _font_manager.make_font(28, bold=True)
font_small = _font_manager.make_font(20)
font_tiny = _font_manager.make_font(15)
