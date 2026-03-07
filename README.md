# OOP Zombie Survival Game

---

## Team Name
Hello 404 Error

---

## Team Members

| ชื่อ-นามสกุล | รหัสนักศึกษา | หน้าที่ |
|------|------------|----------------|
| นายเขษมศักดิ์ แก่นทน | 68114540090 | Game Logic, Player System, Collision Detection |
| นายณัฐกรณ์ วันทาสุข | 68114540179 | Zombie AI, UI Design, Game Testing |
---

## Project Description
Zombie Survival เป็นเกมแนวเอาชีวิตรอด (Survival Game) ที่พัฒนาด้วยภาษา **Python** โดยใช้ Framework **PyGame** ผู้เล่นจะต้องควบคุมตัวละครเพื่อหลบหลีกและต่อสู้กับซอมบี้ที่เข้ามาโจมตี เป้าหมายของเกมคือการเอาชีวิตรอดให้นานที่สุดและทำคะแนนให้สูงที่สุด

โปรเจกต์นี้ถูกพัฒนาขึ้นเพื่อแสดงการประยุกต์ใช้แนวคิด **Object-Oriented Programming (OOP)** และ **SOLID Principles** ในการพัฒนาเกม

---

## 🎮 Features
- Player Movement (ระบบควบคุมตัวละคร)
- Zombie Enemy System (ระบบศัตรูซอมบี้)
- Collision Detection (ระบบตรวจจับการชน)
- Score System (ระบบคะแนน)
- Game Over และ Restart

---

## 🧠 OOP Concepts Used

### Encapsulation
มีการจัดเก็บข้อมูลและฟังก์ชันไว้ภายใน class เช่น `Player`, `Zombie`, และ `Game` เพื่อควบคุมการทำงานของ object

### Inheritance
มีการสร้าง class ลูกที่สืบทอดจาก class พื้นฐาน เช่น `Enemy` → `Zombie`

### Polymorphism
มีการใช้ method ที่ชื่อเดียวกันแต่ทำงานต่างกันในแต่ละ class เช่น `update()` หรือ `draw()`

### Composition
class `Game` ประกอบด้วย object หลายตัว เช่น `Player`, `Zombie` และระบบต่าง ๆ ของเกม

---

## ⚙️ SOLID Principles

### Single Responsibility Principle (SRP)
แต่ละ class มีหน้าที่เฉพาะ เช่น  

- `Player` → ควบคุมตัวละคร  
- `Zombie` → ควบคุมศัตรู  
- `Game` → จัดการระบบเกม  

### Open / Closed Principle (OCP)
สามารถเพิ่ม enemy หรือ feature ใหม่ได้โดยไม่ต้องแก้ไขโค้ดหลักของเกม

---

## 🚀 Installation

### 1. Clone repository

```bash
git clone https://github.com/kasemsakKK06/OOP-Zombie-Survival-Game.git
```

### 2. เข้าไปในโฟลเดอร์โปรเจกต์

```bash
cd OOP-Zombie-Survival-Game
```

### 3. ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

หรือ

```bash
pip install -e .
```

### 4. Run the game

```bash
python main.py
```

---

## 📦 Requirements

- Python 3.10+
- pygame

---

## 📁 Repository Structure

```
OOP-Zombie-Survival-Game
│
├── main.py
├── game.py
├── player.py
├── zombie.py
├── assets/
│   ├── images/
│   └── sounds/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🎥 Demo Video

YouTube Video Link:  
(ใส่ลิงก์วิดีโอที่นี่)