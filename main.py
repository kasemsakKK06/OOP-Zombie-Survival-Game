"""
Module: main.py
SOLID Principle — SRP (Single Responsibility Principle):
    โมดูลนี้รับผิดชอบหน้าที่เดียว คือ เป็นจุดเริ่มต้น (entry point) ของโปรแกรม
    และจัดการ state routing ระหว่างหน้าจอต่างๆ (menu, login, play, leaderboard)

SOLID Principle — DIP (Dependency Inversion Principle):
    ใช้ screen functions (screen_main_menu, screen_login, screen_leaderboard)
    และ Game class ผ่าน abstraction — ไม่ผูกกับ implementation ภายในโดยตรง

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเพิ่ม state ใหม่ (เช่น "settings", "credits") ได้
    โดยเพิ่ม elif block ใหม่โดยไม่แก้ไข logic ของ state เดิม
"""

import pygame
import os

pygame.init()

import sys
from core.settings import SCREEN_H, SCREEN_W, FPS, GAME_SETTINGS

# DIP: ขึ้นกับ screen functions (abstractions) ไม่ผูกกับ implementation ภายใน
from screens.main_menu import screen_main_menu
from screens.login_screen import screen_login
from screens.leaderboard_screen import screen_leaderboard
from screens.how_to_play import screen_how_to_play
from screens.settings_screen import screen_settings

# DIP: ขึ้นกับ Game class (abstraction) ไม่ผูกกับ subsystems ภายใน
from game.game import Game
from core.settings import clock


def find_music_path(base_name):
    """Helper to find music file with any supported extension."""
    base_path = os.path.dirname(__file__)
    for ext in [".mp3", ".ogg", ".wav"]:
        path = os.path.join(base_path, "assets", "sound", base_name + ext)
        if os.path.exists(path):
            return path
    return None


def main():
    """
    SRP: function นี้ทำหน้าที่เดียว คือ จัดการ state machine ของเกม
    DIP: delegate งานให้ screen functions และ Game class ผ่าน abstractions
    OCP: เพิ่ม state ใหม่ได้โดยเพิ่ม elif block โดยไม่แก้ state เดิม
    """

    # Game State Machine
    # state ใช้ควบคุม flow ของหน้าจอทั้งหมดในเกม
    # แต่ละ state จะ delegate ไปยัง screen module ที่เกี่ยวข้อง
    current_user = None
    state = "menu"

    # --- Music Management ---
    # โหลด path ของเพลงสำหรับแต่ละ state
    # แยก menu music และ gameplay music
    # current_playing_path ใช้ตรวจว่าเพลงปัจจุบันตรงกับ state หรือไม่
    menu_music_path = find_music_path("main_soundtrack")  # Soundtrack ตอนเปิดเกม
    game_music_path = find_music_path("Dirty_soundtrack")  # Soundtrack ตอนเล่นเกม
    current_playing_path = None

    # Main Game Loop
    # ลูปหลักของโปรแกรม ทำหน้าที่:
    # 1. จัดการ background music ตาม state
    # 2. เรียก screen หรือ game logic ตาม state ปัจจุบัน
    while True:
        # --- Music State Machine ---
        # 1. Determine which music should be playing based on game state

        # กำหนดว่า state ปัจจุบันควรเล่นเพลงอะไร
        # menu states -> menu music
        # gameplay -> game music
        target_path = None
        if state in ("menu", "login", "leaderboard", "how_to_play", "settings"):
            target_path = menu_music_path
        elif state in ("play", "play_guest"):
            target_path = game_music_path

        # 2. Manage music playback based on target and volume
        if GAME_SETTINGS["music_volume"] == 0:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        else:
            # If the wrong song is playing (or no song), switch to the target song.
            if target_path != current_playing_path:
                if target_path:
                    try:
                        pygame.mixer.music.load(target_path)
                        pygame.mixer.music.play(-1, fade_ms=500)
                        current_playing_path = target_path
                    except pygame.error as e:
                        print(f"Error loading music {target_path}: {e}")
                        current_playing_path = None  # Failed
                else:  # No target song for this state
                    pygame.mixer.music.stop()
                    current_playing_path = None
            # If the right song is loaded but was stopped (e.g. volume was 0), restart it.
            elif target_path and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1, fade_ms=500)

        # 3. Always apply the current volume setting
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(GAME_SETTINGS["music_volume"])

        # OCP: แต่ละ state เป็นอิสระ — เพิ่ม state ใหม่ได้โดยไม่กระทบ state เดิม
        if state == "menu":
            # DIP: delegate ไปยัง screen_main_menu (abstraction)
            action, current_user = screen_main_menu(current_user)
            state = action

        elif state == "login":
            # DIP: delegate ไปยัง screen_login (abstraction)
            action, user = screen_login()
            if user:
                current_user = user
            state = action

        elif state == "leaderboard":
            # DIP: delegate ไปยัง screen_leaderboard (abstraction)
            state = screen_leaderboard()

        elif state == "how_to_play":
            # DIP: delegate ไปยัง screen_how_to_play (abstraction)
            state = screen_how_to_play()

        elif state == "settings":
            # DIP: delegate ไปยัง screen_settings (abstraction)
            state = screen_settings()

        elif state in ("play", "play_guest"):
            if state == "play" and not current_user:
                state = "login"
                continue

            # จำ play mode ไว้
            # เพื่อให้ restart กลับมาเริ่มเกมใหม่ใน mode เดิม
            play_state = state

            if play_state == "play_guest":
                game = Game("โหมดฝึกซ้อม", is_guest=True)
            else:
                game = Game(current_user)

            # Game Loop
            # ลูปหลักของเกม ทำหน้าที่:
            # 1. จัดการ background music ตาม state
            # 2. เรียก screen หรือ game logic ตาม state ปัจจุบัน
            while True:
                events = pygame.event.get()
                action = game.handle_input(events)

                if action in ("quit", "menu", "restart"):
                    if action == "restart":
                        state = play_state  # กลับไปสร้าง Game ใหม่ (Wave 1)
                    else:
                        state = action
                    break

                game.update()
                game.draw()
                clock.tick(FPS)

        elif state == "quit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
