from datetime import datetime
from .views import get_prayer_calendar_context  # ดึง Logic ที่คุณครูเขียนไว้มาใช้

def prayer_navbar_data(request):
    """
    Context Processor สำหรับดึงข้อมูลเวลาละหมาดและสถานที่
    ไปแสดงผลที่ Navbar ในทุกๆ หน้า
    """
    # 1. รับค่าพิกัดจาก GET (ถ้ามีการอัปเดต) หรือจาก Session (ถ้าเคยบันทึกไว้)
    # หากไม่มีเลยให้ใช้ค่า Default (กทม. หรือพิกัดโรงเรียน)
    try:
        lat = float(request.GET.get('lat', request.session.get('user_lat', 13.7563)))
        lng = float(request.GET.get('lng', request.session.get('user_lng', 100.5018)))
        
        # บันทึกพิกัดลง Session ไว้ใช้ในหน้าถัดไปโดยไม่ต้องส่ง Query String
        request.session['user_lat'] = lat
        request.session['user_lng'] = lng
    except (ValueError, TypeError):
        lat, lng = 13.7563, 100.5018

    try:
        # 2. ดึงข้อมูลผ่าน Helper (รวมชื่อสถานที่และตารางเวลา)
        # หมายเหตุ: ฟังก์ชันนี้คำนวณ 30 วัน หากพบว่าหน้าเว็บโหลดช้า 
        # ในอนาคตอาจแยกฟังก์ชันดึงเฉพาะ 'วันนี้' ออกมาต่างหาก
        data = get_prayer_calendar_context(lat, lng)
        
        # 3. กรองหาข้อมูลของ "วันนี้"
        prayer_list = data.get('prayer_calendar_data', [])
        today_data = next((item for item in prayer_list if item.get('is_today')), None)
        
        # หากหา 'is_today' ไม่เจอ (เช่น เปลี่ยนเดือน) ให้เอาตัวแรกของลิสต์มาแสดงก่อน
        if not today_data and prayer_list:
            today_data = prayer_list[0]

        return {
            'nav_prayer_today': today_data,
            'nav_location': data.get('location_name', f"{lat}, {lng}"),
            'latitude': lat,
            'longitude': lng,
        }

    except Exception as e:
        # กรณีเกิด Error (เช่น API ล่ม หรือไม่มี Internet) 
        # ให้ส่งค่าพิกัดกลับไป เพื่อให้ปุ่มอัปเดตยังทำงานได้
        return {
            'nav_prayer_today': None,
            'nav_location': f"{lat}, {lng}",
            'latitude': lat,
            'longitude': lng,
            'nav_error': str(e)
        }