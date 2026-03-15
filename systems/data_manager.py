"""
Module: data_manager.py
SOLID Principle — SRP (Single Responsibility Principle):
    แยกหน้าที่ออกเป็น 2 class:
      - JsonFileHandler: รับผิดชอบแค่การอ่าน/เขียนไฟล์ JSON
      - PlayerRepository: รับผิดชอบแค่ business logic ของ player data

SOLID Principle — OCP (Open/Closed Principle):
    สามารถเปลี่ยน storage backend ได้ (เช่น SQLite, API)
    โดยสร้าง Handler class ใหม่แทน JsonFileHandler โดยไม่แก้ PlayerRepository

SOLID Principle — DIP (Dependency Inversion Principle):
    PlayerRepository ไม่ผูกติดกับ JSON format โดยตรง
    แต่ขึ้นกับ JsonFileHandler (abstraction layer) ที่สามารถเปลี่ยนได้
"""

import json
import os
import hashlib
from core.settings import DATA_FILE


class JsonFileHandler:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว จัดการการอ่าน/เขียนไฟล์ JSON เท่านั้น
    Infrastructure Layer ของระบบจัดเก็บข้อมูล

    OCP: สามารถสร้าง class อื่น (e.g. SqliteHandler) แทนได้โดยไม่แก้ class นี้
    """

    def __init__(self, file_path):
        """SRP: constructor กำหนด path ของไฟล์ที่จะจัดการ"""
        self._file_path = file_path

    def load(self):
        """SRP: method นี้ทำหน้าที่เดียว คือ อ่านข้อมูลจากไฟล์ JSON"""
        if os.path.exists(self._file_path):
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"players": []}

    def save(self, data):
        """SRP: method นี้ทำหน้าที่เดียว คือ เขียนข้อมูลลงไฟล์ JSON"""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class PlayerRepository:
    """
    SRP: class นี้รับผิดชอบหน้าที่เดียว คือ business logic ของ player data
         (ค้นหา, สมัคร, อัปเดตคะแนน, ดึง leaderboard)

    DIP: ขึ้นกับ file_handler (abstraction) ไม่ผูกติดกับ JSON format โดยตรง
    OCP: เพิ่ม method ใหม่ได้โดยไม่แก้ method เดิม
    """

    def __init__(self, file_handler):
        """
        DIP: รับ file_handler เป็น dependency injection
            ทำให้เปลี่ยน storage backend ได้โดยไม่แก้ class นี้
        """
        self._file_handler = file_handler

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_player(self, username):
        """SRP: method นี้ทำหน้าที่เดียว คือ ค้นหาผู้เล่นจากชื่อ"""
        data = self._file_handler.load()
        for p in data["players"]:
            if p["username"].lower() == username.lower():
                return p
        return None

    def register_player(self, username, password):
        """SRP: method นี้ทำหน้าที่เดียว คือ สมัครสมาชิกผู้เล่นใหม่"""
        data = self._file_handler.load()
        for p in data["players"]:
            if p["username"].lower() == username.lower():
                return False, "ชื่อผู้ใช้นี้มีอยู่แล้ว"

        data["players"].append(
            {
                "username": username,
                "password": self._hash_password(password),
                "best_score": 0,
                "games_played": 0,
                "total_kills": 0,
            }
        )
        self._file_handler.save(data)
        return True, "สมัครสมาชิกสำเร็จ!"

    def validate_login(self, username, password):
        """SRP: ตรวจสอบชื่อผู้ใช้และรหัสผ่าน (ใช้ Hash Comparison)"""
        p = self.get_player(username)
        if p and p["password"] == self._hash_password(password):
            return p
        return None

    def update_score(self, username, score, kills):
        """SRP: method นี้ทำหน้าที่เดียว คือ อัปเดตคะแนนของผู้เล่น"""
        data = self._file_handler.load()
        for p in data["players"]:
            if p["username"] == username:
                p["games_played"] += 1
                p["total_kills"] += kills
                if score > p["best_score"]:
                    p["best_score"] = score
        self._file_handler.save(data)

    def get_leaderboard(self):
        """SRP: method นี้ทำหน้าที่เดียว คือ ดึงข้อมูล leaderboard เรียงตามคะแนน"""
        data = self._file_handler.load()
        return sorted(data["players"], key=lambda x: x["best_score"], reverse=True)


# ─── Backward-Compatible Module-Level Functions ─────────────────────────────
# DIP: สร้าง default instances โดยใช้ dependency injection
_default_handler = JsonFileHandler(DATA_FILE)
_default_repo = PlayerRepository(_default_handler)


def load_data():
    """Backward compatible: เรียกผ่าน JsonFileHandler"""
    return _default_handler.load()


def save_data(data):
    """Backward compatible: เรียกผ่าน JsonFileHandler"""
    _default_handler.save(data)


def get_player(username):
    """Backward compatible: เรียกผ่าน PlayerRepository"""
    return _default_repo.get_player(username)


def register_player(username, password):
    """Backward compatible: เรียกผ่าน PlayerRepository"""
    return _default_repo.register_player(username, password)


def validate_login(username, password):
    """Backward compatible: เรียกผ่าน PlayerRepository"""
    return _default_repo.validate_login(username, password)


def update_score(username, score, kills):
    """Backward compatible: เรียกผ่าน PlayerRepository"""
    return _default_repo.update_score(username, score, kills)


def get_leaderboard():
    """Backward compatible: เรียกผ่าน PlayerRepository"""
    return _default_repo.get_leaderboard()
