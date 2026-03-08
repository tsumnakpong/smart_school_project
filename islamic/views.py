import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import get_prayer_times
from django.shortcuts import render
from .utils import get_prayer_calendar_context
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
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



# 3. View สำหรับหน้าเว็บ
# islamic/views.py
from .utils import get_prayer_calendar_context

def islamic_calendar_view(request):
    # 1. พยายามดึงจาก GET (ลำดับความสำคัญสูงสุด)
    lat_param = request.GET.get('lat')
    lng_param = request.GET.get('lng')

    if lat_param and lng_param:
        lat = float(lat_param)
        lng = float(lng_param)
        # บันทึกพิกัดลง Session เพื่อให้ PDF และหน้าอื่นๆ ใช้ต่อได้
        request.session['user_lat'] = lat
        request.session['user_lng'] = lng
    else:
        # 2. ถ้าใน URL ไม่มี ให้ดึงจาก Session (ถ้าเคยมี) หรือใช้ค่า Default (นครศรีฯ)
        lat = request.session.get('user_lat', 8.4351)
        lng = request.session.get('user_lng', 99.9631)

    # ดึงข้อมูลผ่าน Helper
    data = get_prayer_calendar_context(lat, lng)
    
    context = {
        **data,
        'lat': lat,
        'lng': lng,
        'current_hijri_month_name': data['today_hijri'].month_name(),
        'current_hijri_year': data['today_hijri'].year,
    }
    return render(request, 'islamic/prayer_calendar.html', context)

def export_prayer_pdf(request):
    # 1. รับค่าพิกัด
    lat = float(request.GET.get('lat', 13.7563))
    lng = float(request.GET.get('lng', 100.5018))
    
    # 2. ดึงข้อมูลจาก Helper (จุดนี้สำคัญที่สุด! ข้อมูลจะเหมือนหน้าเว็บเป๊ะ)
    data = get_prayer_calendar_context(lat, lng)
    prayer_calendar_data = data['prayer_calendar_data']
    today_hijri = data['today_hijri']
    location_name = data['location_name']

    # 3. เตรียม Font ภาษาไทย
    # ตรวจสอบว่ามีไฟล์ static/fonts/THSarabunNew.ttf ในโปรเจกต์นะครับ
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'THSarabunNew.ttf')
    pdfmetrics.registerFont(TTFont('ThaiFont', font_path))
    pdfmetrics.registerFont(TTFont('ThaiFontBold', font_path))

    # 4. สร้าง PDF Template
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    
    # สร้าง Styles
    style_center = ParagraphStyle(name='Center', fontName='ThaiFont', fontSize=22, alignment=1, spaceAfter=10)
    style_sub = ParagraphStyle(name='Sub', fontName='ThaiFont', fontSize=14, alignment=1, textColor=colors.grey)

    # 5. หัวข้อปฏิทิน
    title = f"<b>ตารางเวลาละหมาด เดือน {today_hijri.month_name()} ฮ.ศ. {today_hijri.year}</b>"
    elements.append(Paragraph(title, style_center))
    
    # แสดงชื่อสถานที่จากพิกัด (อ. และ จ.)
    sub_title = f"สถานที่: {location_name} | โรงเรียนสมาร์ทสคูล"
    elements.append(Paragraph(sub_title, style_sub))
    
    # เส้นคั่นสีทองสวยๆ
    elements.append(Spacer(1, 5))
    elements.append(HRFlowable(width="90%", thickness=1, color=colors.HexColor("#C5A059"), spaceAfter=15))

    # 6. ข้อมูลตาราง (ดึงจาก d['...'] ที่เราคำนวณไว้ใน Helper)
    table_data = [['ฮ.ศ.', 'วันที่ไทย', 'วัน', 'อิมซาก', 'ซุบฮิ', 'ชูรูก', 'ซุฮรี', 'อัศรี', 'มักริบ', 'อิชาอ์']]
    
    for d in prayer_calendar_data:
        table_data.append([
            d['hijri_day'],
            d['gregorian_day'], # วันที่ไทย พ.ศ. (เช่น 3 มี.ค. 2569)
            d['day_name'],      # ชื่อวันไทย
            d['imsak'],         # Fajr - 5 นาที
            d['fajr'],
            d['sunrise'],
            d['dhuhr'],
            d['asr'],
            d['maghrib'],
            d['isha']
        ])

    # 7. สร้าง Table และใส่ Style
    # ปรับความกว้างคอลัมน์ให้พอดี (A4 แนวนอน หรือ แนวตั้งตามความเหมาะสม)
    t = Table(table_data, colWidths=[25, 75, 45, 45, 45, 45, 45, 45, 45, 45])
    
    style = TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'ThaiFont'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#10B981")), # สีเขียวอิสลาม
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
    ])
    t.setStyle(style)
    elements.append(t)

    # 8. สรุปท้ายไฟล์
    elements.append(Spacer(1, 15))
    footer_text = f"<i>* เวลาอิมซากคำนวณก่อนเวลาซุบฮิ 5 นาที | ออกโดยระบบ SmartSchool Islamic App</i>"
    elements.append(Paragraph(footer_text, ParagraphStyle('Footer', fontName='ThaiFont', fontSize=10, alignment=1)))

    # 9. ส่งไฟล์ออก
    doc.build(elements)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Prayer_Schedule_{today_hijri.year}_{today_hijri.month}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()
    return response


# --- หน้าแสดงเวลาละหมาด ---
@login_required
def prayer_times_view(request):
    try:
        prayer_times = get_prayer_times()
        if not prayer_times:
            messages.warning(request, "ไม่สามารถดึงข้อมูลเวลาละหมาดได้ในขณะนี้")
    except Exception as e:
        prayer_times = None
        messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")
        
    return render(request, 'islamic/prayer_times.html', {
        'prayer_times': prayer_times,
        'location': 'Nakhon Si Thammarat' # คุณครูสามารถดึงจาก Profile ได้
    })

# --- หน้าแสดงรายชื่อซูเราะฮ์ (Quran List) ---
@login_required
def quran_list(request):
    try:
        url = "https://api.quran.com/api/v4/chapters?language=th"
        response = requests.get(url, timeout=10) # เพิ่ม timeout กันค้าง
        response.raise_for_status() # เช็คว่า API return error code หรือไม่
        data = response.json()
        chapters = data.get('chapters', [])
    except requests.exceptions.RequestException:
        chapters = []
        messages.error(request, "ไม่สามารถเชื่อมต่อกับฐานข้อมูลอัลกุรอานได้")

    return render(request, 'islamic/quran_list.html', {'chapters': chapters})

# --- หน้าแสดงเนื้อหาซูเราะฮ์ (Quran Detail) ---
@login_required
def quran_detail(request, chapter_id):
    # ดึงข้อมูลเบื้องต้นของซูเราะฮ์ (เช่น ชื่อซูเราะฮ์) มาแสดงก่อน
    # เพื่อให้ UI ดูดีระหว่างที่ JavaScript กำลังโหลดเนื้อหาอายะฮ์
    context = {
        'chapter_id': chapter_id,
    }
    return render(request, 'islamic/quran_detail.html', context)

# --- หน้าเข็มทิศกิบลัต ---
@login_required
def qibla_compass(request):
    return render(request, 'islamic/qibla.html')

# --- หน้าดุอาอ์ (เพิ่มมาเผื่อคุณครูใช้งาน) ---
@login_required
def dua_list(request):
    return render(request, 'islamic/dua_list.html')