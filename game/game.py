"""
Module: game.py
SOLID Principle — SRP (Single Responsibility Principle):
    แยก class Game ออกเป็น subsystems ย่อย:
      - SpawnManager: รับผิดชอบแค่การ spawn ซอมบี้ตาม wave
      - CollisionHandler: รับผิดชอบแค่การตรวจจับ collision
      - HUDRenderer: รับผิดชอบแค่การวาด HUD/overlay/game-over
      - Game: ประสานงาน (orchestrate) subsystems ต่างๆ

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเพิ่ม subsystem ใหม่ได้ (เช่น SoundManager) โดยไม่แก้ subsystem เดิม

SOLID Principle — DIP (Dependency Inversion Principle):
    Game ขึ้นกับ subsystem objects (SpawnManager, CollisionHandler, HUDRenderer)
    ไม่ผูกกับ implementation โดยตรง — สามารถเปลี่ยน implementation ได้
"""

import pygame
import random
import os
from core.settings import (
    screen,
    SCREEN_W,
    SCREEN_H,
    DARK,
    GREEN,
    WHITE,
    RED,
    ORANGE,
    YELLOW,
    LIME,
    CYAN,
    GREY,
    BLOOD,
    BLACK,
    GAME_SETTINGS,
)
from core.fonts import font_big, font_med, font_small, font_tiny
import math
from entities.player import Player
from entities.zombie import Zombie
from entities.bullet import Bullet
from entities.powerup import PowerUp
from entities.particle import Particle, BloodParticle
from entities.weapon import Rifle, Pistol, Shotgun, Knife
from entities.obstacle import Obstacle
from systems.data_manager import update_score
from ui.ui_components import Button, draw_text, draw_text_left, draw_panel
from effects.damage_flash import DamageFlash
from entities.decoration import Grass, Road

# ─── SpawnManager (SRP: รับผิดชอบเฉพาะ spawn ซอมบี้) ────────────────────────


class SpawnManager:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ สร้างซอมบี้ตาม wave
    OCP: สามารถ extend เพื่อเปลี่ยนรูปแบบการ spawn ได้โดย subclass
    """

    def spawn_wave(self, wave, zombies_group):
        """SRP: method นี้ทำหน้าที่เดียว คือ spawn ซอมบี้สำหรับ wave ที่กำหนด"""
        count = 6 + wave * 3
        for _ in range(count):
            x, y = self._get_spawn_position()
            z = Zombie(x, y, wave)
            zombies_group.add(z)

    def _get_spawn_position(self):
        """SRP: method นี้ทำหน้าที่เดียว คือ คำนวณตำแหน่ง spawn แบบสุ่มจากขอบจอ"""
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return random.randint(0, SCREEN_W), 62
        elif side == "bottom":
            return random.randint(0, SCREEN_W), SCREEN_H - 5
        elif side == "left":
            return 2, random.randint(60, SCREEN_H)
        else:
            return SCREEN_W - 2, random.randint(60, SCREEN_H)


# ─── CollisionHandler (SRP: รับผิดชอบเฉพาะ collision detection) ──────────────


class CollisionHandler:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ ตรวจจับและจัดการ collision ทั้งหมด
    OCP: สามารถเพิ่มประเภท collision ใหม่ได้โดยเพิ่ม method ใหม่
    """

    def handle_zombie_player_collision(self, zombies, player, particles, damage_flash):
        """SRP: method นี้ทำหน้าที่เดียว คือ ตรวจสอบและจัดการ zombie ชน player"""
        for z in list(zombies):
            if z.hitbox.colliderect(player.hitbox) and z.attack_cd <= 0:
                z.play_attack_sound()
                player.hp -= z.dmg
                z.attack_cd = 60
                damage_flash.trigger()

                # --- New Player Blood Effect ---
                # Blood spurts away from the zombie
                dx = player.rect.centerx - z.rect.centerx
                dy = player.rect.centery - z.rect.centery
                angle = math.degrees(math.atan2(dy, dx))

                for _ in range(random.randint(12, 20)):  # More particles
                    # Player blood is red
                    color = random.choice([(200, 0, 0), (160, 0, 0), (220, 20, 20)])
                    particles.append(
                        BloodParticle(
                            player.rect.centerx,
                            player.rect.centery,
                            color,
                            angle,
                            speed_mult=1.2,  # Player blood spurts more
                        )
                    )

    def handle_bullet_zombie_collision(
        self, zombies, bullets, particles, powerups, game
    ):
        """SRP: method นี้ทำหน้าที่เดียว คือ ตรวจสอบและจัดการกระสุนชนซอมบี้"""
        hits = pygame.sprite.groupcollide(zombies, bullets, False, True)
        for z, bullet_list in hits.items():
            if GAME_SETTINGS["sfx_volume"] > 0 and game.zombie_hit_sfx:
                game.zombie_hit_sfx.set_volume(0.4 * GAME_SETTINGS["sfx_volume"])
                game.zombie_hit_sfx.play()

            for b in bullet_list:
                z.hp -= b.damage
                # --- New Zombie Blood Effect (from bullet) ---
                angle = math.degrees(math.atan2(b.vy, b.vx))
                for _ in range(random.randint(8, 15)):
                    # Zombie blood is green-ish
                    color = random.choice(
                        [(80, 180, 40), (60, 150, 30), (100, 200, 60)]
                    )
                    particles.append(
                        BloodParticle(
                            z.rect.centerx, z.rect.centery, color, angle, speed_mult=0.8
                        )
                    )

            if z.hp <= 0:
                game.score += z.score_val
                game.kills += 1

                # --- New Zombie Death Explosion ---
                for i in range(45):  # More particles for a bigger explosion
                    angle = random.uniform(0, 360)
                    color = random.choice([(180, 40, 0), (150, 20, 0), (100, 100, 40)])
                    particles.append(
                        BloodParticle(
                            z.rect.centerx, z.rect.centery, color, angle, speed_mult=1.8
                        )
                    )

                if random.random() < 0.15:
                    pu = PowerUp(z.rect.centerx, z.rect.centery)
                    powerups.add(pu)
                z.kill()

    def handle_powerup_collision(self, player, powerups, game):
        """SRP: method นี้ทำหน้าที่เดียว คือ ตรวจสอบและจัดการ player เก็บ power-up"""
        # ใช้ hitbox ของ player ในการเช็คชนเพื่อความแม่นยำ
        for pu in list(powerups):
            if player.hitbox.colliderect(pu.rect):
                if pu.effect == "hp":
                    player.hp = min(100, player.hp + 30)
                elif pu.effect == "speed":
                    game.speed_boost = 300
                elif pu.effect == "rapid":
                    game.rapid_fire = 400
                pu.kill()

    def handle_bullet_obstacle_collision(self, bullets, obstacles):
        """SRP: ตรวจสอบกระสุนชนสิ่งกีดขวาง"""
        pygame.sprite.groupcollide(bullets, obstacles, True, False)


