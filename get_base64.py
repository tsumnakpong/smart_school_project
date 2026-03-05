import base64
import os

# ระบุตำแหน่งไฟล์ฟอนต์ (ตรวจสอบว่าชื่อไฟล์สะกดตรงกันนะครับ)
font_path = os.path.join('static', 'fonts', 'THSarabunNew.ttf')

try:
    with open(font_path, "rb") as font_file:
        # แปลงเป็น Base64
        encoded_string = base64.b64encode(font_file.read()).decode('utf-8')
        
        # บันทึกรหัสลงในไฟล์ text เพื่อให้ก๊อปปี้ง่ายๆ
        with open("font_base64.txt", "w") as f:
            f.write(encoded_string)
            
    print("สำเร็จ! รหัสถูกสร้างไว้ในไฟล์ 'font_base64.txt' แล้วครับ")
    print("ให้ครูเปิดไฟล์นั้นแล้วก๊อปปี้รหัสทั้งหมดไปใช้ได้เลย")
except FileNotFoundError:
    print(f"หาไฟล์ไม่เจอที่: {font_path} ครูลองเช็คตำแหน่งไฟล์อีกทีนะครับ")