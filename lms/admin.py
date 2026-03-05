from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AIChatLog, Course, Lesson, QuizScore, QuizQuestion, ParentProfile
from sms.models import Student
from .models import Schedule, Attendance, LeaveRequest, TermGrade

admin.site.register([Schedule, Attendance, LeaveRequest, TermGrade])

# 1. จัดการรายวิชา
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # เนื่องจาก Course ไม่มีฟิลด์ name_th โดยตรง เราจึงต้องดึงจาก subject มาแสดง
    list_display = ('get_subject_name', 'get_subject_code')
    
    def get_subject_name(self, obj):
        return obj.subject.name_th
    get_subject_name.short_description = 'ชื่อวิชา (ไทย)'

    def get_subject_code(self, obj):
        return obj.subject.code if hasattr(obj.subject, 'code') else "-"
    get_subject_code.short_description = 'รหัสวิชา'

# 2. จัดการบทเรียน
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    ordering = ('course', 'order')
        # แสดงสวิตช์เปิด-ปิดในหน้าตาราง
    list_display = ('title', 'course', 'enable_ai_chat', 'enable_quiz', 'enable_video', 'order')
    # ทำให้กดติ๊กถูก/ผิดได้ทันทีโดยไม่ต้องกดเข้าไปแก้ข้างใน
    list_editable = ('enable_ai_chat', 'enable_quiz', 'enable_video', 'order')
    list_filter = ('course', 'enable_ai_chat', 'enable_quiz')
    search_fields = ('title',)

# 3. จัดการคลังข้อสอบ
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'lesson', 'correct_answer')
    list_filter = ('lesson',)
    search_fields = ('question_text',)

# 4. ดูคะแนนสอบนักเรียน
@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score', 'total_questions', 'classroom', 'timestamp')
    list_filter = ('classroom', 'lesson', 'timestamp')
    search_fields = ('student__username', 'classroom')
    readonly_fields = ('timestamp',)

# 5. ดูประวัติการแชทกับ AI
@admin.register(AIChatLog)
class AIChatLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'timestamp')
    list_filter = ('lesson', 'timestamp')
    readonly_fields = ('student', 'lesson', 'question', 'answer', 'timestamp')

# 6. จัดการความสัมพันธ์ผู้ปกครอง-ลูก
@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('my_students',)
    search_fields = ('user__username', 'students__username')

