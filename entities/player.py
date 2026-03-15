import pygame
import os
import math
from entities.bullet import Bullet

"""
Module: player.py

SOLID Principle — SRP (Single Responsibility Principle):
    class Player รับผิดชอบเฉพาะ logic ของตัวผู้เล่น
    เช่น การเคลื่อนที่ การยิง การเล่น animation และการหมุนตามเมาส์

SOLID Principle — OCP (Open/Closed Principle):
    ระบบอาวุธสามารถเพิ่มชนิดใหม่ได้โดยเพิ่มใน weapon_folders
    โดยไม่ต้องแก้ logic การโหลด sprite หรือ animation

OOP Principle — Encapsulation:
    ข้อมูลของผู้เล่น เช่น hp, speed, shoot_cd, animation state
    ถูกเก็บไว้ภายใน class Player
"""


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        base_path = os.path.dirname(os.path.dirname(__file__))

        # โหลด sprite frames สำหรับอาวุธทุกชนิด
        self.weapon_frames = {}

        # OCP: สามารถเพิ่มอาวุธใหม่ได้โดยเพิ่ม folder ใน dictionary นี้
        weapon_folders = {
            "Rifle": "move_rifle",
            "Pistol": "move_handgun",
            "Shotgun": "move_shotgun",
            "Knife": "move_knife",
        }
        for weapon_name, folder in weapon_folders.items():
            folder_path = os.path.join(base_path, "assets", "images", folder)

            if os.path.isdir(folder_path):

                if weapon_name == "Knife":
                    frames = self._load_frames(folder_path, (64, 64))  # มีดใหญ่
                else:
                    frames = self._load_frames(folder_path, (48, 48))  # ปืนปกติ

            else:
                fallback = os.path.join(base_path, "assets", "images", "move_handgun")
                frames = self._load_frames(fallback, (32, 32))

            self.weapon_frames[weapon_name] = frames

        # --- เพิ่ม: โหลดเฟรมเท้า (ซ้าย/ขวา) ---
        feet_right_path = os.path.join(base_path, "assets", "images", "feet_right")
        feet_left_path = os.path.join(base_path, "assets", "images", "feet_left")

        self.feet_right_frames = (
            self._load_frames(feet_right_path, (16, 16))
            if os.path.isdir(feet_right_path)
            else []
        )
        self.feet_left_frames = (
            self._load_frames(feet_left_path, (16, 16))
            if os.path.isdir(feet_left_path)
            else []
        )

        # Fallback: ถ้ามีแค่ข้างเดียว ให้ flip มาใช้อีกข้างเพื่อความเสถียร
        if self.feet_right_frames and not self.feet_left_frames:
            self.feet_left_frames = [
                pygame.transform.flip(f, True, False) for f in self.feet_right_frames
            ]
        elif self.feet_left_frames and not self.feet_right_frames:
            self.feet_right_frames = [
                pygame.transform.flip(f, True, False) for f in self.feet_left_frames
            ]

        self.feet_frame_index = 0
        self.feet_animation_speed = 0.25
        self.feet_image = pygame.Surface((0, 0), pygame.SRCALPHA)

        # เริ่มต้นด้วย Rifle
        self.move_frames = self.weapon_frames["Rifle"]
        self.animate_on_move = True  # มีดไม่ต้อง animate เวลาเดิน

        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_attacking = False

        self.image = self.move_frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Hitbox สำหรับจัดการการเคลื่อนที่และการชน จะมีขนาดคงที่
        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.hitbox.center = self.rect.center
        self.feet_rect = self.feet_image.get_rect(center=self.hitbox.center)

        self.hp = 100
        self.speed = 3.5
        self.shoot_cd = 0
        self.angle = 0

    def _load_frames(self, folder_path, size=(48, 48)):
        """
        SRP:
            method นี้รับผิดชอบเฉพาะการโหลด sprite frames
            และเตรียม animation ของตัวละคร
        """
        """โหลด sprite frames จากโฟลเดอร์ที่กำหนด"""
        frames = []
        try:
            # พยายามเรียงตามตัวเลขหลัง '_' เช่น 'move_0.png', 'move_1.png'
            file_list = sorted(
                os.listdir(folder_path),
                key=lambda f: int(f.split("_")[-1].split(".")[0]),
            )
        except (ValueError, IndexError):
            # ถ้าเรียงไม่ได้ (เช่น ไม่มี '_') ให้เรียงตามชื่อไฟล์ปกติ
            file_list = sorted(os.listdir(folder_path))

        for file in file_list:
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
                img = pygame.transform.scale(img, size)

                # --- ปรับความสว่างของตัวละคร ---
                # เลข 40 คือระดับความสว่าง ยิ่งเยอะยิ่งสว่าง (เช่น 60, 80, 100)
                brightness = 30
                img.fill(
                    (brightness, brightness, brightness, 0),
                    special_flags=pygame.BLEND_RGBA_ADD,
                )

                frames.append(img)
        return frames

    def switch_weapon(self, weapon_name):
        if weapon_name in self.weapon_frames:
            self.move_frames = self.weapon_frames[weapon_name]
            self.animate_on_move = weapon_name != "Knife"

            self.frame_index = 0

            center = self.rect.center  # เก็บตำแหน่งเดิม
            self.image = self.move_frames[self.frame_index]
            self.rect = self.image.get_rect(center=center)

    def update(self, keys, map_rect, obstacles):
        """
        SRP:
        method นี้จัดการ behaviour ของผู้เล่นในแต่ละ frame
        เช่น movement, collision, animation และ cooldown
        """
        dx = dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed

        moving = dx != 0 or dy != 0

        # Move X
        self.hitbox.x += dx
        if self.hitbox.left < map_rect.left:
            self.hitbox.left = map_rect.left
        if self.hitbox.right > map_rect.right:
            self.hitbox.right = map_rect.right

        for obs in obstacles:
            if self.hitbox.colliderect(obs.rect):
                if dx > 0:
                    self.hitbox.right = obs.rect.left
                elif dx < 0:
                    self.hitbox.left = obs.rect.right

        # Move Y
        self.hitbox.y += dy
        if self.hitbox.top < map_rect.top:
            self.hitbox.top = map_rect.top
        if self.hitbox.bottom > map_rect.bottom:
            self.hitbox.bottom = map_rect.bottom

        # Composition:
        # Player ใช้ Obstacle objects เพื่อจัดการ collision
        # โดยไม่ได้รวม logic ของ obstacle ไว้ใน Player
        for obs in obstacles:
            if self.hitbox.colliderect(obs.rect):
                if dy > 0:
                    self.hitbox.bottom = obs.rect.top
                elif dy < 0:
                    self.hitbox.top = obs.rect.bottom

        # --- อัปเดตอนิเมชั่นเท้า (จะเล่นเมื่อมีการเคลื่อนที่) ---
        if moving and (self.feet_left_frames or self.feet_right_frames):
            # อนิเมชั่นเท้า
            self.feet_frame_index += self.feet_animation_speed
            if self.feet_frame_index >= len(self.feet_right_frames):
                self.feet_frame_index = 0
        elif not moving:
            self.feet_frame_index = 0  # ถ้าหยุดเดิน ให้เท้ากลับไปเฟรมแรก

        if moving and self.animate_on_move:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.move_frames):
                self.frame_index = 0

        if self.is_attacking:
            self.frame_index += self.animation_speed * 2
            if self.frame_index >= len(self.move_frames):
                self.frame_index = 0
                self.is_attacking = False

        # --- อัปเดตภาพและตำแหน่ง ---
        # หมุนลำตัวตามเมาส์ตลอด แม้ยืนนิ่ง
        base_image = self.move_frames[int(self.frame_index)]
        self.rotate_towards_mouse()
        self.image = pygame.transform.rotate(base_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # หมุนเท้าตามทิศทางของเมาส์ โดยใช้ sprite ซ้าย/ขวา ให้ถูกต้อง
        if self.feet_right_frames and self.feet_left_frames:
            # Right hemisphere: -90 to 90 degrees
            if -90 <= self.angle <= 90:
                base_feet_image = self.feet_right_frames[int(self.feet_frame_index)]
                self.feet_image = pygame.transform.rotate(base_feet_image, self.angle)
            # Left hemisphere
            else:
                base_feet_image = self.feet_left_frames[int(self.feet_frame_index)]
                # ชดเชยมุมสำหรับ sprite ที่หันไปทางซ้าย (180 องศา) อยู่แล้ว
                adjusted_angle = self.angle - 180
                self.feet_image = pygame.transform.rotate(
                    base_feet_image, adjusted_angle
                )

            self.feet_rect = self.feet_image.get_rect(center=self.hitbox.center)

        if self.shoot_cd > 0:
            self.shoot_cd -= 1

    def rotate_towards_mouse(self):
        """
        SRP:
            method นี้มีหน้าที่เดียว คือ คำนวณมุมของตัวละคร
            เพื่อให้หันตามตำแหน่งเมาส์
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.hitbox.centerx
        dy = mouse_y - self.hitbox.centery

        self.angle = math.degrees(math.atan2(-dy, dx))

    def shoot(self, bullets):
        """
        SRP:
        method นี้จัดการการยิงกระสุนของผู้เล่น

        Composition:
        Player สร้าง Bullet object และเพิ่มเข้า sprite group
        """

        if self.shoot_cd == 0:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y)

            bullets.add(bullet)

            self.shoot_cd = 10
