"""
Module: weapon.py
SOLID Principle — SRP (Single Responsibility Principle):
    แต่ละ class รับผิดชอบหน้าที่เดียว คือ เก็บข้อมูลและพฤติกรรมของอาวุธแต่ละชนิด

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเพิ่มอาวุธใหม่ได้โดยสร้าง subclass ใหม่ โดยไม่ต้องแก้ไข code ที่มีอยู่

SOLID Principle — LSP (Liskov Substitution Principle):
    subclass ทุกตัวสามารถใช้แทน Weapon ได้ทุกที่โดยไม่ทำให้พฤติกรรมผิดพลาดและเปลี่ยน
"""


class Weapon:
    """
    SRP: class นี้รับผิดชอบเฉพาะข้อมูลพื้นฐานของอาวุธ
    OCP: เพิ่มอาวุธใหม่โดย subclass ไม่ต้องแก้ class นี้
    """

    def __init__(self, name, shoot_cd, damage, auto_fire=False, is_melee=False):
        """
        Parameters
        ----------
        name      : ชื่ออาวุธ (แสดงบน HUD)
        shoot_cd  : cooldown ระหว่างการยิง/โจมตี (frames)
        damage    : ดาเมจต่อครั้ง
        auto_fire : True = กดค้างยิงรัวได้ (Rifle)
        is_melee  : True = โจมตีระยะประชิด ไม่ยิงกระสุน (Knife)
        """
        self.name = name
        self.shoot_cd = shoot_cd
        self.damage = damage
        self.auto_fire = auto_fire
        self.is_melee = is_melee


class Rifle(Weapon):
    """OCP: สร้าง subclass ใหม่เพื่อเพิ่มอาวุธประเภท Rifle"""

    def __init__(self):
        super().__init__(
            name="Rifle",
            shoot_cd=6,
            damage=20,
            auto_fire=True,
            is_melee=False,
        )


class Pistol(Weapon):
    """OCP: สร้าง subclass ใหม่เพื่อเพิ่มอาวุธประเภท Pistol"""

    def __init__(self):
        super().__init__(
            name="Pistol",
            shoot_cd=18,
            damage=20,
            auto_fire=False,
            is_melee=False,
        )


class Knife(Weapon):
    """OCP: สร้าง subclass ใหม่เพื่อเพิ่มอาวุธประเภท Knife"""

    MELEE_RANGE = 90  # รัศมีการฟัน (pixels)

    def __init__(self):
        super().__init__(
            name="Knife",
            shoot_cd=20,
            damage=35,
            auto_fire=False,
            is_melee=True,
        )


class Shotgun(Weapon):
    """OCP: สร้าง subclass ใหม่เพื่อเพิ่มอาวุธประเภท Shotgun"""

    def __init__(self):
        super().__init__(
            name="Shotgun",
            shoot_cd=40,
            damage=15,  # ต่อ 1 กระสุนย่อย (จะยิงออกไปหลายนัดพร้อมกันใน game.py)
            auto_fire=False,
            is_melee=False,
        )
