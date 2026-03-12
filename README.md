# 🧟 Zombie Survival: DEAD ZONE

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6-green)
![Project](https://img.shields.io/badge/OOP-Final%20Project-orange)

โครงงานกลุ่มรายวิชา <br>**1145105-68 การเขียนโปรแกรมเชิงวัตถุ (Object-Oriented Programming – OOP)**

เกมแนว **Top-Down Survival Shooter** พัฒนาด้วยภาษา **Python** และ **PyGame** โดยเน้นการออกแบบซอฟต์แวร์ตามหลักการ **OOP** และ **SOLID Principles** เพื่อให้โค้ดมีความเป็นระบบ อ่านง่าย และสามารถขยายต่อได้ในอนาคต

---


# 👥 สมาชิกในทีม

**Team Name:** Hello Dev 404

| รหัสนักศึกษา | ชื่อ-นามสกุล         | หน้าที่ความรับผิดชอบ         |
| ------------ | -------------------- | ---------------------------- |
| 68114540090  | นายเขษมศักดิ์ แก่นทน | Game Architecture, Game Logic, Systems, Physics, Testing |
| 68114540179  | นายณัฐกรณ์ วันทาสุข  | Game Assets, UI Design          |

---


# 🎮 เกี่ยวกับเกม

**Zombie Survival: DEAD ZONE** เป็นเกมแนว **Top-Down Shooter Survival**
ผู้เล่นจะต้องเอาชีวิตรอดจากฝูง **ซอมบี้ (Zombies)** ที่บุกเข้ามาเป็นระลอก (Wave)

เมื่อเวลาผ่านไป:

* จำนวนซอมบี้จะเพิ่มขึ้น
* ซอมบี้จะมีความยากมากขึ้น
* ผู้เล่นต้องใช้กลยุทธ์ การเคลื่อนที่ และการเลือกใช้อาวุธให้เหมาะสม

โปรเจกต์นี้เน้นการออกแบบระบบให้เป็น **Modular Architecture** เพื่อให้สามารถพัฒนาและขยายเกมต่อได้ง่าย

---


# ✨ ฟีเจอร์หลักของเกม

## 🧟 Wave System

* ซอมบี้จะเกิดเป็น **Wave**
* แต่ละ Wave จะมีจำนวนซอมบี้มากขึ้น
* ความยากเพิ่มขึ้นตามลำดับ

---

## 🔫 Weapon System

ผู้เล่นสามารถใช้อาวุธได้ **4 ประเภท**

| อาวุธ   | รายละเอียด                       |
| ------- | -------------------------------- |
| Rifle   | ปืนยิงอัตโนมัติ ยิงต่อเนื่องได้  |
| Pistol  | ปืนยิงทีละนัด แม่นยำ             |
| Shotgun | ยิงกระสุนกระจาย ดาเมจสูงระยะใกล้ |
| Knife   | อาวุธประชิดตัว                   |

---

## 🌗 Day / Night Cycle

เกมมีระบบ **กลางวัน / กลางคืน**
ทำให้บรรยากาศของฉากเปลี่ยนไปตามเวลา

---

## 👤 User System

* ระบบ **Login / Register**
* บันทึกข้อมูลผู้เล่น
* แสดง **Leaderboard (คะแนนสูงสุด)**

---

## ⚙️ Settings

ผู้เล่นสามารถปรับค่าได้ เช่น

* ระดับเสียง **Music**
* ระดับเสียง **Sound Effects**

---

## 💥 Visual Effects

เกมมีเอฟเฟกต์ต่าง ๆ เช่น

* เอฟเฟกต์เลือด (Blood Particles)
* แสงแฟลชตอนยิงปืน
* เอฟเฟกต์การฟันด้วยมีด

---

# 🎮  Game Controls

| ปุ่ม           | การทำงาน           |
| -------------- | ------------------ |
| **W A S D**    | เคลื่อนที่ตัวละคร  |
| **Mouse**      | เล็งทิศทาง         |
| **Left Click** | ยิง / โจมตี        |
| **1 – 4**      | สลับอาวุธ          |
| **ESC**        | หยุดเกม / เปิดเมนู |

---

# 🧠 การออกแบบซอฟต์แวร์ (OOP & SOLID)

โปรเจกต์นี้ถูกออกแบบโดยใช้หลักการ **SOLID Principles** เพื่อให้โค้ดมีความยืดหยุ่นและง่ายต่อการดูแลรักษา

---

## 1️⃣ Single Responsibility Principle (SRP)

แต่ละ Class มีหน้าที่รับผิดชอบเพียง **หน้าที่เดียว**

ตัวอย่าง

* `Game`
  ทำหน้าที่ควบคุมการทำงานของระบบต่าง ๆ ภายในเกม

* `SpawnManager`
  จัดการการเกิดของซอมบี้ในแต่ละ Wave

* `CollisionHandler`
  จัดการระบบการชนกันของ Object ต่าง ๆ

* `HUDRenderer`
  วาด UI เช่น HP, Score และหน้าจอ Game Over

---

## 2️⃣ Open / Closed Principle (OCP)

ระบบสามารถ **เพิ่มความสามารถใหม่ได้ โดยไม่ต้องแก้ไขโค้ดเดิม**

ตัวอย่าง

* เพิ่มประเภทซอมบี้ใหม่
* เพิ่มหน้าจอใหม่ (Game State)
* เพิ่มเอฟเฟกต์ Particle ใหม่

---

## 3️⃣ Liskov Substitution Principle (LSP)

Class ลูกสามารถใช้แทน Class แม่ได้โดยไม่ทำให้โปรแกรมเกิดข้อผิดพลาด

ตัวอย่าง

* `Zombie` และ `Player` สืบทอดจาก `pygame.sprite.Sprite`
* `BloodParticle` สืบทอดจาก `Particle`

ทำให้สามารถใช้งานร่วมกับ `pygame.sprite.Group` ได้เหมือนกัน

---

## 4️⃣ Dependency Inversion Principle (DIP)

Class ระดับสูงไม่ควรขึ้นกับ Class ระดับล่างโดยตรง
แต่ควรทำงานผ่าน **Abstraction**

ตัวอย่าง

* `Game` เรียกใช้งานระบบย่อยผ่านตัวจัดการ เช่น `_spawn_manager`
* หน้าจอ Leaderboard เรียกใช้ `get_leaderboard()` โดยไม่ต้องรู้ว่าข้อมูลถูกเก็บในไฟล์ JSON


# 📁 โครงสร้างโปรเจกต์ (Project Structure)

```
OOP_FinalProject
│
├── assets/                 # ไฟล์ทรัพยากรของเกม
│   ├── images/             # ภาพตัวละคร แอนิเมชัน เอฟเฟกต์ และซอมบี้
│   └── sound/              # เสียงเอฟเฟกต์และเพลงประกอบเกม
│
├── core/                   # การตั้งค่าหลักของเกม
│   ├── settings.py         # ค่าคงที่และการตั้งค่าต่าง ๆ ของเกม
│   └── fonts.py            # การโหลดและจัดการฟอนต์
│
├── data/                   # การจัดเก็บข้อมูลผู้เล่น
│   └── players.json        # ข้อมูลผู้เล่นและ Leaderboard
│
├── effects/                # เอฟเฟกต์ภาพต่าง ๆ
│   └── damage_flash.py
│
├── entities/               # คลาสของวัตถุในเกม (ใช้แนวคิด OOP)
│   ├── player.py           # คลาสผู้เล่น
│   ├── zombie.py           # คลาสซอมบี้
│   ├── bullet.py           # คลาสกระสุน
│   ├── weapon.py           # ระบบอาวุธ
│   ├── powerup.py          # ไอเทมเสริมพลัง
│   └── obstacle.py         # สิ่งกีดขวางในเกม
│
├── game/                   # Logic หลักของเกมและ Game Loop
│   └── game.py
│
├── screens/                # หน้าจอต่าง ๆ ของเกม
│   ├── main_menu.py        # หน้าเมนูหลัก
│   ├── login_screen.py     # หน้าล็อกอินผู้เล่น
│   ├── leaderboard_screen.py # หน้าแสดงอันดับคะแนน
│   ├── how_to_play.py      # หน้าคำแนะนำการเล่น
│   └── settings_screen.py  # หน้าการตั้งค่า
│
├── systems/                # ระบบย่อยของเกม
│   └── data_manager.py     # จัดการข้อมูลผู้เล่นและ Leaderboard
│
├── ui/                     # ส่วนติดต่อผู้ใช้ (UI Components)
│   └── ui_components.py
│
├── main.py                 # จุดเริ่มต้นของโปรแกรม
├── requirements.txt        # รายการไลบรารีที่ใช้ในโปรเจกต์
├── pyproject.toml          # ไฟล์กำหนดค่าของโปรเจกต์
└── README.md               # เอกสารอธิบายโปรเจกต์

```

---


# 🚀 วิธีติดตั้งและรันโปรแกรม

## 1. Clone Repository

```
git clone https://github.com/kasemsakKK06/OOP-Zombie-Survival-DEAD-ZONE-Game.git
cd OOP-Zombie-Survival-DEAD-ZONE-Game
```

---

## 2. ติดตั้ง Library ที่จำเป็น

```
pip install -r requirements.txt
```

หรือ

```
pip install pygame
```

---

## 3. รันเกม

```
python main.py
```

---


# 📋 Requirements

| Software | Version |
| -------- | ------- |
| Python   | 3.10+   |
| Pygame   | 2.6+    |

---


# 📚 วัตถุประสงค์ทางการศึกษา

โปรเจกต์นี้พัฒนาขึ้นเพื่อใช้เป็น **Final Project ของรายวิชา Object-Oriented Programming**
เพื่อแสดงการประยุกต์ใช้แนวคิดดังต่อไปนี้

* Object-Oriented Programming
* SOLID Principles
* Game Architecture Design
* การพัฒนาเกมด้วย Python และ PyGame

---

<br>

# 🧟 ขอให้คุณรอดจากฝูงซอมบี้ให้ได้นานที่สุด...
