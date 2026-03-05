from django.shortcuts import render, get_object_or_404
from iot.models import AttendanceLog
from sms.models import Student
from django.utils import timezone
import datetime # เพิ่มการ import datetime
# อย่าลืม import Model ของ News มาด้วยนะครับ (ถ้าสร้างไว้แล้ว)
# from .models import News

def home(request):
    # ดึงเวลาปัจจุบันในไทย
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    total_students = Student.objects.count()
    
    # กรองข้อมูล Attendance ที่เกิดขึ้นภายในวันนี้
    present_today = AttendanceLog.objects.filter(
        timestamp__range=(today_start, today_end)
    ).values('student').distinct().count()
    
    print(f"DEBUG: ช่วงเวลา={today_start} ถึง {today_end}")
    print(f"DEBUG: ทั้งหมด={total_students}, มาเรียน={present_today}")
    
    attendance_percent = 0
    if total_students > 0:
        attendance_percent = (present_today / total_students) * 100
        
    context = {
        'attendance_percent': round(attendance_percent, 1),
        'total_students': total_students,
        'present_count': present_today,
    }
    return render(request, 'cms/index.html', context)

# ฟังก์ชันหน้า About ที่เราทำกันก่อนหน้านี้
def about_view(request):
    return render(request, 'cms/about.html')

# เพิ่มฟังก์ชันที่ระบบฟ้องว่าหาไม่เจอ (manage_news)
def manage_news(request):
    return render(request, 'cms/manage_news.html')

# แถม: ฟังก์ชันอื่นๆ ที่เราใส่ไว้ใน urls.py ก่อนหน้านี้ 
# ถ้าใน urls.py มีชื่อพวกนี้ ต้องใส่ในนี้ให้ครบด้วยนะครับ
def news_list(request):
    return render(request, 'cms/news_list.html')

def news_detail(request, pk):
    return render(request, 'cms/news_detail.html')

def news_create(request):
    return render(request, 'cms/news_form.html')

def news_edit(request, pk):
    return render(request, 'cms/news_form.html')

def news_delete(request, pk):
    return render(request, 'cms/news_confirm_delete.html')

def curriculum_view(request):
    return render(request, 'cms/curriculum.html')

def museum_view(request):
    return render(request, 'cms/museum.html')

def learning_view(request):
    return render(request, 'cms/online_learning.html')

def games_view(request):
    return render(request, 'cms/educational_games.html')

def contact_view(request):
    return render(request, 'cms/contact.html')



