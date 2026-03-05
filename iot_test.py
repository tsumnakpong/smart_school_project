import requests
import json

# 1. ตั้งค่า URL (ตรวจสอบพอร์ตให้ตรงกับที่รัน manage.py runserver)
API_URL = "http://127.0.0.1:8000/iot/api/checkin/"

# 2. ใส่รหัส Student ID ให้ตรงกับในหน้า Admin (SMS > Students)
# *** สำคัญ: ต้องเป็นรหัสเดียวกับที่คุณเห็นในหน้า Admin เป๊ะๆ ***
test_students = ["STD001","69001"] 

def run_test():
    print("🚀 เริ่มต้นการส่งข้อมูลจำลองจากอุปกรณ์ AIoT...")
    print("-" * 50)

    for s_id in test_students:
        payload = {
            "student_id": s_id,
            "device_id": "GATE-01"
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 201:
                print(f"✅ สำเร็จ: รหัส {s_id} เช็คชื่อเรียบร้อย!")
                print(f"   [Server Response]: {response.json()}")
            elif response.status_code == 404:
                print(f"❌ ล้มเหลว: ไม่พบรหัส {s_id} ในฐานข้อมูล SMS")
                print(f"   [คำแนะนำ]: ไปเช็คที่ Admin > SMS > Students ว่ามีรหัสนี้จริงไหม")
            else:
                print(f"⚠️ พลาด: Server ตอบกลับด้วยสถานะ {response.status_code}")
                print(f"   [Detail]: {response.text}")
                
        except Exception as e:
            print(f"🛑 Error: ไม่สามารถเชื่อมต่อกับ Server ได้ ({e})")
            print("   [คำแนะนำ]: คุณรัน 'python manage.py runserver' ค้างไว้หรือยัง?")

    print("-" * 50)
    print("🏁 จบการทดสอบ")

if __name__ == "__main__":
    run_test()