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

โปรเจกต์นี้ถูกออกแบบโดยใช้หลักการ **Object-Oriented Programming (OOP)** และ **SOLID Principles** เพื่อให้โค้ดมีความเป็นระบบ ยืดหยุ่น แก้ไขง่าย และรองรับการขยายตัวในอนาคต

---

## 🏗️ Object-Oriented Programming (OOP)

### 1️⃣ Encapsulation (การห่อหุ้มข้อมูล)
การรวบรวมข้อมูล (Data) และฟังก์ชันการทำงาน (Methods) ไว้ภายใน Class เดียวกัน และซ่อนรายละเอียดที่ไม่จำเป็นไว้ เพื่อป้องกันการแก้ไขข้อมูลโดยไม่ตั้งใจจากภายนอก
* **ในโปรเจกต์นี้:** Class `Player` ไม่ได้เป็นเพียงแค่ตัวเก็บค่าพลังชีวิต แต่ยังรวม Logic การคำนวณ Cooldown การยิง (`shoot_cd`) และการจัดการ Animation ไว้ภายในตัวเอง ทำให้ส่วนอื่นของโปรแกรมสั่งงานผ่าน Method เช่น `shoot()` หรือ `switch_weapon()` โดยไม่ต้องยุ่งกับตัวแปรนับเวลาภายในโดยตรง

### 2️⃣ Inheritance (การสืบทอดคุณสมบัติ)
การนำคุณสมบัติของ Class หลัก (Superclass) มาใช้ใน Class ใหม่ (Subclass) ช่วยลดการเขียนโค้ดซ้ำซ้อน
* **ในโปรเจกต์นี้:** `Player`, `Zombie`, `Bullet` และ `PowerUp` ต่างก็สืบทอดมาจาก **`pygame.sprite.Sprite`** ทำให้ทุกตัวมีคุณสมบัติพื้นฐานเหมือนกัน เช่น `self.image` (รูปภาพ) และ `self.rect` (ตำแหน่ง) และสามารถใช้คำสั่งมาตรฐานของ Pygame ในการวาดและจัดการกลุ่ม (Group) ได้ทันที

### 3️⃣ Polymorphism (การพ้องรูป)
ความสามารถของ Object ที่แตกต่างกัน แต่สามารถตอบสนองต่อคำสั่งเดียวกันได้ในรูปแบบที่ต่างกัน
* **ในโปรเจกต์นี้:** ใน Game Loop มีการเรียกคำสั่ง `sprite.update()` ใส่ทุก Object ในกลุ่ม แต่ละตัวจะทำงานต่างกัน:
  * `Player`: รับค่าปุ่มกดและขยับตัว
  * `Zombie`: เดินไล่ตามผู้เล่น
  * `Bullet`: พุ่งไปข้างหน้า
  * **ประโยชน์:** เราไม่ต้องเขียน `if` เช็คทีละตัวว่าคืออะไร เพียงแค่สั่ง `update()` ทุกตัวก็ทำงานหน้าที่ใครหน้าที่มัน

---

## 📐 SOLID Principles

### 1️⃣ Single Responsibility Principle (SRP)
**"หนึ่ง Class ควรมีหน้าที่เพียงอย่างเดียว"** เพื่อให้โค้ดโฟกัส แก้ไขง่าย และไม่กระทบส่วนอื่น
* `Game`: ทำหน้าที่เป็น "วาทยากร" (Orchestrator) คอยคุมจังหวะเกมเท่านั้น ไม่ลงไปคำนวณเอง
* `SpawnManager`: รับผิดชอบแค่ "การเกิดของซอมบี้" (Wave Logic)
* `CollisionHandler`: รับผิดชอบแค่ "การชน" (ใครชนใคร แล้วเกิดอะไรขึ้น)
* `HUDRenderer`: รับผิดชอบแค่ "การวาด UI" บนหน้าจอ

### 2️⃣ Open / Closed Principle (OCP)
**"เปิดรับการขยาย แต่ปิดกั้นการแก้ไข"** คือเราควรเพิ่มฟีเจอร์ใหม่ได้โดยไม่ต้องไปแก้โค้ดเก่า
* **ในโปรเจกต์นี้:** ระบบซอมบี้และ Power-up ออกแบบเป็น **Data-Driven** (ใช้ List/Dictionary เก็บค่า Config) หากต้องการเพิ่ม **Zombie ชนิดใหม่** สามารถเพิ่มข้อมูลลงใน `Zombie.TYPES` ได้เลย โดยไม่ต้องไปแก้ Logic การเคลื่อนที่หรือการโจมตีใน Class `Zombie`

### 3️⃣ Liskov Substitution Principle (LSP)
**"Class ลูก ต้องสามารถใช้แทน Class แม่ได้สมบูรณ์"**
* **ในโปรเจกต์นี้:** ทุก Entity (`Zombie`, `Bullet`, `PowerUp`) เป็นลูกของ `pygame.sprite.Sprite` เราสามารถโยน Object เหล่านี้เข้าไปใน `pygame.sprite.Group` แล้วสั่ง `draw()` หรือ `update()` ได้เหมือนกันหมด โดยที่โปรแกรมไม่พังและไม่ต้องแก้โค้ดส่วนจัดการ Sprite

### 4️⃣ Dependency Inversion Principle (DIP)
**"Class หลักไม่ควรผูกติดกับ Class ย่อยโดยตรง แต่ควรคุยกันผ่านตัวกลางหรือ Abstraction"**
* **ในโปรเจกต์นี้:** `Game` ไม่ได้เขียน Logic การชนหรือการเกิดซอมบี้ไว้ในตัวเองตรงๆ แต่เรียกใช้ผ่าน Instance ของ `CollisionHandler` และ `SpawnManager`
* **ประโยชน์:** ลดความซับซ้อนภายใน Class `Game` และทำให้ง่ายต่อการแยกส่วนไปทดสอบหรือแก้ไข


# 📁 โครงสร้างโปรเจกต์ (Project Structure)
```
OOP-Zombie-Survival-Game
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
git clone https://github.com/kasemsakKK06/OOP-Zombie-Survival-Game.git
cd OOP-Zombie-Survival-Game
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
