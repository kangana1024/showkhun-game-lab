# S2E01 — แท่นกระพริบ (Roblox)

เป้าหมาย: ทำด่านกระโดด 3 แท่นลอยเหนือเหว แล้วเขียนสคริปต์แรกให้แท่นเปลี่ยนสีทุกครึ่งวินาที

Roblox ใช้ภาษา **Luau** ที่ต่อยอดมาจาก Lua

ทุกบั๊กในตอนนี้พังจริงใน Roblox Studio 0.742 และแก้แล้วหายจริง ข้อความ error ด้านล่างคัดมาจาก Output ตรงๆ

| ไฟล์ | เกิดอะไรขึ้น | วิธีแก้ |
|---|---|---|
| `bug-fall.rbxlx` | กดรันแล้ว **แท่นร่วงลงเหวหมด** เพราะแท่นยังไม่ได้ยึดไว้ | เลือกทั้ง 3 แท่น แล้วติ๊ก **Anchored** |
| `bug-typo.rbxlx` | Output ขึ้นตัวแดง `Brickcolor is not a valid member of Part "Workspace.Part"` เพราะพิมพ์ c ตัวเล็ก | แก้เป็น **`BrickColor`** (Luau แยกตัวเล็กตัวใหญ่) |
| `bug-timeout.rbxlx` | เกมค้าง แล้วขึ้น `Script timeout: exhausted allowed execution time` เพราะลูปวิ่งไม่ยอมพัก | ใส่ **`task.wait(0.5)`** ในลูป |
| `fix.rbxlx` | แท่นกระพริบเปลี่ยนสีทุกครึ่งวินาที กระโดดผ่านได้ครบ | — |

โค้ดสุดท้าย (`Blink.server.luau`):

```lua
local part = script.Parent
while true do
	part.BrickColor = BrickColor.random()
	task.wait(0.5)
end
```

## เปิดไฟล์ `.rbxlx`

ดับเบิลคลิกไฟล์ หรือเปิด Roblox Studio แล้วไปที่ **File → Open from File…**

## ดูทีละขั้นว่าแก้อะไร

```bash
git diff s2e01-bug2 s2e01-bug3 -- roblox/s2e01-blink/Blink.server.luau   # แก้บั๊ก 2 (Brickcolor → BrickColor)
git diff s2e01-bug3 s2e01-fix  -- roblox/s2e01-blink/Blink.server.luau   # แก้บั๊ก 3 (ใส่ task.wait)
```

`Blink.server.luau` คือสคริปต์ในแท่นแรก ดึงออกมาจากไฟล์ place ด้วย `python3 tools/rbxlx.py script <ไฟล์>.rbxlx`
