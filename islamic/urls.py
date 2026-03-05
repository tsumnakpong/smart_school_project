from django.urls import path
from . import views

app_name = 'islamic'

urlpatterns = [
    # หน้าแสดงเวลาละหมาด (Prayer Times)
    path('prayer-times/', views.prayer_times_view, name='prayer_times'),
    
    # หน้าเข็มทิศกิบลัต (Qibla Compass)
    path('qibla/', views.qibla_compass, name='qibla'),
    
    # หน้าหลักอัลกุรอาน - รายชื่อซูเราะฮ์ (Quran List)
    path('quran/', views.quran_list, name='quran'),
    
    # หน้าอ่านอัลกุรอาน - เนื้อหาอายะฮ์ (Quran Detail)
    path('quran/<int:chapter_id>/', views.quran_detail, name='quran_detail'),
    
    # เพิ่มหน้าดุอาอ์ (Dua List) เพื่อให้ปุ่มใน Botbar ทำงานได้จริง
    path('duas/', views.dua_list, name='dua_list'),

    path('calendar/', views.islamic_calendar_view, name='prayer_calendar'),
    path('calendar/download/', views.export_prayer_pdf, name='download_pdf'),
]