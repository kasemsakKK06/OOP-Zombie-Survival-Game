"""
Module: main_menu.py
SOLID Principle — SRP (Single Responsibility Principle):
    โมดูลนี้รับผิดชอบหน้าที่เดียว คือ แสดงหน้า Main Menu ของเกม
    function draw_bg() ดูแลแค่พื้นหลัง, screen_main_menu() ดูแลแค่ UI flow ของ menu

SOLID Principle — DIP (Dependency Inversion Principle):
    ใช้ get_player() จาก data_manager (abstraction) โดยไม่ผูกกับ JSON implementation
    ใช้ Button, draw_text, draw_panel จาก ui_components (abstraction)
"""

import math
import pygame
import os
import random
from core.settings import (
    screen,
    clock,
    DARK,
    GAME_SETTINGS,
    SCREEN_W,
    SCREEN_H,
    FPS,
    LIME,
    ORANGE,
    GREY,
    CYAN,
    RED,
    WHITE,
)
from core.fonts import font_big, font_small, font_tiny
from ui.ui_components import Button, draw_text, draw_panel

from entities.particle import Particle

# DIP: ขึ้นกับ get_player (abstraction) ไม่ผูกกับ JSON implementation
from systems.data_manager import get_player


def draw_bg(tick):
    """SRP: function นี้ทำหน้าที่เดียว คือ วาดพื้นหลังแบบ animated grid"""
    screen.fill(DARK)
    for i in range(0, SCREEN_W, 40):
        for j in range(0, SCREEN_H, 40):
            v = int(20 + 12 * math.sin((i + j + tick * 0.5) * 0.05))
            pygame.draw.rect(screen, (0, v, 0), (i, j, 38, 38), 1)


def screen_main_menu(current_user):
    """
    SRP: function นี้ทำหน้าที่เดียว คือ จัดการ UI flow ของหน้า Main Menu
    DIP: ใช้ Button (abstraction) จัดการปุ่ม, get_player (abstraction) ดึงข้อมูลผู้เล่น
    """
    tick = 0
    particles = []

    # Load Hover Sound
    hover_sfx = None
    base_path = os.path.dirname(os.path.dirname(__file__))

    # โหลดไฟล์ Menu_hover.wav โดยตรง
    s_path = os.path.join(base_path, "assets", "sound", "Menu_hover.wav")
    if os.path.exists(s_path):
        print(f"Loading sound from: {s_path}")
        hover_sfx = pygame.mixer.Sound(s_path)
        hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])

    # Load Click Sound
    click_sfx = None
    c_path = os.path.join(base_path, "assets", "sound", "Menu_click.wav")
    if os.path.exists(c_path):
        click_sfx = pygame.mixer.Sound(c_path)
        click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

    play_btn = Button(SCREEN_W // 2 - 110, 280, 220, 50, "Play Game")
    guest_btn = Button(
        SCREEN_W // 2 - 110, 335, 220, 50, "Practice Mode", (50, 50, 30), ORANGE
    )
    login_btn = Button(
        SCREEN_W // 2 - 110, 390, 220, 50, "Login / Register", (40, 40, 80), CYAN
    )
    howto_btn = Button(
        SCREEN_W // 2 - 110, 445, 220, 50, "How to Play", (20, 60, 60), LIME
    )
    board_btn = Button(SCREEN_W // 2 - 110, 500, 220, 50, "LeaderBoard", GREY)
    settings_btn = Button(
        SCREEN_W // 2 - 110, 555, 220, 50, "Settings", (60, 60, 60), WHITE
    )
    quit_btn = Button(SCREEN_W // 2 - 110, 610, 220, 50, "Quit Game", (60, 10, 10), RED)

    while True:
        tick += 1
        events = pygame.event.get()
        mx, my = pygame.mouse.get_pos()

        for btn in [
            play_btn,
            guest_btn,
            howto_btn,
            board_btn,
            settings_btn,
            login_btn,
            quit_btn,
        ]:

            btn.update(mx, my)

            # Hover Sound Logic
            if btn.rect.collidepoint(mx, my):
                if not getattr(btn, "sound_hovered", False):
                    if GAME_SETTINGS["sfx_volume"] > 0 and hover_sfx:
                        hover_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])
                        hover_sfx.play()
                    btn.sound_hovered = True
            else:
                btn.sound_hovered = False

        for event in events:
            if event.type == pygame.QUIT:
                return "quit", current_user

            if play_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                if not current_user:
                    return "login", current_user
                return "play", current_user

            if board_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "leaderboard", current_user

            if login_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "login", current_user

            if guest_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "play_guest", current_user

            if howto_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "how_to_play", current_user

            if settings_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "settings", current_user

            if quit_btn.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "quit", current_user

        draw_bg(tick)

        # เพิ่ม Effect ละอองบรรยากาศ (Particles) เพื่อความสวยงาม
        if random.random() < 0.3:  # โอกาสเกิด 30% ต่อเฟรม
            px = random.randint(0, SCREEN_W)
            py = random.randint(0, SCREEN_H)

            # สุ่มสี: เขียวพิษ, แดงเลือด, หรือเทาเขม่า
            p_color = random.choice([LIME, RED, (60, 60, 60)])
            particles.append(Particle(px, py, p_color))

        for p in particles:
            p.update()
        particles = [p for p in particles if p.life > 0]

        for p in particles:
            p.draw(screen)

        glow = int(180 + 60 * math.sin(tick * 0.05))
        draw_text(
            screen,
            "ZOMBIE SURVIVAL DEAD ZONE",
            font_big,
            (0, glow, 0),
            SCREEN_W // 2,
            110,
        )
        draw_text(screen, "ฝ่าวิกฤตซอมบี้ให้รอด!", font_small, LIME, SCREEN_W // 2, 160)

        draw_panel(screen, (SCREEN_W // 2 - 190, 195, 380, 65), color=(0, 25, 5))
        if current_user:

            # DIP: เรียก get_player ผ่าน abstraction function
            p = get_player(current_user)
            bs = p["best_score"] if p else 0
            draw_text(
                screen,
                f"ผู้เล่น: {current_user}   คะแนนสูงสุด: {bs}",
                font_small,
                CYAN,
                SCREEN_W // 2,
                227,
            )
        else:
            draw_text(
                screen,
                "กรุณาเข้าสู่ระบบก่อนเล่น หรือ กดผู้เล่นทั่วไป",
                font_small,
                ORANGE,
                SCREEN_W // 2,
                227,
            )

        for btn in [
            play_btn,
            guest_btn,
            howto_btn,
            board_btn,
            settings_btn,
            login_btn,
            quit_btn,
        ]:
            btn.draw(screen)
        draw_text(
            screen,
            "WASD = เดิน Click = ยิงปืน  ESC=หยุด",
            font_tiny,
            GREY,
            SCREEN_W // 2,
            SCREEN_H - 18,
            False,
        )
        draw_text(
            screen, "v1.0 Beta", font_tiny, (80, 80, 80), SCREEN_W - 40, SCREEN_H - 10
        )

        pygame.display.flip()
        clock.tick(FPS)
