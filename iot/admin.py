from django.contrib import admin
from .models import AttendanceLog

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    # กำหนดคอลัมน์ที่จะโชว์ในหน้าตาราง
    list_display = ('student', 'status', 'timestamp', 'method', 'device_id')
    # เพิ่มตัวกรองข้อมูลด้านข้าง
    list_filter = ('status', 'method', 'timestamp')
    # เพิ่มช่องค้นหาชื่อนักเรียน หรือรหัส
    search_fields = ('student__student_id', 'student__user__first_name')