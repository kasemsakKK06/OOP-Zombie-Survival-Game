"""
Module: settings_screen.py
SRP: รับผิดชอบหน้าจอตั้งค่าเกม (เปิด/ปิด เสียง)
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
    GREY,
    GREEN,
    RED,
    ORANGE,
    CYAN,
    GAME_SETTINGS,
)
from core.fonts import font_big, font_med, font_small
from ui.ui_components import Button, draw_text, draw_panel
from screens.main_menu import draw_bg


class Slider:
    """
    SRP: รับผิดชอบการแสดงผลและจัดการ input ของ Slider bar
    OCP: สามารถปรับเปลี่ยนสีหรือขนาดได้ผ่าน constructor
    """

    def __init__(self, x, y, w, h, initial_val, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.val = initial_val
        self.color = color
        self.dragging = False

    def handle_event(self, event):
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_val(event.pos[0])
                changed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_val(event.pos[0])
                changed = True
        return changed

    def update_val(self, mouse_x):
        rel_x = mouse_x - self.rect.x
        self.val = max(0.0, min(1.0, rel_x / self.rect.width))

    def draw(self, surf):
        # Background track
        pygame.draw.rect(surf, (40, 40, 40), self.rect, border_radius=10)
        # Fill
        fill_w = int(self.rect.width * self.val)
        if fill_w > 0:
            pygame.draw.rect(
                surf,
                self.color,
                (self.rect.x, self.rect.y, fill_w, self.rect.height),
                border_radius=10,
            )
        # Border
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=10)
        # Knob (ปุ่มจับ)
        knob_x = self.rect.x + fill_w
        pygame.draw.circle(
            surf, WHITE, (knob_x, self.rect.centery), self.rect.height // 2 + 3
        )


def screen_settings():
    tick = 0

    # Load Sounds (โหลดเสียงเพื่อใช้ในหน้านี้)
    hover_sfx = None
    click_sfx = None
    base_path = os.path.dirname(os.path.dirname(__file__))

    s_path = os.path.join(base_path, "assets", "sound", "Menu_hover.wav")
    if os.path.exists(s_path):
        hover_sfx = pygame.mixer.Sound(s_path)
        hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])

    c_path = os.path.join(base_path, "assets", "sound", "Menu_click.wav")
    if os.path.exists(c_path):
        click_sfx = pygame.mixer.Sound(c_path)
        click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

    # UI Setup
    cx = SCREEN_W // 2
    cy = SCREEN_H // 2

    back_btn = Button(20, 20, 80, 36, "กลับ", GREY)

    # Sliders
    music_slider = Slider(
        cx - 100, cy - 40, 200, 20, GAME_SETTINGS["music_volume"], GREEN
    )
    sfx_slider = Slider(cx - 100, cy + 50, 200, 20, GAME_SETTINGS["sfx_volume"], YELLOW)

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

            if back_btn.clicked(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "menu"

            # --- Slider Events ---
            if music_slider.handle_event(event):
                GAME_SETTINGS["music_volume"] = music_slider.val
                pygame.mixer.music.set_volume(GAME_SETTINGS["music_volume"])

            if sfx_slider.handle_event(event):
                GAME_SETTINGS["sfx_volume"] = sfx_slider.val
                # Update loaded sounds volume immediately
                if hover_sfx:
                    hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])
                if click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

        draw_bg(tick)

        # วาดกรอบพื้นหลัง
        draw_panel(screen, (cx - 200, cy - 100, 400, 250), color=(20, 30, 35))
        draw_text(screen, "Settings", font_big, YELLOW, cx, cy - 130)

        # วาดแถบ Music
        draw_text(
            screen,
            f"Music: {int(GAME_SETTINGS['music_volume']*100)}%",
            font_med,
            CYAN,
            cx,
            cy - 65,
        )
        music_slider.draw(screen)

        # วาดแถบ SFX
        draw_text(
            screen,
            f"SFX: {int(GAME_SETTINGS['sfx_volume']*100)}%",
            font_med,
            ORANGE,
            cx,
            cy + 25,
        )
        sfx_slider.draw(screen)

        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
