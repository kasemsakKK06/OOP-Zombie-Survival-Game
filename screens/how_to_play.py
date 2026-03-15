"""
Module: how_to_play.py
SOLID Principle — SRP: รับผิดชอบหน้าที่เดียวคือแสดงหน้าจอสอนวิธีการเล่น
"""

import pygame
import os
from core.settings import (
    screen,
    clock,
    SCREEN_W,
    SCREEN_H,
    FPS,
    WHITE,
    YELLOW,
    LIME,
    CYAN,
    GREY,
    ORANGE,
    GAME_SETTINGS,
)
from core.fonts import font_big, font_med, font_small
from ui.ui_components import Button, draw_text, draw_text_left, draw_panel
from screens.main_menu import draw_bg


def screen_how_to_play():
    """แสดงหน้าจอวิธีการเล่น (Controls)"""
    tick = 0
    # Load Hover Sound
    hover_sfx = None
    base_path = os.path.dirname(os.path.dirname(__file__))
    s_path = os.path.join(base_path, "assets", "sound", "Menu_hover.wav")
    if os.path.exists(s_path):
        hover_sfx = pygame.mixer.Sound(s_path)
        hover_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

    # Load Click Sound
    click_sfx = None
    c_path = os.path.join(base_path, "assets", "sound", "Menu_click.wav")
    if os.path.exists(c_path):
        click_sfx = pygame.mixer.Sound(c_path)
        click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

    back_btn = Button(20, 20, 80, 36, "กลับ", GREY)

    while True:
        tick += 1
        events = pygame.event.get()
        mx, my = pygame.mouse.get_pos()

        back_btn.update(mx, my)

        # Hover Sound Logic
        if back_btn.rect.collidepoint(mx, my):
            if not getattr(back_btn, "sound_hovered", False):
                if GAME_SETTINGS["sfx_volume"] > 0 and hover_sfx:
                    hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])
                    hover_sfx.play()
                back_btn.sound_hovered = True
        else:
            back_btn.sound_hovered = False

        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if back_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        draw_bg(tick)

        # Title
        draw_text(screen, "How to Play", font_big, YELLOW, SCREEN_W // 2, 60)

        # Main Panel
        panel_w = 700
        panel_h = 420
        px = SCREEN_W // 2 - panel_w // 2
        py = SCREEN_H // 2 - panel_h // 2 + 20

        draw_panel(screen, (px, py, panel_w, panel_h), color=(20, 30, 25))

        # Instructions Data: (Key, Description, Color)
        controls = [
            ("W A S D", "เคลื่อนที่ตัวละคร (บน, ซ้าย, ล่าง, ขวา)", LIME),
            ("Mouse Left", "ยิงปืน / โจมตี", ORANGE),
            ("1 - 4", "สลับอาวุธ (Rifle, Pistol, Shotgun, Knife)", CYAN),
            ("ESC", "หยุดเกม / เมนูหลัก", GREY),
        ]

        start_y = py + 50
        gap = 70

        for i, (key, desc, col) in enumerate(controls):
            y = start_y + i * gap
            # Key column
            draw_text_left(screen, key, font_med, col, px + 60, y)
            # Desc column
            draw_text_left(screen, desc, font_small, WHITE, px + 280, y + 8)

            # Divider line
            if i < len(controls) - 1:
                pygame.draw.line(
                    screen,
                    (40, 60, 40),
                    (px + 40, y + 45),
                    (px + panel_w - 40, y + 45),
                )

        # Tips at bottom
        draw_text(
            screen,
            "Tip: เก็บ Power-up เพื่อเพิ่มพลังและคะแนน!",
            font_small,
            YELLOW,
            SCREEN_W // 2,
            py + panel_h - 40,
        )

        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
