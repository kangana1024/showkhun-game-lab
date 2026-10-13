# Showkhun Game Lab

โปรเจกต์ประกอบซีรีส์สอนเขียนเกมด้วย Scratch และ Roblox (Luau) ของ Showkhun Lab
เก็บไฟล์โปรเจกต์ Scratch (`.sb3`) และ Roblox place (`.rbxlx`) ของแต่ละตอน กับเครื่องมือ Python เล็กๆ สำหรับอ่านไฟล์

## ตอนที่ทำแล้ว

| ตอน | บั๊ก | วิธีแก้ | ไฟล์ | คลิป |
|---|---|---|---|---|
| S1E01 หยองหยองเดินซ้าย-ขวา | ไม่ขยับ / กลับหัว / หายเข้าขอบจอ | วนซ้ำตลอด / หมุนแบบซ้าย-ขวา / ตั้งค่า x ไม่ให้เกิน ±200 | [scratch/s1e01-move](scratch/s1e01-move) | [YouTube](https://youtu.be/sGut0VtfFC8) · [Facebook](https://www.facebook.com/reel/2181042402483792) |
| S2E01 แท่นกระพริบ (Roblox) | แท่นร่วง / Brickcolor error / Script timeout | Anchored / BrickColor / task.wait(0.5) | [roblox/s2e01-blink](roblox/s2e01-blink) | [YouTube](https://youtu.be/wXPtPNyInH8) · [Facebook](https://www.facebook.com/reel/1993806684643365) |

## วิธีเปิดไฟล์ `.sb3`

1. เปิด Scratch (scratch.mit.edu/projects/editor)
2. ไปที่ **ไฟล์ → โหลดจากคอมพิวเตอร์**
3. เลือกไฟล์ `.sb3` ที่ต้องการ

## วิธีเปิดไฟล์ `.rbxlx` (Roblox)

ดับเบิลคลิกไฟล์ หรือเปิด Roblox Studio แล้วไปที่ **File → Open from File…**

## วิธีดูการแก้บั๊ก

แต่ละตอนมี tag ทีละขั้น เช่น `s1e01-bug1` … `s1e01-bug3`, `s1e01-fix` และ `s2e01-bug1` … `s2e01-fix`

```bash
git diff s1e01-bug1 s1e01-fix -- scratch/s1e01-move/project.json
```

## เครื่องมือ `tools/sb3.py`

```bash
python3 tools/sb3.py dump in.sb3 out.json
```

แปลง `project.json` ในไฟล์ `.sb3` เป็น JSON ที่จัดรูปแบบคงที่ เพื่อให้ `git diff` อ่านง่าย

## เครื่องมือ `tools/rbxlx.py`

```bash
python3 tools/rbxlx.py script place.rbxlx
```

พิมพ์โค้ดของ Script ในไฟล์ Roblox place (`.rbxlx`) ออกมา

## ลิขสิทธิ์

โค้ดในโปรเจกต์นี้อยู่ภายใต้ MIT License (ดู [LICENSE](./LICENSE))

ตัวละครหยองหยองเป็นของ Showkhun Lab ไม่อยู่ใต้ MIT — ใช้ในโปรเจกต์ฝึกเขียนเกมได้
