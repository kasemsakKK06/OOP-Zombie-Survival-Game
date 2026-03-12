"""
Module: leaderboard_screen.py
SOLID Principle — SRP (Single Responsibility Principle):
    โมดูลนี้รับผิดชอบหน้าที่เดียว คือ แสดงหน้า Leaderboard ของเกม
    ไม่ยุ่งกับ logic อื่น เช่น game logic หรือ data storage

SOLID Principle — DIP (Dependency Inversion Principle):
    ใช้ get_leaderboard จาก data_manager (abstraction) ดึงข้อมูล
    ใช้ Button, draw_text จาก ui_components (abstraction) วาด UI
    ไม่ผูกติดกับ implementation ของ JSON storage โดยตรง
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
    RED,
    GREEN,
    YELLOW,
    ORANGE,
    GREY,
    LIME,
    CYAN,
    GAME_SETTINGS,
)
from core.fonts import font_big, font_med, font_small, font_tiny

# DIP: ขึ้นกับ UI components (abstraction)
from ui.ui_components import Button, draw_text, draw_text_left

# DIP: ขึ้นกับ data_manager (abstraction) ไม่ผูกกับ JSON format
from systems.data_manager import get_leaderboard
from screens.main_menu import draw_bg


def screen_leaderboard():
    """
    SRP: function นี้ทำหน้าที่เดียว คือ จัดการ UI flow ของหน้า Leaderboard
    DIP: ใช้ get_leaderboard ผ่าน abstraction, ใช้ Button ผ่าน abstraction
    """
    tick = 0
    # Load Hover Sound
    hover_sfx = None
    base_path = os.path.dirname(os.path.dirname(__file__))
    s_path = os.path.join(base_path, "assets", "sound", "Menu_hover.wav")
    if os.path.exists(s_path):
        hover_sfx = pygame.mixer.Sound(s_path)
        hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])

    # Load Click Sound
    click_sfx = None
    c_path = os.path.join(base_path, "assets", "sound", "Menu_click.wav")
    if os.path.exists(c_path):
        click_sfx = pygame.mixer.Sound(c_path)
        click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

    # DIP: เรียก get_leaderboard ผ่าน abstraction function
    board = get_leaderboard()
    back = Button(20, 20, 80, 36, "กลับ", GREY)
    scroll = 0
    while True:
        tick += 1
        events = pygame.event.get()
        mx, my = pygame.mouse.get_pos()
        back.update(mx, my)
        # Hover Sound Logic
        if back.rect.collidepoint(mx, my):
            if not getattr(back, "sound_hovered", False):
                if GAME_SETTINGS["sfx_volume"] > 0 and hover_sfx:
                    hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])
                    hover_sfx.play()
                back.sound_hovered = True
        else:
            back.sound_hovered = False

        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if back.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEWHEEL:
                scroll = max(0, min(scroll - event.y, max(0, len(board) - 9)))

        draw_bg(tick)
        draw_text(screen, "ตารางคะแนนสูงสุด", font_big, YELLOW, SCREEN_W // 2, 55)

        headers = ["อันดับ", "ผู้เล่น", "คะแนนสูงสุด", "เล่นแล้ว", "Kills รวม"]
        col_x = [55, 150, 370, 570, 730]
        pygame.draw.rect(
            screen, (30, 50, 20), (25, 95, SCREEN_W - 50, 34), border_radius=4
        )

        for h, cx in zip(headers, col_x):
            draw_text_left(screen, h, font_small, LIME, cx, 100)
        pygame.draw.line(screen, GREEN, (25, 130), (SCREEN_W - 25, 130), 1)

        rank_border = [YELLOW, (192, 192, 192), (205, 127, 50)]
        for idx, p in enumerate(board[scroll : scroll + 10]):
            rank = scroll + idx + 1
            y = 148 + idx * 42
            bg = (25, 45, 15) if idx % 2 == 0 else (15, 30, 10)
            pygame.draw.rect(
                screen, bg, (25, y - 14, SCREEN_W - 50, 36), border_radius=4
            )
            if rank <= 3:
                pygame.draw.rect(
                    screen,
                    rank_border[rank - 1],
                    (25, y - 14, SCREEN_W - 50, 36),
                    2,
                    border_radius=4,
                )

            medals = ["1", "2", "3"]
            rank_txt = medals[rank - 1] if rank <= 3 else f"#{rank}"
            color_name = CYAN if rank <= 3 else WHITE
            draw_text_left(
                screen,
                rank_txt,
                font_small,
                YELLOW if rank <= 3 else WHITE,
                col_x[0],
                y - 10,
            )
            draw_text_left(
                screen, p["username"], font_small, color_name, col_x[1], y - 10
            )
            draw_text_left(
                screen, str(p["best_score"]), font_small, YELLOW, col_x[2], y - 10
            )
            draw_text_left(
                screen, str(p["games_played"]), font_small, WHITE, col_x[3], y - 10
            )
            draw_text_left(
                screen, str(p["total_kills"]), font_small, ORANGE, col_x[4], y - 10
            )

        if not board:
            draw_text(
                screen, "ยังไม่มีข้อมูลผู้เล่น", font_med, GREY, SCREEN_W // 2, SCREEN_H // 2
            )

        back.draw(screen)
        draw_text(
            screen,
            f"ผู้เล่นทั้งหมด {len(board)} คน",
            font_tiny,
            GREY,
            SCREEN_W // 2,
            SCREEN_H - 18,
            False,
        )
        pygame.display.flip()
        clock.tick(FPS)
