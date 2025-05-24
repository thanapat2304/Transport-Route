## ระบบจัดการข้อมูลการขนส่ง (Transport-Route System)

ระบบนี้เป็นเว็บแอปพลิเคชันสำหรับจัดการข้อมูลการขนส่ง พัฒนาด้วย Flask Framework และใช้ MySQL เป็นฐานข้อมูล

## คุณสมบัติหลัก

- ระบบล็อกอินและการจัดการสิทธิ์ผู้ใช้
- แดชบอร์ดแสดงภาพรวมข้อมูลการขนส่ง
- จัดการข้อมูลการขนส่ง (เพิ่ม/แก้ไข/ลบ)
- ระบบติดตามราคาน้ำมัน (อัพเดตอัตโนมัติทุก 6:00 น.)
- จัดการข้อมูลรถ
- จัดการข้อมูลสาขา
- จัดการข้อมูลเส้นทาง
- ระบบรายงาน
  - รายงานการขนส่ง
  - รายงานตามสาขา
  - รายงานรายเดือน

## การติดตั้งระบบ

1. ติดตั้ง Python 3.x
2. ติดตั้ง dependencies:
```bash
pip install flask
pip install mysql-connector-python
pip install pandas
pip install selenium
pip install webdriver-manager
```

3. ตั้งค่าฐานข้อมูล MySQL:
   - Host: 192.168.10.4
   - Database: aep_portal
   - Charset: utf8

## การตั้งค่า Task Scheduler สำหรับ oil_pd.py

1. เปิด Task Scheduler ใน Windows
2. สร้าง Task ใหม่:
   - ชื่อ Task: "Oil Price Update"
   - Trigger: ทุกวัน เวลา 06:00 น.
   - Action: Start Program
   - Program/script: python
   - Add arguments: oil_pd.py
   - Start in: [path to your workspace]

## การเริ่มต้นใช้งานระบบ

1. รัน Flask application:
```bash
python app.py
```

2. เข้าถึงระบบผ่าน web browser:
```
http://localhost:8080
```

## โครงสร้างไฟล์

- `app.py` - ไฟล์หลักของระบบ
- `oil_pd.py` - ระบบอัพเดตราคาน้ำมันอัตโนมัติ
- `backend/` - โมดูลและฟังก์ชันต่างๆ
- `templates/` - ไฟล์ HTML templates
- `static/` - ไฟล์ CSS, JavaScript, และรูปภาพ

## ความปลอดภัย

- ระบบมีการใช้ session management
- Session timeout ตั้งไว้ที่ 30 นาที
- มีการเข้ารหัส secret key สำหรับ session

## การดูแลรักษาระบบ

- ตรวจสอบ log ของ oil_pd.py เป็นประจำ
- สำรองข้อมูลฐานข้อมูลเป็นประจำ
- ตรวจสอบการทำงานของ Task Scheduler

## หมายเหตุ

- ระบบ oil_pd.py จะทำการดึงข้อมูลราคาน้ำมันจากเว็บไซต์ Bangchak และอัพเดตลงฐานข้อมูลทุกวันเวลา 06:00 น.
- หากไม่สามารถดึงราคาน้ำมันปัจจุบันได้ ระบบจะใช้ราคาน้ำมันของเมื่อวาน 

## ผู้พัฒนา

ธนภัทร โสภณ