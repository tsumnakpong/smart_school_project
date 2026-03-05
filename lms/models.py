from django.db import models
from sms.models import Subject
from django.contrib.auth.models import User
from django.conf import settings # เพิ่มตัวนี้
from sms.models import Student # import มาใช้



class AIChatLog(models.Model):
    # เปลี่ยนจาก User เป็น settings.AUTH_USER_MODEL
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Course(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name='course')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='courses/', null=True, blank=True)

    def __str__(self):
        return self.subject.name_th

# lms/models.py

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255, verbose_name="หัวข้อบทเรียน")
    content = models.TextField(help_text="เนื้อหาบทเรียน (รองรับ Markdown หรือ HTML)", verbose_name="เนื้อหา")
    video_url = models.URLField(blank=True, help_text="ลิงก์วิดีโอจาก YouTube/Vimeo", verbose_name="ลิงก์วิดีโอ")
    order = models.PositiveIntegerField(default=0, verbose_name="ลำดับบทเรียน")

    # --- ส่วนที่เพิ่มใหม่: ระบบเปิด-ปิดฟีเจอร์ (Feature Toggles) ---
    enable_ai_chat = models.BooleanField(default=True, verbose_name="เปิดใช้งาน AI Tutor")
    enable_quiz = models.BooleanField(default=True, verbose_name="เปิดใช้งานระบบ Quiz")
    enable_video = models.BooleanField(default=True, verbose_name="แสดงวิดีโอประกอบ")
    
    # เพิ่มเติม: ระดับความยากของ AI (ตัวเลือกเสริมสำหรับครู)
    ai_complexity = models.CharField(
        max_length=20, 
        choices=[('easy', 'พื้นฐาน'), ('medium', 'ปานกลาง'), ('hard', 'ขั้นสูง')],
        default='medium',
        verbose_name="ระดับความยากของ AI"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "บทเรียน"
        verbose_name_plural = "บทเรียน"

    def __str__(self):
        return f"{self.course.subject.name_th} - {self.title}"

# lms/models.py

class QuizScore(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    classroom = models.CharField(max_length=10, default="6/1", verbose_name="ห้องเรียน") # เช่น 6/1, 6/2
# lms/models.py

class QuizQuestion(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.IntegerField(help_text="ใส่เลข 0-3 (0=ข้อแรก, 1=ข้อสอง...)")

    def __str__(self):
        return f"{self.lesson.title} - {self.question_text[:30]}"
    

# lms/models.py
class ParentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lms_parent_profile'
    )
    # ใช้ชื่อ 'sms.Student' เป็น String เพื่อเลี่ยง Error ตอนไขว้แอป
    my_students = models.ManyToManyField('sms.Student', related_name='parents')

    def __str__(self):
        return f"ผู้ปกครอง: {self.user.username}"
    
# lms/models.py

# lms/models.py

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lms_student_profile'
    )
    student_id = models.CharField(max_length=10, unique=True, verbose_name="เลขประจำตัวนักเรียน")
    
    # เปลี่ยนจาก CharField เป็น ForeignKey เพื่อเชื่อมกับห้องเรียนในแอป sms
    classroom = models.ForeignKey(
        'sms.Classroom', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="ห้องเรียน"
    )

    def __str__(self):
        # ดึงชื่อจาก User มาแสดงจะดูง่ายกว่าครับ
        return f"{self.user.first_name} - {self.classroom}"
    


class Notification(models.Model):
    TYPES = (
        ('score', 'แจ้งเตือนคะแนน'),
        ('warning', 'แจ้งเตือนพิเศษ'),
        ('info', 'ข่าวสาร'),
    )
    # ✅ แก้ไขจาก User เป็น settings.AUTH_USER_MODEL
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notif_type = models.CharField(max_length=10, choices=TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    

# lms/models.py

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'มาเรียน'),
        ('late', 'สาย'),
        ('absent', 'ขาดเรียน'),
        ('leave', 'ลา'),
    )
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'schedule', 'date')
        verbose_name = "การเข้าเรียน"
        verbose_name_plural = "การเข้าเรียน"

    # เพิ่มตัวนี้เพื่อให้เรียกใช้ใน Template ได้ง่ายขึ้น
    @property
    def is_present(self):
        return self.status == 'present'
    
# lms/models.py

class LeaveRequest(models.Model):
    LEAVE_TYPES = (
        ('sick', 'ลาป่วย'),
        ('errand', 'ลากิจ'),
        ('other', 'อื่นๆ'),
    )
    STATUS_CHOICES = (
        ('pending', 'รออนุมัติ'),
        ('approved', 'อนุมัติแล้ว'),
        ('rejected', 'ปฏิเสธ'),
    )
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.get_leave_type_display()} ({self.start_date})"
    
# lms/models.py

class TermGrade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # ✅ แก้ไขตรงนี้: ระบุเป็น 'sms.Subject' เพื่อบอก Django ว่าให้ไปดูที่แอป sms
    subject = models.ForeignKey(
        'sms.Subject', 
        on_delete=models.CASCADE, 
        related_name='lms_term_grades' # ตั้งชื่อให้ต่างจากแอปอื่น
    )
    
    term = models.IntegerField(default=1)
    year = models.IntegerField(default=2026)
    total_score = models.FloatField()
    grade = models.CharField(max_length=5)

    class Meta:
        unique_together = ('student', 'subject', 'term', 'year')

class Schedule(models.Model):
    DAYS_OF_WEEK = (
        (1, 'จันทร์'), (2, 'อังคาร'), (3, 'พุธ'), 
        (4, 'พฤหัสบดี'), (5, 'ศุกร์'), (6, 'เสาร์'), (7, 'อาทิตย์'),
    )
    
    # ✅ แก้ไข: ระบุชื่อแอปนำหน้า Model (สมมติว่า Classroom/Subject อยู่ในแอป sms)
    # ถ้าอยู่ในแอปอื่นให้เปลี่ยน 'sms' เป็นชื่อแอปนั้นๆ ครับ
    classroom = models.ForeignKey('sms.Classroom', on_delete=models.CASCADE, related_name='lms_schedules')
    subject = models.ForeignKey('sms.Subject', on_delete=models.CASCADE, related_name='lms_schedules')
    
    # ✅ แก้ไข: เพิ่ม related_name เพื่อไม่ให้ซ้ำกับแอป sms
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lms_teacher_schedules' 
    )
    
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

