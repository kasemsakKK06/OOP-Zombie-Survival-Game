"""
Module: login_screen.py
SOLID Principle — SRP (Single Responsibility Principle):
    โมดูลนี้รับผิดชอบหน้าที่เดียว คือ จัดการหน้า Login/Register ของเกม
    ไม่ยุ่งกับ logic อื่น เช่น game logic หรือ data storage

SOLID Principle — DIP (Dependency Inversion Principle):
    ใช้ get_player, register_player จาก data_manager (abstraction)
    ใช้ Button, InputBox, draw_text จาก ui_components (abstraction)
    ไม่ผูกติดกับ implementation ของ JSON storage โดยตรง

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเปลี่ยน backend (data_manager) หรือ UI components ได้
    โดยไม่ต้องแก้ไข logic ในโมดูลนี้
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
    DARK_GREEN,
    ORANGE,
    GREY,
    PURPLE,
    LIME,
    CYAN,
    GAME_SETTINGS,
)
from core.fonts import font_med, font_small, font_tiny

# DIP: ขึ้นกับ UI components (abstraction) ไม่ผูกติดกับ implementation
from ui.ui_components import Button, InputBox, draw_text, draw_text_left, draw_panel

# DIP: ขึ้นกับ data_manager functions (abstraction) ไม่ผูกติดกับ JSON format
from systems.data_manager import get_player, register_player
from screens.main_menu import draw_bg


def screen_login():
    """
    SRP: function นี้ทำหน้าที่เดียว คือ จัดการ UI flow ของหน้า Login/Register
    DIP: ใช้ get_player, register_player ผ่าน abstraction
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

    mode = "login"
    msg, msg_color, msg_timer = "", WHITE, 0
    # DIP: ใช้ InputBox, Button (abstractions) จัดการ UI
    user_box = InputBox(SCREEN_W // 2 - 145, 285, 290, 42, "ชื่อผู้ใช้")
    pass_box = InputBox(SCREEN_W // 2 - 145, 352, 290, 42, "รหัสผ่าน", password=True)
    tab_l = Button(SCREEN_W // 2 - 145, 215, 140, 38, "เข้าสู่ระบบ", DARK_GREEN)
    tab_r = Button(SCREEN_W // 2 + 5, 215, 140, 38, "สมัครสมาชิก", GREY, PURPLE)
    ok_btn = Button(SCREEN_W // 2 - 145, 410, 290, 44, "ยืนยัน")
    back = Button(20, 20, 80, 36, "กลับ", GREY)

    while True:
        tick += 1
        events = pygame.event.get()
        mx, my = pygame.mouse.get_pos()
        if msg_timer > 0:
            msg_timer -= 1
        for btn in [tab_l, tab_r, ok_btn, back]:
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

        for box in [user_box, pass_box]:
            for e in events:
                box.handle(e)

        for event in events:
            if event.type == pygame.QUIT:
                return "quit", None
            if back.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                return "menu", None
            if tab_l.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                mode = "login"
            if tab_r.clicked(event):
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.play()
                mode = "register"

            submit = ok_btn.clicked(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
            )
            if submit:
                if GAME_SETTINGS["sfx_volume"] > 0 and click_sfx:
                    click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])
                    click_sfx.play()
                u = user_box.text.strip()
                p = pass_box.text.strip()
                if not u or not p:
                    msg, msg_color, msg_timer = "กรุณากรอกให้ครบทุกช่อง!", ORANGE, 150
                elif mode == "login":
                    # DIP: เรียก get_player ผ่าน abstraction function
                    pl = get_player(u)
                    if pl and pl["password"] == p:
                        msg, msg_color, msg_timer = f"ยินดีต้อนรับ {u}!", GREEN, 120
                        pygame.display.flip()
                        pygame.time.wait(700)
                        return "menu", u
                    else:
                        msg, msg_color, msg_timer = "ชื่อหรือรหัสผ่านไม่ถูกต้อง!", RED, 150
                else:
                    # DIP: เรียก register_player ผ่าน abstraction function
                    ok, txt = register_player(u, p)
                    msg, msg_color, msg_timer = txt, GREEN if ok else RED, 150
                    if ok:
                        pygame.display.flip()
                        pygame.time.wait(700)
                        return "menu", u

        draw_bg(tick)
        draw_panel(screen, (SCREEN_W // 2 - 185, 190, 370, 350))
        draw_text(screen, "จัดการบัญชีผู้ใช้", font_med, LIME, SCREEN_W // 2, 155)

        tab_l.color = DARK_GREEN if mode == "login" else GREY
        tab_r.color = (40, 20, 80) if mode == "register" else GREY
        tab_l.draw(screen)
        tab_r.draw(screen)

        draw_text_left(screen, "Username", font_tiny, GREY, SCREEN_W // 2 - 145, 265)
        draw_text_left(screen, "Password", font_tiny, GREY, SCREEN_W // 2 - 145, 333)
        user_box.draw(screen)
        pass_box.draw(screen)

        ok_btn.text = "เข้าสู่ระบบ" if mode == "login" else "สมัครสมาชิก"
        ok_btn.draw(screen)
        back.draw(screen)

        if msg and msg_timer > 0:
            draw_text(screen, msg, font_small, msg_color, SCREEN_W // 2, 475)

        pygame.display.flip()
        clock.tick(FPS)
