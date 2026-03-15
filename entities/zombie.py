"""
Module: zombie.py

SOLID Principle — SRP (Single Responsibility Principle):
    class Zombie มีหน้าที่เดียว คือ จัดการข้อมูลและพฤติกรรมของซอมบี้
    เช่น การสร้างซอมบี้ตามประเภท การเคลื่อนที่เข้าหาผู้เล่น และการวาด HP bar

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเพิ่มประเภทซอมบี้ใหม่ได้โดยเพิ่มข้อมูลใน TYPES list
    โดยไม่ต้องแก้ไข logic ภายใน class

SOLID Principle — LSP (Liskov Substitution Principle):
    Zombie สืบทอดจาก pygame.sprite.Sprite
    จึงสามารถใช้แทน Sprite ได้ทุกที่ เช่น pygame.sprite.Group หรือ groupcollide()
"""

import pygame
import random
import math
import os
from core.settings import BLACK, RED, GREEN, GAME_SETTINGS


class Zombie(pygame.sprite.Sprite):
    """
    SRP:
        class นี้รับผิดชอบเฉพาะพฤติกรรมของซอมบี้

    OCP:
        สามารถเพิ่ม zombie type ใหม่ใน TYPES ได้
        โดยไม่ต้องแก้ไข method ภายใน class

    LSP:
        Zombie เป็น subclass ของ pygame.sprite.Sprite
        จึงสามารถใช้แทน Sprite ได้ในระบบของ pygame
    """

    # ใช้ Class variable เก็บ frames จะได้ไม่ต้องโหลดไฟล์ใหม่ทุกครั้งที่ซอมบี้เกิด
    _frames = None
    _hit_sound = None
    _cry_sound = None
    _attack_sound = None

    # OCP: ประเภทพื้นฐานที่กำหนดความอึด ความเร็ว
    TYPES = [
        {"hp": 30, "speed": 1.5, "dmg": 8, "score": 10},
        {"hp": 60, "speed": 1.0, "dmg": 15, "score": 20},
        {"hp": 100, "speed": 2.2, "dmg": 20, "score": 35},
        {"hp": 200, "speed": 0.8, "dmg": 30, "score": 60},
    ]

    @classmethod
    def load_frames(cls):
        if cls._frames is not None:
            return

        cls._frames = []
        base_path = os.path.dirname(os.path.dirname(__file__))
        folder_path = os.path.join(base_path, "assets", "images", "zombie_move")

        # ถ้าไม่มีโฟลเดอร์ให้ใช้ surface สีแดงสำรอง
        if not os.path.isdir(folder_path):
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(surf, (150, 0, 0), (20, 20), 20)
            pygame.draw.circle(surf, (0, 0, 0), (20, 20), 20, 2)
            cls._frames.append(surf)
            return

        # เลือกเฉพาะรูปตอนเดิน (skeleton-move_*) และไม่ใช่ attack หรือ idle
        move_files = [
            f
            for f in os.listdir(folder_path)
            if f.startswith("skeleton-move_") and f.endswith(".png")
        ]

        # เรียงลำดับตามตัวเลข 0, 1, 2... (เพื่อไม่ให้ 10 มาก่อน 2)
        move_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

        for file in move_files:
            img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
            cls._frames.append(img)

        # กันเหนียวถ้าโฟลเดอร์ว่างเปล่า
        if not cls._frames:
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(surf, (150, 0, 0), (20, 20), 20)
            cls._frames.append(surf)

        # Load Hit Sound (shot_zombie.ogg)
        sound_path = os.path.join(base_path, "assets", "sound", "shot_zombie.ogg")
        if os.path.exists(sound_path):
            cls._hit_sound = pygame.mixer.Sound(sound_path)
            cls._hit_sound.set_volume(0.8)

        # Load Cry Sound (cry_zombie.ogg)
        cry_path = os.path.join(base_path, "assets", "sound", "cry_zombie.ogg")
        if os.path.exists(cry_path):
            cls._cry_sound = pygame.mixer.Sound(cry_path)
            cls._cry_sound.set_volume(0.8)

        # Load Attack Sound (damage_zombie.ogg)
        attack_path = os.path.join(base_path, "assets", "sound", "damage_zombie.ogg")
        if os.path.exists(attack_path):
            cls._attack_sound = pygame.mixer.Sound(attack_path)
            cls._attack_sound.set_volume(2.0)

    def __init__(self, x, y, wave):
        """
        SRP:
            constructor ทำหน้าที่สร้าง zombie ตาม type และ wave
        OCP:
            ใช้ TYPES list จึงเพิ่ม type ใหม่ได้โดยไม่ต้องแก้ method นี้
        """
        super().__init__()

        # โหลดรูปภาพครั้งแรกถ้ายังไม่ได้โหลด
        Zombie.load_frames()

        idx = random.choices([0, 1, 2, 3], weights=[50, 30, 15, 5])[0]
        idx = min(idx, min(wave // 2, 3))
        t = self.TYPES[idx]

        self.hp = t["hp"] + wave * 5
        self.max_hp = self.hp
        self.speed = t["speed"] + wave * 0.05
        self.dmg = t["dmg"]
        self.score_val = t["score"] + wave * 2

        # ขยายขนาดตามเลือด (เลือดเยอะ = ตัวใหญ่)
        self.size = max(30, int(35 + (self.hp / 5)))

        # สเกลรูปภาพตามขนาด (เก็บ frames ของตัวเองที่สเกลแล้ว)
        self.scaled_frames = [
            pygame.transform.scale(img, (self.size, self.size))
            for img in Zombie._frames
        ]

        self.frame_index = 0
        self.animation_speed = 0.15 + (self.speed * 0.05)  # วิ่งเร็ว อนิเมชั่นเร็ว
        self.angle = 0

        self.image = self.scaled_frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Hitbox สำหรับจัดการการเคลื่อนที่และการชน จะมีขนาดคงที่
        # เพื่อป้องกันปัญหาการสั่นจากการหมุนตัวละคร
        self.hitbox = pygame.Rect(0, 0, self.size * 0.7, self.size * 0.7)
        self.hitbox.center = (x, y)

        self.attack_cd = 0
        self.avoid_timer = 0
        self.avoid_dir = (0, 0)

    def update(self, player, obstacles, map_rect):
        """
        SRP:
            method นี้รับผิดชอบการเคลื่อนที่ของ zombie เข้าหาผู้เล่นเท่านั้น

        LSP:
            override update() ตาม interface ของ pygame.sprite.Sprite
            จึงสามารถใช้ใน pygame.sprite.Group.update() ได้
        """
        # คำนวณทิศทางไปหาผู้เล่นจากศูนย์กลางของ hitbox
        dx = player.rect.centerx - self.hitbox.centerx
        dy = player.rect.centery - self.hitbox.centery

        dist = math.hypot(dx, dy)
        if dist < 1:
            vx, vy = 0, 0
        else:
            vx = (dx / dist) * self.speed
            vy = (dy / dist) * self.speed

        # Logic การหลบหลีกเมื่อติดกำแพง
        old_pos = self.hitbox.center
        if self.avoid_timer > 0:
            self.avoid_timer -= 1
            vx, vy = self.avoid_dir

        # --- การเคลื่อนที่แบบแยกแกน (Separate Axis Movement) โดยใช้ Hitbox ---

        # Move X
        self.hitbox.x += vx
        for obs in obstacles:
            if self.hitbox.colliderect(obs.rect):
                if vx > 0:
                    self.hitbox.right = obs.rect.left
                elif vx < 0:
                    self.hitbox.left = obs.rect.right

        # Move Y
        self.hitbox.y += vy
        for obs in obstacles:
            if self.hitbox.colliderect(obs.rect):
                if vy > 0:
                    self.hitbox.bottom = obs.rect.top
                elif vy < 0:
                    self.hitbox.top = obs.rect.bottom

        # เช็คขอบเขตแผนที่
        self.hitbox.clamp_ip(map_rect)

        # ถ้าตำแหน่งไม่ขยับเลย แสดงว่าติด ให้เริ่มโหมดหลบหลีก
        if self.hitbox.center == old_pos and self.avoid_timer == 0 and dist > 1:
            self.avoid_timer = 45
            self.avoid_dir = (
                (self.speed * random.choice([-1, 1]), 0)
                if abs(dy) > abs(dx)
                else (0, self.speed * random.choice([-1, 1]))
            )

        # --- อัปเดตการแสดงผล (Visuals) ---

        # คำนวณมุมและเล่นอนิเมชั่น
        self.angle = math.degrees(math.atan2(-dy, dx))
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.scaled_frames):
            self.frame_index = 0

        # หมุนภาพ และอัปเดต rect ที่ใช้แสดงผล (self.rect) ให้มีจุดศูนย์กลางเดียวกับ hitbox
        base_image = self.scaled_frames[int(self.frame_index)]
        self.image = pygame.transform.rotate(base_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if self.attack_cd > 0:
            self.attack_cd -= 1

        # Random ambient cry (เสียงร้องโหยหวนตอนเดิน)
        if (
            GAME_SETTINGS["sfx_volume"] > 0
            and self._cry_sound
            and random.random() < 0.001
        ):
            self._cry_sound.set_volume(0.8 * GAME_SETTINGS["sfx_volume"])
            self._cry_sound.play()

    def draw_hp(self, surf):
        """
        SRP:
            method นี้รับผิดชอบเฉพาะการวาด HP bar ของ zombie
        """
        bw = self.rect.width
        x = self.rect.x
        y = self.rect.y - 8

        pygame.draw.rect(surf, RED, (x, y, bw, 4))
        pygame.draw.rect(
            surf,
            GREEN,
            (x, y, int(bw * (self.hp / self.max_hp)), 4),
        )

    def play_hit_sound(self):
        if GAME_SETTINGS["sfx_volume"] > 0 and self._hit_sound:
            self._hit_sound.set_volume(0.8 * GAME_SETTINGS["sfx_volume"])
            self._hit_sound.play()

    def play_attack_sound(self):
        if self._attack_sound:
            if GAME_SETTINGS["sfx_volume"] > 0 and self._attack_sound:
                self._attack_sound.set_volume(2.0 * GAME_SETTINGS["sfx_volume"])
                self._attack_sound.play()
