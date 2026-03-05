from django.urls import path
from . import views

# กำหนด app_name เพื่อใช้ในการเรียก {% url 'lms:...' %}
app_name = 'lms'

urlpatterns = [
    # --- 1. Dashboard แยกตามบทบาท ---
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    path('portfolio/<int:student_id>/', views.student_portfolio, name='student_portfolio'),

    # --- 2. การเรียนและ AI Tutor (LMS) ---
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('ai-chat/<int:lesson_id>/', views.ai_tutor_chat, name='ai_tutor_chat'),
    path('clear-chat/<int:lesson_id>/', views.clear_chat_history, name='clear_chat_history'),
    path('generate-quiz/<int:lesson_id>/', views.generate_quiz, name='generate_quiz'),
    path('save-quiz-score/<int:lesson_id>/', views.save_quiz_score, name='save_quiz_score'),
    path('quiz-history/', views.quiz_history, name='quiz_history'),

    # --- 3. ระบบเช็คชื่อและตารางเรียน (SMS) ---
    path('schedule/', views.view_schedule, name='view_schedule'),
    path('attendance/take/<int:schedule_id>/', views.take_attendance, name='take_attendance'),
    path('attendance/report/<int:classroom_id>/', views.monthly_attendance_report, name='monthly_attendance_report'),
    
    # QR Code ระบบที่ 1: ครูสแกนเด็ก
    path('attendance/scanner/<int:schedule_id>/', views.scanner_check_in, name='scanner_check_in'),
    # QR Code ระบบที่ 2: เด็กสแกนเครื่องครู
    path('attendance/show-qr/<int:schedule_id>/', views.teacher_show_qr, name='teacher_show_qr'),
    path('attendance/confirm/<int:schedule_id>/<str:token>/', views.student_confirm_attendance, name='student_confirm_attendance'),

    # --- 4. ระบบแจ้งลาออนไลน์ ---
    path('leave/submit/', views.submit_leave, name='submit_leave'),
    path('leave/list/', views.teacher_leave_list, name='teacher_leave_list'),

    # --- 5. ระบบเกรดและการแจ้งเตือน (MIS) ---
    path('grade/summary/<int:classroom_id>/', views.grade_summary, name='grade_summary'),
    path('grade/notify-parents/<int:classroom_id>/', views.send_grade_notifications, name='send_grade_notifications'),

    # --- 6. ระบบ Export ข้อมูล ---
    path('export/pdf/report/<int:student_id>/', views.export_pdf_report, name='export_pdf_report'),
    path('export/pdf/transcript/<int:student_id>/', views.export_student_grade_pdf, name='export_student_grade_pdf'),
    path('export/excel/attendance/<int:classroom_id>/', views.export_attendance_excel, name='export_attendance_excel'),
    path('export/excel/chat-logs/', views.export_chat_logs_excel, name='teacher_dashboard_export'),
]