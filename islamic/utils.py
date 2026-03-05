import requests
from hijri_converter import Gregorian
from prayer_times_calculator import PrayerTimesCalculator
from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO

from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from hijri_converter import Gregorian
from prayer_times_calculator import PrayerTimesCalculator





# 1. ฟังก์ชันดึงชื่อสถานที่ (แยกไว้เพื่อความเป็นระเบียบ)

def get_location_name(lat, lng):
    try:
        geolocator = Nominatim(user_agent="smart_school_app_v2")
        location = geolocator.reverse(f"{lat}, {lng}", timeout=10, language='th')
        if location:
            addr = location.raw.get('address', {})
            amphoe = addr.get('amphoe') or addr.get('district') or addr.get('city_district') or ''
            province = addr.get('province') or addr.get('state') or ''
            amphoe = amphoe.replace('อำเภอ', '').replace('เขต', '').strip()
            province = province.replace('จังหวัด', '').strip()
            if amphoe and province:
                return f"อ.{amphoe} จ.{province}"
            return f"จ.{province}" if province else f"{lat}, {lng}"
    except:
        pass
    return f"พิกัด: {lat}, {lng}"

# 2. ฟังก์ชันเตรียมข้อมูลหลัก (รวม Imsak -5 นาที และ วันที่ไทย พ.ศ.)
def get_prayer_calendar_context(lat, lng):
    today_gregorian = datetime.now()
    today_hijri = Gregorian(today_gregorian.year, today_gregorian.month, today_gregorian.day).to_hijri()
    
    # รายชื่อเดือนไทยสำหรับการแสดงผล พ.ศ.
    thai_months = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    thai_days = {"Monday": "จันทร์", "Tuesday": "อังคาร", "Wednesday": "พุธ", "Thursday": "พฤหัสฯ", "Friday": "ศุกร์", "Saturday": "เสาร์", "Sunday": "อาทิตย์"}

    prayer_data = []
    # เริ่มวันที่ 1 ของเดือนฮิจเราะฮ์ปัจจุบัน
    start_date = today_gregorian - timedelta(days=today_hijri.day - 1)
    
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        calc = PrayerTimesCalculator(
            latitude=lat, longitude=lng,
            calculation_method='karachi',
            date=current_date.strftime("%Y-%m-%d")
        )
        times = calc.fetch_prayer_times()
        
        # --- กฎอิมซาก: ซุบฮิ (Fajr) ลบ 5 นาที ---
        fajr_time = datetime.strptime(times['Fajr'], "%H:%M")
        imsak_time = (fajr_time - timedelta(minutes=5)).strftime("%H:%M")
        
        # --- Format วันที่ไทย (พ.ศ.) ---
        day_name_th = thai_days.get(current_date.strftime("%A"), current_date.strftime("%A"))
        thai_date_str = f"{current_date.day} {thai_months[current_date.month]} {current_date.year + 543}"

        h = Gregorian(current_date.year, current_date.month, current_date.day).to_hijri()
        
        prayer_data.append({
            'hijri_day': h.day,
            'gregorian_day': thai_date_str,
            'day_name': day_name_th,
            'imsak': imsak_time,
            'fajr': times['Fajr'],
            'sunrise': times['Sunrise'],
            'dhuhr': times['Dhuhr'],
            'asr': times['Asr'],
            'maghrib': times['Maghrib'],
            'isha': times['Isha'],
            'is_today': current_date.date() == today_gregorian.date(),
            'is_friday': current_date.weekday() == 4,
        })
    
    return {
        'prayer_calendar_data': prayer_data,
        'today_hijri': today_hijri,
        'today_gregorian': today_gregorian,
        'location_name': get_location_name(lat, lng)
    }


# ใน islamic/utils.py

# ฟังก์ชันเสริมที่ mis/views.py เรียกใช้ (ถ้ามี)
def get_prayer_times(lat, lng):
    data = get_prayer_calendar_context(lat, lng)
    return next((item for item in data['prayer_calendar_data'] if item['is_today']), None)
    