# ─── HUDRenderer (SRP: รับผิดชอบเฉพาะการวาด HUD/overlay) ────────────────────


class HUDRenderer:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ วาด HUD, overlay, และ game-over screen
    OCP: สามารถ extend เพื่อเพิ่มรูปแบบ HUD ใหม่ได้โดย subclass
    """

    def draw_hud(self, surf, game):
        """SRP: method นี้ทำหน้าที่เดียว คือ วาด HUD แถบบน (HP, score, wave, kills)"""
        # HUD top bar
        pygame.draw.rect(surf, (10, 20, 10), (0, 0, SCREEN_W, 90))
        pygame.draw.line(surf, GREEN, (0, 90), (SCREEN_W, 90), 2)

        # HP bar
        pygame.draw.rect(surf, (60, 0, 0), (10, 10, 160, 20), border_radius=4)
        hp_w = int(160 * max(game.player.hp, 0) / 100)
        hp_col = (
            GREEN if game.player.hp > 50 else ORANGE if game.player.hp > 25 else RED
        )
        pygame.draw.rect(surf, hp_col, (10, 10, hp_w, 20), border_radius=4)
        pygame.draw.rect(surf, WHITE, (10, 10, 160, 20), 1, border_radius=4)
        draw_text_left(surf, f"HP: {game.player.hp}", font_tiny, WHITE, 14, 12)

        draw_text(
            surf, f"คะแนน: {int(game.score)}", font_med, YELLOW, SCREEN_W // 2, 40
        )
        draw_text_left(surf, f"Wave {game.wave}", font_small, LIME, SCREEN_W - 230, 11)
        draw_text_left(
            surf, f"ฆ่าไปแล้ว: {game.kills}", font_small, ORANGE, SCREEN_W - 230, 34
        )

        # --- Day/Night Indicator (แสดงสถานะเวลา) ---
        # Smooth text color transition (เปลี่ยนสีตัวหนังสือแบบค่อยเป็นค่อยไป)
        t = game.day_night_factor
        c_night = (150, 150, 255)  # สีม่วงอ่อน (กลางคืน)
        c_day = (255, 220, 0)  # สีเหลือง (กลางวัน)

        r = int(c_night[0] + (c_day[0] - c_night[0]) * t)
        g = int(c_night[1] + (c_day[1] - c_night[1]) * t)
        b = int(c_night[2] + (c_day[2] - c_night[2]) * t)

        time_txt = "Time: Day" if t > 0.5 else "Time: Night"
        draw_text_left(surf, time_txt, font_small, (r, g, b), SCREEN_W - 230, 57)

        draw_text_left(surf, game.username, font_tiny, CYAN, 14, 42)

        # Buff indicators
        bx = 185
        if game.speed_boost > 0:
            draw_text_left(surf, "SPEED+", font_tiny, CYAN, bx, 10)
            bx += 65
        if game.rapid_fire > 0:
            draw_text_left(surf, "RAPID+", font_tiny, YELLOW, bx, 10)

        # OCP: สามารถเพิ่มอาวุธใหม่ได้โดยเพิ่มใน weapon_colors
        # โดยไม่ต้องแก้ logic การวาด HUD
        # Weapon slots HUD — แสดงอาวุธ 3 ช่องบน top bar
        slot_w, slot_h = 70, 22
        slot_y = 65
        slot_start_x = 14
        weapon_colors = {
            "Rifle": LIME,
            "Pistol": CYAN,
            "Shotgun": YELLOW,
            "Knife": ORANGE,
        }

        for i, wp in enumerate(game.weapons):
            sx = slot_start_x + i * (slot_w + 4)
            is_active = i == game.current_weapon_idx
            # พื้นหลังช่อง
            bg_col = (40, 60, 40) if is_active else (20, 30, 20)
            pygame.draw.rect(
                surf, bg_col, (sx, slot_y, slot_w, slot_h), border_radius=4
            )
            # ขอบ highlight
            border_col = weapon_colors.get(wp.name, WHITE) if is_active else GREY
            pygame.draw.rect(
                surf, border_col, (sx, slot_y, slot_w, slot_h), 2, border_radius=4
            )
            # ชื่อและปุ่มลัด
            label = f"{i+1}:{wp.name}"
            txt_col = weapon_colors.get(wp.name, WHITE) if is_active else GREY
            draw_text(
                surf, label, font_tiny, txt_col, sx + slot_w // 2, slot_y + slot_h // 2
            )

        # Pause button — ปุ่มหยุดมุมขวาบน
        game.pause_btn.draw(surf)
        # Draw || icon on pause button
        pb = game.pause_btn.rect
        bx = pb.x + 8
        by = pb.centery - 5
        pygame.draw.rect(surf, WHITE, (bx, by, 3, 10), border_radius=1)
        pygame.draw.rect(surf, WHITE, (bx + 5, by, 3, 10), border_radius=1)

    def draw_between_wave(self, surf, game):
        """SRP: method นี้ทำหน้าที่เดียว คือ วาด overlay ระหว่าง wave"""
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 130))
        surf.blit(ov, (0, 0))

        draw_text(
            surf,
            f"WAVE {game.wave-1} COMPLETED!",
            font_big,
            LIME,
            SCREEN_W // 2,
            SCREEN_H // 2 - 30,
        )
        draw_text(
            surf,
            f"Wave {game.wave} จะเริ่มใน {game.between_timer//60+1} วินาที",
            font_med,
            WHITE,
            SCREEN_W // 2,
            SCREEN_H // 2 + 30,
        )

    def draw_paused(self, surf, game):
        """SRP: method นี้ทำหน้าที่เดียว คือ วาด overlay หน้าจอหยุดชั่วคราว"""
        # Subtle dark overlay — มืดนิดหน่อยให้โฟกัสที่ panel
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 90))
        surf.blit(ov, (0, 0))

        cx = SCREEN_W // 2
        panel_w, panel_h = 360, 370
        panel_x = cx - panel_w // 2
        panel_y = SCREEN_H // 2 - panel_h // 2

        # Outer glow border
        glow = pygame.Surface((panel_w + 12, panel_h + 12), pygame.SRCALPHA)
        glow.fill((50, 200, 50, 30))
        surf.blit(glow, (panel_x - 6, panel_y - 6))

        # Main panel background
        draw_panel(surf, (panel_x, panel_y, panel_w, panel_h), color=(12, 24, 12))

        # Green accent header bar
        header_h = 55
        hdr = pygame.Surface((panel_w - 4, header_h), pygame.SRCALPHA)
        hdr.fill((30, 80, 30, 200))
        surf.blit(hdr, (panel_x + 2, panel_y + 2))

        # Title — draw pause icon (||) + text centered together
        title_text = "GAME PAUSED"
        title_surf = font_med.render(title_text, True, WHITE)
        title_w = title_surf.get_width()
        bar_w, bar_h = 5, 24
        bar_gap = 6
        icon_total_w = bar_w * 2 + bar_gap  # || icon width
        spacing = 12  # gap between icon and text
        total_w = icon_total_w + spacing + title_w
        start_x = cx - total_w // 2
        icon_y = panel_y + 20
        # Draw || bars
        pygame.draw.rect(surf, WHITE, (start_x, icon_y, bar_w, bar_h), border_radius=2)
        pygame.draw.rect(
            surf,
            WHITE,
            (start_x + bar_w + bar_gap, icon_y, bar_w, bar_h),
            border_radius=2,
        )
        # Draw title text (left-aligned after icon)
        text_x = start_x + icon_total_w + spacing
        text_y = panel_y + 30 - title_surf.get_height() // 2
        # Shadow
        shadow = font_med.render(title_text, True, (0, 0, 0))
        surf.blit(shadow, (text_x + 2, text_y + 2))
        surf.blit(title_surf, (text_x, text_y))

        # Divider
        div_y = panel_y + header_h + 8
        pygame.draw.line(
            surf,
            (50, 120, 50),
            (panel_x + 25, div_y),
            (panel_x + panel_w - 25, div_y),
            1,
        )

        # Stats section — แสดงข้อมูลปัจจุบัน
        stats_y = div_y + 14
        stat_labels = [
            (f"Wave: {game.wave}", LIME),
            (f"คะแนน: {int(game.score)}", YELLOW),
            (f"กำจัด: {game.kills} ตัว", ORANGE),
        ]
        stat_spacing = panel_w // 3
        for i, (label, col) in enumerate(stat_labels):
            sx = panel_x + stat_spacing // 2 + i * stat_spacing
            draw_text(surf, label, font_tiny, col, sx, stats_y)

        # Divider 2
        div2_y = stats_y + 22
        pygame.draw.line(
            surf,
            (40, 80, 40),
            (panel_x + 25, div2_y),
            (panel_x + panel_w - 25, div2_y),
            1,
        )

        # Subtitle
        draw_text(surf, "คุณต้องการทำอะไร?", font_small, (120, 160, 120), cx, div2_y + 22)

        # 3 Buttons + icons
        game.resume_btn.draw(surf)
        game.restart_btn.draw(surf)
        game.quit_p_btn.draw(surf)

        # Icon: ▶ triangle on resume button
        rb = game.resume_btn.rect
        tri_x = rb.x + 18
        tri_y = rb.centery
        pygame.draw.polygon(
            surf,
            LIME,
            [
                (tri_x, tri_y - 8),
                (tri_x, tri_y + 8),
                (tri_x + 12, tri_y),
            ],
        )

        # Icon: circular arrow on restart button
        rsb = game.restart_btn.rect
        arc_cx = rsb.x + 22
        arc_cy = rsb.centery
        arc_r = 8
        pygame.draw.arc(
            surf,
            WHITE,
            (arc_cx - arc_r, arc_cy - arc_r, arc_r * 2, arc_r * 2),
            0.5,
            5.5,
            2,
        )
        # arrow tip
        pygame.draw.polygon(
            surf,
            WHITE,
            [
                (arc_cx + arc_r - 1, arc_cy - 4),
                (arc_cx + arc_r + 5, arc_cy - 1),
                (arc_cx + arc_r - 1, arc_cy + 2),
            ],
        )

        # Icon: X on quit button
        qb = game.quit_p_btn.rect
        x_cx = qb.x + 22
        x_cy = qb.centery
        pygame.draw.line(surf, WHITE, (x_cx - 6, x_cy - 6), (x_cx + 6, x_cy + 6), 3)
        pygame.draw.line(surf, WHITE, (x_cx + 6, x_cy - 6), (x_cx - 6, x_cy + 6), 3)

    def draw_game_over(self, surf, game):
        """SRP: method นี้ทำหน้าที่เดียว คือ วาดหน้าจอ game over"""
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        surf.blit(ov, (0, 0))
        draw_panel(
            surf,
            (SCREEN_W // 2 - 210, SCREEN_H // 2 - 140, 420, 290),
            color=(40, 0, 0),
        )
        draw_text(surf, "GAME OVER", font_big, RED, SCREEN_W // 2, SCREEN_H // 2 - 100)
        draw_text(
            surf,
            f"คะแนน: {int(game.score)}",
            font_med,
            YELLOW,
            SCREEN_W // 2,
            SCREEN_H // 2 - 50,
        )
        draw_text(
            surf,
            f"ถึง Wave: {game.wave}   กำจัดซอมบี้: {game.kills} ตัว",
            font_small,
            WHITE,
            SCREEN_W // 2,
            SCREEN_H // 2 - 10,
        )
        game.play_again_btn.draw(surf)
        game.menu_btn.draw(surf)


# ─── Game Class (SRP: ประสานงาน subsystems / DIP: ขึ้นกับ abstractions) ──────


class Game:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ ประสานงาน (orchestrate) subsystems ต่างๆ
         ไม่ทำ logic ย่อยเอง แต่ delegate ไปยัง SpawnManager, CollisionHandler, HUDRenderer
    DIP: ขึ้นกับ subsystem objects (abstraction) ไม่ผูกกับ implementation โดยตรง
    OCP: สามารถเพิ่ม subsystem ใหม่ได้โดยไม่แก้ code เดิม
    """

    def __init__(self, username, is_guest=False):
        """
        SRP: constructor จัดการแค่การสร้างสถานะเกมและ inject subsystems
        DIP: สร้าง subsystems ผ่าน dependency injection pattern
        """
        self.username = username
        self.is_guest = is_guest
        self.score = 0
        self.kills = 0
        self.wave = 1
        self.between_wave = False
        self.between_timer = 180
        self.game_over = False
        self.paused = False
        self.slash_effects = []  # เก็บเอฟเฟกต์ฟันมีด
        self.map_rect = pygame.Rect(0, 92, SCREEN_W, SCREEN_H - 92)
        self.player = Player(SCREEN_W // 2, SCREEN_H // 2)
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.particles = []

        self._build_map()
        self.speed_boost = 0
        self.rapid_fire = 0
        self.hp_regen_timer = 120  # Auto รีเจนเลือดทุก 2 วินาที (120 frames ที่ 60 FPS)
        self.is_attacking = False

        # ระบบอาวุธ: 1=Rifle, 2=Pistol, 3=Shotgun, 4=Knife
        self.weapons = [Rifle(), Pistol(), Shotgun(), Knife()]
        self.current_weapon_idx = 0

        # --- เพิ่ม: โหลด BG กลางวันและกลางคืน ---

        base_path = os.path.dirname(os.path.dirname(__file__))
        self.bg_image_night = None
        self.bg_image_day = None

        # Load Shotgun Sound
        self.shotgun_sfx = None
        shotgun_path = os.path.join(base_path, "assets", "sound", "shotgun.wav")
        if os.path.exists(shotgun_path):
            self.shotgun_sfx = pygame.mixer.Sound(shotgun_path)
            self.shotgun_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])

        # Load Handgun Sound
        self.handgun_sfx = None
        handgun_path = os.path.join(base_path, "assets", "sound", "handgun.wav")
        if os.path.exists(handgun_path):
            self.handgun_sfx = pygame.mixer.Sound(handgun_path)
            self.handgun_sfx.set_volume(0.4 * GAME_SETTINGS["sfx_volume"])

        # Load Rifle Sound
        self.rifle_sfx = None
        rifle_path = os.path.join(base_path, "assets", "sound", "rifle.wav")
        if os.path.exists(rifle_path):
            self.rifle_sfx = pygame.mixer.Sound(rifle_path)
            self.rifle_sfx.set_volume(0.3 * GAME_SETTINGS["sfx_volume"])

        # Load Melee Sound
        self.melee_sfx = None
        melee_path = os.path.join(base_path, "assets", "sound", "melee.wav")
        if os.path.exists(melee_path):
            self.melee_sfx = pygame.mixer.Sound(melee_path)
            self.melee_sfx.set_volume(0.6 * GAME_SETTINGS["sfx_volume"])

        # Load Menu Hover Sound
        self.menu_hover_sfx = None
        hover_path = os.path.join(base_path, "assets", "sound", "Menu_hover.wav")
        if os.path.exists(hover_path):
            self.menu_hover_sfx = pygame.mixer.Sound(hover_path)
            self.menu_hover_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

        # Load Menu Click Sound
        self.menu_click_sfx = None
        click_path = os.path.join(base_path, "assets", "sound", "Menu_click.wav")
        if os.path.exists(click_path):
            self.menu_click_sfx = pygame.mixer.Sound(click_path)
            self.menu_click_sfx.set_volume(1.0 * GAME_SETTINGS["sfx_volume"])

        # Load Zombie Hit Sound
        self.zombie_hit_sfx = None
        zombie_hit_path = os.path.join(base_path, "assets", "sound", "shot_zombie.wav")
        if os.path.exists(zombie_hit_path):
            self.zombie_hit_sfx = pygame.mixer.Sound(zombie_hit_path)
            self.zombie_hit_sfx.set_volume(0.4 * GAME_SETTINGS["sfx_volume"])

        # Load Muzzle Flash Images
        self.muzzle_flash_imgs = []
        self.muzzle_flashes = []  # เก็บรายการ flash ที่กำลังแสดง {img, rect, timer}
        mf_path = os.path.join(base_path, "assets", "images", "muzzle_flashs")
        if os.path.exists(mf_path):
            for f in os.listdir(mf_path):
                if f.lower().endswith(".png"):
                    img = pygame.image.load(os.path.join(mf_path, f)).convert_alpha()
                    # --- ปรับขนาดไฟตรงนี้ (Scale) ---
                    # 0.3 หมายถึงย่อเหลือ 30% ของขนาดเดิม (ถ้ายังใหญ่ไปให้ลดเลขลง เช่น 0.2)
                    scale_val = 0.15
                    img = pygame.transform.scale(
                        img,
                        (
                            int(img.get_width() * scale_val),
                            int(img.get_height() * scale_val),
                        ),
                    )
                    self.muzzle_flash_imgs.append(img)

        # --- Load Knife Effect Images (New) ---
        self.knife_effect_imgs = []
        ke_path = os.path.join(base_path, "assets", "images", "knife_effect")
        if os.path.exists(ke_path):
            # พยายามเรียงไฟล์ตามตัวเลข (เช่น slash_0, slash_1)
            try:
                files = sorted(
                    os.listdir(ke_path),
                    key=lambda x: (
                        int("".join(filter(str.isdigit, x)))
                        if any(c.isdigit() for c in x)
                        else x
                    ),
                )
            except:
                files = sorted(os.listdir(ke_path))
            for f in files:
                if f.lower().endswith(".png"):
                    img = pygame.image.load(os.path.join(ke_path, f)).convert_alpha()
                    # ปรับขนาดให้พอดีกับระยะฟัน (ปรับเล็กลงจาก 190 เป็น 150)
                    img = pygame.transform.scale(img, (100, 100))
                    self.knife_effect_imgs.append(img)

        bg_path_night = os.path.join(
            base_path, "assets", "images", "bg_map", "terrain-map-v7.png"
        )
        if os.path.exists(bg_path_night):
            self.bg_image_night = pygame.image.load(bg_path_night).convert()
            self.bg_image_night = pygame.transform.scale(
                self.bg_image_night, (SCREEN_W, SCREEN_H)
            )

        # ผมจะสมมติว่าไฟล์กลางวันชื่อ 'terrain-map-v7-day.png' นะครับ
        # ถ้าไม่มีไฟล์นี้ ผมจะสร้างเวอร์ชั่นสว่างขึ้นมาให้แทน
        bg_path_day = os.path.join(
            base_path, "assets", "images", "bg_map", "terrain-map-v7-day.png"
        )
        if os.path.exists(bg_path_day):
            self.bg_image_day = pygame.image.load(bg_path_day).convert()
            self.bg_image_day = pygame.transform.scale(
                self.bg_image_day, (SCREEN_W, SCREEN_H)
            )
        elif self.bg_image_night:
            # Fallback: สร้าง BG กลางวันที่สว่างกว่าจาก BG กลางคืน
            self.bg_image_day = self.bg_image_night.copy()
            # เพิ่มความสว่างให้มากขึ้น จะได้ดูเป็นกลางวันชัดเจน
            self.bg_image_day.fill((90, 90, 70), special_flags=pygame.BLEND_RGB_ADD)

        self.day_night_factor = 0.0  # 0.0 = Night, 1.0 = Day
        self.target_day_night_factor = 0.0
        self._update_background()
        self.day_night_factor = self.target_day_night_factor  # เริ่มต้นให้ตรงกับสภาพจริงทันที

        self.bg_dots = [
            (
                random.randint(0, SCREEN_W),
                random.randint(60, SCREEN_H),
                random.randint(3, 8),
                random.choice([(20, 40, 20), (30, 50, 20), (15, 35, 15)]),
            )
            for _ in range(50)
        ]

        # UI Buttons (SRP: ปุ่มแต่ละตัวจัดการตัวเอง)
        # Pause menu buttons — 3 ปุ่ม: ดำเนินต่อ / เริ่มใหม่ / ออกเกม
        self.resume_btn = Button(
            SCREEN_W // 2 - 110, SCREEN_H // 2 - 20, 220, 46, "   ดำเนินการต่อ"
        )
        self.restart_btn = Button(
            SCREEN_W // 2 - 110,
            SCREEN_H // 2 + 36,
            220,
            46,
            "   เริ่มเกมใหม่",
            ORANGE,
            YELLOW,
        )
        self.quit_p_btn = Button(
            SCREEN_W // 2 - 110,
            SCREEN_H // 2 + 92,
            220,
            46,
            "   ออกจากเกม",
            BLOOD,
            RED,
        )
        # Game over buttons
        self.play_again_btn = Button(
            SCREEN_W // 2 - 100, SCREEN_H // 2 + 30, 200, 44, "เล่นใหม่"
        )
        self.menu_btn = Button(
            SCREEN_W // 2 - 100, SCREEN_H // 2 + 85, 200, 44, "หน้าหลัก", GREY
        )
        # Pause button on HUD — ปุ่มหยุดบนแถบ HUD
        self.pause_btn = Button(
            SCREEN_W - 110, 15, 100, 29, "  Pause", (30, 50, 30), (60, 100, 60)
        )

        # DIP: inject subsystems — สามารถเปลี่ยน implementation ได้
        self._spawn_manager = SpawnManager()
        self._collision_handler = CollisionHandler()
        self._hud_renderer = HUDRenderer()

        # Spawn wave แรก
        self._spawn_manager.spawn_wave(self.wave, self.zombies)
        self.damage_flash = DamageFlash((SCREEN_W, SCREEN_H))
        self._update_background()  # เรียกครั้งแรกเพื่อตั้งค่า BG สำหรับ wave 1
        self.wave = 1

    def _build_map(self):
        """SRP: สร้างสิ่งกีดขวางในฉากให้ดูเป็นแผนที่ที่มีมิติ"""

        # สร้างหญ้ากระจัดกระจาย (Decoration)
        for _ in range(8):
            gx = random.randint(0, SCREEN_W - 100)
            gy = random.randint(100, SCREEN_H - 100)
            self.decorations.add(
                Grass(gx, gy, random.randint(80, 200), random.randint(80, 200))
            )

        # สร้างทางเดิน (ถนนคาดกลาง) (Decoration)
        self.decorations.add(Road(150, 350, SCREEN_W - 300, 60))
        self.decorations.add(Road(SCREEN_W // 2 - 30, 150, 60, SCREEN_H - 300))

        # สร้างสิ่งกีดขวางกล่อง/หิน (สุ่มวางแบบมีช่องว่างวิ่งผ่านได้)
        placed_rects = []
        for _ in range(random.randint(4, 9)):
            for attempt in range(10):  # ลองสุ่ม 10 ครั้งต่อชิ้น หาจุดที่ไม่ทับกัน
                ow = random.randint(40, 90)
                oh = random.randint(30, 70)
                ox = random.randint(100, SCREEN_W - 100 - ow)
                oy = random.randint(100, SCREEN_H - 100 - oh)

                new_rect = pygame.Rect(
                    ox - 60, oy - 60, ow + 120, oh + 120
                )  # เผื่อช่องว่างรอบตัวอย่างน้อย 60px

                # ตรวจสอบว่าทับกับชิ้นอื่นที่มีอยู่แล้วไหม
                overlap = any(new_rect.colliderect(r) for r in placed_rects)

                # อย่าให้บังตรงกลางแมพมากเกินไปตรงจุดเกิด Player
                center_rect = pygame.Rect(
                    SCREEN_W // 2 - 100, SCREEN_H // 2 - 100, 200, 200
                )
                if not overlap and not new_rect.colliderect(center_rect):
                    actual_rect = pygame.Rect(ox, oy, ow, oh)
                    placed_rects.append(actual_rect)
                    color = random.choice([(60, 60, 60), (80, 50, 30), (50, 70, 50)])
                    self.obstacles.add(Obstacle(ox, oy, ow, oh, color))
                    break

    def _update_background(self):
        """SRP: อัปเดตภาพพื้นหลังตาม wave (กลางวัน/กลางคืน)"""
        is_day = ((self.wave - 1) // 3) % 2 == 1
        self.target_day_night_factor = 1.0 if is_day else 0.0

    @property
    def current_weapon(self):
        return self.weapons[self.current_weapon_idx]

    def _shoot(self, mx, my):
        weapon = self.current_weapon
        if self.player.shoot_cd > 0:
            return

        # --- คำนวณตำแหน่งจุดกำเนิดกระสุน (Spawn Point) ---
        angle = self.player.angle
        rad = math.radians(angle)
        cx, cy = self.player.hitbox.centerx, self.player.hitbox.centery

        # 1. ระยะยื่นไปข้างหน้า (Forward Offset) - ปรับตามความยาวปืน
        forward_offset = 40
        if weapon.name == "Pistol":
            forward_offset = 36
        elif weapon.name in ("Rifle", "Shotgun"):
            forward_offset = 34

        # 2. ระยะห่างด้านข้าง (Side Offset)
        # ถ้ากระสุนอยู่ "ล่าง" ไป (ต่ำกว่าปืน) ให้ ลดค่านี้ลง (เช่น 15 -> 5 หรือ -5)
        # ถ้ากระสุนอยู่ "บน" ไป (สูงกว่าปืน) ให้ เพิ่มค่านี้
        side_offset = 12

        # สูตรคำนวณพิกัด (Vector Rotation)
        spawn_x = cx + (forward_offset * math.cos(rad)) + (side_offset * math.sin(rad))
        spawn_y = cy - (forward_offset * math.sin(rad)) + (side_offset * math.cos(rad))

        if weapon.name == "Shotgun":
            if GAME_SETTINGS["sfx_volume"] > 0 and self.shotgun_sfx:
                self.shotgun_sfx.set_volume(0.5 * GAME_SETTINGS["sfx_volume"])
                self.shotgun_sfx.play()
            for _ in range(5):
                b = Bullet(
                    spawn_x,
                    spawn_y,
                    mx + random.randint(-40, 40),
                    my + random.randint(-40, 40),
                    damage=weapon.damage,
                )
                self.bullets.add(b)
        else:
            if (
                GAME_SETTINGS["sfx_volume"] > 0
                and weapon.name == "Pistol"
                and self.handgun_sfx
            ):
                self.handgun_sfx.set_volume(0.4 * GAME_SETTINGS["sfx_volume"])
                self.handgun_sfx.play()
            elif (
                GAME_SETTINGS["sfx_volume"] > 0
                and weapon.name == "Rifle"
                and self.rifle_sfx
            ):
                self.rifle_sfx.set_volume(0.3 * GAME_SETTINGS["sfx_volume"])
                self.rifle_sfx.play()

            b = Bullet(
                spawn_x,
                spawn_y,
                mx,
                my,
                damage=weapon.damage,
            )
            self.bullets.add(b)

        # --- Muzzle Flash Effect ---
        if self.muzzle_flash_imgs:
            # ใช้ตำแหน่งเดียวกับกระสุนเลย ไฟจะได้ออกตรงรู
            tip_x = spawn_x
            tip_y = spawn_y

            # สุ่มภาพและหมุนตามทิศทาง
            mf_img = random.choice(self.muzzle_flash_imgs)
            rot_mf = pygame.transform.rotate(mf_img, angle)
            mf_rect = rot_mf.get_rect(center=(tip_x, tip_y))
            self.muzzle_flashes.append({"img": rot_mf, "rect": mf_rect, "timer": 3})

        cd = weapon.shoot_cd
        if self.rapid_fire > 0:
            cd = max(4, cd // 2)
        self.player.shoot_cd = cd

    def _melee_attack(self, weapon):
        """SRP: method ฟัน zombie ที่อยู่ในรัศมีมีด"""
        if GAME_SETTINGS["sfx_volume"] > 0 and self.melee_sfx:
            self.melee_sfx.set_volume(0.6 * GAME_SETTINGS["sfx_volume"])
            self.melee_sfx.play()
        px, py = self.player.hitbox.centerx, self.player.hitbox.centery
        mx, my = pygame.mouse.get_pos()
        # คำนวณมุมจาก player ไปยัง mouse เพื่อทำ slash arc
        angle = math.atan2(my - py, mx - px)

        if self.knife_effect_imgs:
            # --- Use Sprite Effect (New) ---
            # คำนวณตำแหน่งเริ่มต้นให้ตรงกับ Logic ใน Update (จะได้ไม่กระตุกเฟรมแรก)
            forward_offset = 60
            side_offset = 50

            self.slash_effects.append(
                {
                    "type": "sprite",
                    "x": px
                    + (math.cos(angle) * forward_offset)
                    + (math.sin(angle) * side_offset),
                    "y": py
                    + (math.sin(angle) * forward_offset)
                    - (math.cos(angle) * side_offset),
                    "angle": angle,
                    "frame": 0,
                    "speed": 0.75,  # เร่งความเร็วให้ฉับไวขึ้น (เดิม 0.5)
                }
            )
        else:
            # Use Procedural Effect (Fallback) - กรณีไม่มีไฟล์ภาพ
            self.slash_effects.append(
                {
                    "type": "procedural",
                    "x": px,
                    "y": py,
                    "angle": angle,
                    "radius": weapon.MELEE_RANGE,
                    "timer": 12,
                    "max_timer": 12,
                }
            )
        for z in list(self.zombies):
            dist = math.hypot(z.rect.centerx - px, z.rect.centery - py)
            if dist <= weapon.MELEE_RANGE:
                z.play_hit_sound()
                z.hp -= weapon.damage

                # --- New Zombie Blood Effect (from melee) ---
                dx = z.rect.centerx - px
                dy = z.rect.centery - py
                angle = math.degrees(math.atan2(dy, dx))
                for _ in range(random.randint(15, 25)):
                    color = random.choice(
                        [(80, 180, 40), (60, 150, 30), (100, 200, 60)]
                    )
                    self.particles.append(
                        BloodParticle(
                            z.rect.centerx, z.rect.centery, color, angle, speed_mult=2.0
                        )
                    )

                if z.hp <= 0:
                    self.score += z.score_val
                    self.kills += 1
                    # --- New Zombie Death Explosion (from melee) ---
                    for i in range(45):
                        angle = random.uniform(0, 360)
                        self.particles.append(
                            BloodParticle(
                                z.rect.centerx,
                                z.rect.centery,
                                color,
                                angle,
                                speed_mult=1.8,
                            )
                        )
                    if random.random() < 0.15:
                        pu = PowerUp(z.rect.centerx, z.rect.centery)
                        self.powerups.add(pu)
                    z.kill()

    def handle_input(self, events):
        """SRP: method นี้ทำหน้าที่เดียว คือ จัดการ input ของผู้เล่น"""
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    self.paused = not self.paused

            # สลับอาวุธด้วยปุ่ม 1, 2, 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_weapon_idx = 0
                    self.player.switch_weapon("Rifle")

                elif event.key == pygame.K_2:
                    self.current_weapon_idx = 1
                    self.player.switch_weapon("Pistol")

                elif event.key == pygame.K_3:
                    self.current_weapon_idx = 2
                    self.player.switch_weapon("Shotgun")

                elif event.key == pygame.K_4:
                    self.current_weapon_idx = 3
                    self.player.switch_weapon("Knife")

            if not self.paused and not self.game_over:  # self.between_wave
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_weapon.is_melee:
                        self.player.is_attacking = True
                        self.player.frame_index = 0
                        self._melee_attack(self.current_weapon)
                    elif not self.current_weapon.auto_fire:
                        self._shoot(mx, my)

            if self.paused:
                self.resume_btn.update(mx, my)
                self.restart_btn.update(mx, my)
                self.quit_p_btn.update(mx, my)

                # Hover Sound for Pause Menu
                for btn in [self.resume_btn, self.restart_btn, self.quit_p_btn]:
                    if btn.rect.collidepoint(mx, my):
                        if not getattr(btn, "sound_hovered", False):
                            if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_hover_sfx:
                                self.menu_hover_sfx.set_volume(
                                    1.0 * GAME_SETTINGS["sfx_volume"]
                                )
                                self.menu_hover_sfx.play()
                            btn.sound_hovered = True
                    else:
                        btn.sound_hovered = False

                if self.resume_btn.clicked(event):
                    if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_click_sfx:
                        self.menu_click_sfx.set_volume(
                            1.0 * GAME_SETTINGS["sfx_volume"]
                        )
                        self.menu_click_sfx.play()
                    self.paused = False

                if self.restart_btn.clicked(event):
                    if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_click_sfx:
                        self.menu_click_sfx.set_volume(
                            1.0 * GAME_SETTINGS["sfx_volume"]
                        )
                        self.menu_click_sfx.play()
                    return "restart"

                if self.quit_p_btn.clicked(event):
                    if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_click_sfx:
                        self.menu_click_sfx.set_volume(
                            1.0 * GAME_SETTINGS["sfx_volume"]
                        )
                        self.menu_click_sfx.play()
                    return "menu"

            if self.game_over:
                self.play_again_btn.update(mx, my)
                self.menu_btn.update(mx, my)

                # Hover Sound for Game Over Menu
                for btn in [self.play_again_btn, self.menu_btn]:
                    if btn.rect.collidepoint(mx, my):
                        if not getattr(btn, "sound_hovered", False):
                            if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_hover_sfx:
                                self.menu_hover_sfx.set_volume(
                                    1.0 * GAME_SETTINGS["sfx_volume"]
                                )
                                self.menu_hover_sfx.play()
                            btn.sound_hovered = True
                    else:
                        btn.sound_hovered = False

                if self.play_again_btn.clicked(event):
                    if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_click_sfx:
                        self.menu_click_sfx.set_volume(
                            1.0 * GAME_SETTINGS["sfx_volume"]
                        )
                        self.menu_click_sfx.play()
                    return "restart"

                if self.menu_btn.clicked(event):
                    if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_click_sfx:
                        self.menu_click_sfx.set_volume(
                            1.0 * GAME_SETTINGS["sfx_volume"]
                        )
                        self.menu_click_sfx.play()
                    return "menu"

            if not self.paused and not self.game_over:
                # Pause button on HUD — คลิกปุ่มหยุดบนหน้าจอ
                self.pause_btn.update(mx, my)

                # Hover Sound for HUD Pause Button
                if self.pause_btn.rect.collidepoint(mx, my):
                    if not getattr(self.pause_btn, "sound_hovered", False):
                        if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_hover_sfx:
                            self.menu_hover_sfx.set_volume(
                                1.0 * GAME_SETTINGS["sfx_volume"]
                            )
                            self.menu_hover_sfx.play()
                        self.pause_btn.sound_hovered = True
                else:
                    self.pause_btn.sound_hovered = False

                if self.pause_btn.clicked(event):
                    if GAME_SETTINGS["sfx_volume"] > 0 and self.menu_click_sfx:
                        self.menu_click_sfx.set_volume(
                            1.0 * GAME_SETTINGS["sfx_volume"]
                        )
                        self.menu_click_sfx.play()
                    self.paused = True

        # Rifle auto-fire: กดค้างยิงรัว
        if not self.paused and not self.game_over:  # self.between_wave เพื่อไม่ให้ยิงได้
            if self.current_weapon.auto_fire:
                if pygame.mouse.get_pressed()[0]:
                    self._shoot(mx, my)

        return None

    def update(self):
        """
        SRP: method นี้ทำหน้าที่เดียว คือ อัปเดตสถานะเกม โดย delegate ไปยัง subsystems
        DIP: เรียกใช้ subsystems ผ่าน abstraction (self._collision_handler, etc.)
        """

        if self.paused or self.game_over:
            return

        if self.paused or self.game_over:
            return

        # --- Smooth Day/Night Transition Logic ---
        # ค่อยๆ ปรับค่า day_night_factor เข้าหา target ทีละนิด
        if self.day_night_factor < self.target_day_night_factor:
            self.day_night_factor += 0.005  # ความเร็วในการเปลี่ยน (ยิ่งน้อยยิ่งสมูท)

            if self.day_night_factor > self.target_day_night_factor:
                self.day_night_factor = self.target_day_night_factor

        elif self.day_night_factor > self.target_day_night_factor:
            self.day_night_factor -= 0.005

            if self.day_night_factor < self.target_day_night_factor:
                self.day_night_factor = self.target_day_night_factor

        keys = pygame.key.get_pressed()

        # ให้ผู้เล่นเดินได้ตลอด
        self.player.update(keys, self.map_rect, self.obstacles)

        if self.between_wave:
            self.between_timer -= 1
            if self.between_timer <= 0:
                self.between_wave = False
                self.between_timer = 180
                # DIP: delegate spawn ให้ SpawnManager
                self._spawn_manager.spawn_wave(self.wave, self.zombies)

        # ปรับความเร็วการเดินของคน
        # ความเร็วตอนได้บัพรองเท้าวิ่งเร็ว (ค่าเดิม 5.5 ปรับเป็น 3.5)
        # ความเร็วปกติ (ค่าเดิม 3.5 ปรับเป็น 2.0)
        self.player.speed = 6.5 if self.speed_boost > 0 else 4.0
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.rapid_fire > 0:
            self.rapid_fire -= 1

        for b in list(self.bullets):
            b.update(self.map_rect)
        for z in list(self.zombies):
            z.update(self.player, self.obstacles, self.map_rect)

        # DIP: delegate collision handling ให้ CollisionHandler
        self._collision_handler.handle_zombie_player_collision(
            self.zombies, self.player, self.particles, self.damage_flash
        )
        self._collision_handler.handle_bullet_zombie_collision(
            self.zombies, self.bullets, self.particles, self.powerups, self
        )
        self._collision_handler.handle_bullet_obstacle_collision(
            self.bullets, self.obstacles
        )
        self._collision_handler.handle_powerup_collision(
            self.player, self.powerups, self
        )

        for pu in list(self.powerups):
            pu.update()

        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()
        self.score += 0.01

        # Auto HP regen: ทุก 2 วินาที เพิ่มเลือดสุ่ม 1-10 อัตโนมัติ
        if self.hp_regen_timer > 0:
            self.hp_regen_timer -= 1

        if self.hp_regen_timer <= 0:
            heal = random.randint(1, 10)
            self.player.hp = min(100, self.player.hp + heal)
            self.hp_regen_timer = 120  # รีเซ็ตนับใหม่อีก 2 วินาที

        if len(self.zombies) == 0 and not self.between_wave:
            self.wave += 1
            self.between_wave = True
            self.between_timer = 180
            self._update_background()

        if self.player.hp <= 0:
            self.player.hp = 0
            self.game_over = True
            (
                update_score(self.username, int(self.score), self.kills)
                if not self.is_guest
                else None
            )

        self.damage_flash.update()

        # อัปเดตเอฟเฟกต์ฟันมีด
        active_slash = []
        for fx in self.slash_effects:
            if fx.get("type") == "sprite":
                fx["frame"] += fx.get("speed", 0.5)

                # --- แก้ให้เอฟเฟกต์เกาะติดตัวผู้เล่น (Move with player) ---
                # อัปเดตมุมให้หมุนตามหน้าตัวละครตลอดเวลา (Sync with player facing)
                # ต้องแปลงมุม Player เป็น Screen Radians เพื่อคำนวณตำแหน่ง
                current_rad = -math.radians(self.player.angle)
                fx["angle"] = current_rad

                # --- ปรับตำแหน่ง (Offset) ---
                forward_offset = 60  # ระยะยื่นไปข้างหน้า
                side_offset = 50  # ระยะขยับซ้าย-ขวา (ค่าบวก = มาทางซ้าย, ค่าลบ = ไปทางขวา)

                # สูตรคำนวณพิกัดใหม่ (หน้า + ข้าง)
                fx["x"] = (
                    self.player.hitbox.centerx
                    + (math.cos(current_rad) * forward_offset)
                    + (math.sin(current_rad) * side_offset)
                )
                fx["y"] = (
                    self.player.hitbox.centery
                    + (math.sin(current_rad) * forward_offset)
                    - (math.cos(current_rad) * side_offset)
                )

                if fx["frame"] < len(self.knife_effect_imgs):
                    active_slash.append(fx)
            else:
                fx["timer"] -= 1
                if fx["timer"] > 0:
                    active_slash.append(fx)
        self.slash_effects = active_slash

        # อัปเดต muzzle flashes (ลดเวลาแสดงผล)
        for mf in self.muzzle_flashes:
            mf["timer"] -= 1
        self.muzzle_flashes = [mf for mf in self.muzzle_flashes if mf["timer"] > 0]

    def _draw_slash_effects(self, surf):
        """SRP: วาดเอฟเฟกต์ฟันมีดแบบกวาดลากซ้าย-ขวา"""
        for fx in self.slash_effects:
            if fx.get("type") == "sprite":
                # --- Draw Sprite Effect ---
                idx = int(fx["frame"])
                if idx < len(self.knife_effect_imgs):
                    img = self.knife_effect_imgs[idx]
                    # หมุนภาพตามทิศทางเม้าส์ (-degrees เพราะ pygame หมุนทวนเข็ม)
                    rot_img = pygame.transform.rotate(img, -math.degrees(fx["angle"]))
                    rect = rot_img.get_rect(center=(fx["x"], fx["y"]))
                    surf.blit(rot_img, rect)
                continue

            # --- Draw Procedural Effect (Legacy) ---
            progress = 1.0 - (fx["timer"] / fx["max_timer"])  # 0→1
            base_angle = fx["angle"]
            radius = fx["radius"] * 1.2  # ขยายรัศมีนิดหน่อยให้พอดี
            sweep = math.pi * 1.1  # กวาดประมาณ 200 องศา (ลดลงจากเดิม)

            # เริ่มกวาดจากด้านหนึ่งไปอีกด้านหนึ่ง
            start_a = base_angle - sweep / 2
            # มุมที่ปลายกวาดถึงตอนนี้ (เร็วกว่าเดิมนิดนึง)
            current_sweep = sweep * (progress**0.8)
            end_a = start_a + current_sweep

            slash_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            num_points = 20

            # วาด trail เลเยอร์ต่างๆ ให้บางลง
            for layer in range(3):
                # ระยะห่างเลเยอร์แคบลง
                r = radius + layer * 4
                points = []
                for i in range(num_points + 1):
                    t = i / num_points
                    a = start_a + current_sweep * t
                    px_pt = fx["x"] + math.cos(a) * r
                    py_pt = fx["y"] + math.sin(a) * r
                    points.append((px_pt, py_pt))

                if len(points) < 2:
                    continue

                # วาดแต่ละ segment โดยสีจางจากหัว→หาง
                for j in range(len(points) - 1):
                    seg_t = j / max(1, len(points) - 2)
                    fade = seg_t**0.6  # ทำให้หางสั้นลง

                    if layer == 0:
                        a_val = int(255 * fade * (1.0 - progress * 0.5))
                        col = (255, 255, 255, max(0, a_val))  # แกนกลางขาวสว่าง
                        w = 3
                    elif layer == 1:
                        a_val = int(200 * fade * (1.0 - progress * 0.6))
                        col = (100, 255, 255, max(0, a_val))  # ฟ้าอ่อน
                        w = 6
                    else:
                        a_val = int(100 * fade * (1.0 - progress * 0.7))
                        col = (0, 150, 255, max(0, a_val))  # น้ำเงินขอบๆ
                        w = 12

                    if a_val > 5:
                        pygame.draw.line(
                            slash_surf,
                            col,
                            (int(points[j][0]), int(points[j][1])),
                            (int(points[j + 1][0]), int(points[j + 1][1])),
                            w,
                        )

            # จุดประกายสว่างวาบที่ปลายกวาด (leading edge)
            tip_alpha = int(255 * (1.0 - progress * 0.3))
            tip_x = fx["x"] + math.cos(end_a) * radius
            tip_y = fx["y"] + math.sin(end_a) * radius

            # Glow รอบปลาย เล็กลงกว่าเดิม
            for gr in range(2, 0, -1):
                ga = max(0, tip_alpha - (3 - gr) * 80)
                pygame.draw.circle(
                    slash_surf,
                    (150, 255, 255, ga),
                    (int(tip_x), int(tip_y)),
                    gr * 4,
                )
            # จุดสว่างแบบแฟลชตรงกลางปลายดาบ เล็กลง
            pygame.draw.circle(
                slash_surf,
                (255, 255, 255, min(255, tip_alpha)),
                (int(tip_x), int(tip_y)),
                4,
            )

            surf.blit(slash_surf, (0, 0))

    def draw(self):
        """
        SRP: method นี้ทำหน้าที่เดียว คือ ประสานการวาดทุกองค์ประกอบ
        DIP: delegate HUD rendering ให้ HUDRenderer
        """
        if hasattr(self, "bg_image") and self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        # --- Background Drawing with Transition ---
        if self.bg_image_night and self.bg_image_day:
            # วาดกลางคืนเป็นฐาน
            screen.blit(self.bg_image_night, (0, 0))
            # วาดกลางวันทับลงไปแบบจางๆ ตามค่า factor
            alpha = int(self.day_night_factor * 255)
            if alpha > 0:
                self.bg_image_day.set_alpha(alpha)
                screen.blit(self.bg_image_day, (0, 0))
        elif self.bg_image_night:
            screen.blit(self.bg_image_night, (0, 0))
        elif self.bg_image_day:
            screen.blit(self.bg_image_day, (0, 0))
        else:
            # Fallback: ถ้าไม่มีรูป BG ให้เปลี่ยนสีพื้นหลังแทน
            is_day = ((self.wave - 1) // 3) % 2 == 1
            bg_col = (60, 70, 60) if is_day else DARK
            screen.fill(bg_col)
            # Fallback: Color Interpolation (เปลี่ยนสีพื้นหลังแบบไล่เฉด)
            c_night = (15, 20, 15)
            c_day = (60, 70, 60)
            t = self.day_night_factor
            r = int(c_night[0] + (c_day[0] - c_night[0]) * t)
            g = int(c_night[1] + (c_day[1] - c_night[1]) * t)
            b = int(c_night[2] + (c_day[2] - c_night[2]) * t)
            screen.fill((r, g, b))

            for tx, ty, ts, tc in self.bg_dots:
                pygame.draw.rect(screen, tc, (tx, ty, ts, ts))

        # วาดพุ่มหญ้า/ถนน
        for dec in self.decorations:
            screen.blit(dec.image, dec.rect)

        for p in self.particles:
            p.draw(screen)

        for pu in self.powerups:
            screen.blit(pu.image, pu.rect)

        for z in self.zombies:
            screen.blit(z.image, z.rect)
            z.draw_hp(screen)

        for obs in self.obstacles:
            screen.blit(obs.image, obs.rect)

        # วาดเท้าของผู้เล่นก่อน (ถ้ามี) เพื่อให้เท้าอยู่ใต้ลำตัว
        if hasattr(self.player, "feet_image"):
            screen.blit(self.player.feet_image, self.player.feet_rect)
        screen.blit(self.player.image, self.player.rect)

        # Draw Muzzle Flashes (วาดทับตัวละครเพื่อให้แสงอยู่บนปืน)
        for mf in self.muzzle_flashes:
            screen.blit(mf["img"], mf["rect"])

        self._draw_slash_effects(screen)
        for b in self.bullets:
            screen.blit(b.image, b.rect)

        # DIP: delegate HUD drawing ให้ HUDRenderer
        self._hud_renderer.draw_hud(screen, self)

        if self.between_wave:
            self._hud_renderer.draw_between_wave(screen, self)

        if self.paused:
            self._hud_renderer.draw_paused(screen, self)

        # ถ้ายืนยันว่าเกมจบแล้ว จะไม่วาดจอแดงทับ (ให้ Game Over ขึ้นมาเด่นๆ เลย)
        if not self.game_over:
            self.damage_flash.draw(screen)

        if self.game_over:
            self._hud_renderer.draw_game_over(screen, self)

        pygame.display.flip()
