from django.db import models
from django.conf import settings

# 1. ข้อมูลห้องเรียน
class Classroom(models.Model):
    name = models.CharField(max_length=50, verbose_name="ชื่อห้องเรียน") # เช่น ม.1/1
    year_level = models.IntegerField(verbose_name="ชั้นปี") # เช่น 7 (ม.1)
    
    def __str__(self):
        return self.name

# 2. ข้อมูลรายวิชา (รองรับ 2 สาย)
class Subject(models.Model):
    CATEGORY_CHOICES = (
        ('ACADEMIC', 'วิชาสามัญ'),
        ('RELIGIOUS', 'วิชาศาสนา'),
    )
    code = models.CharField(max_length=15, unique=True, verbose_name="รหัสวิชา")
    name_th = models.CharField(max_length=200, verbose_name="ชื่อวิชา (ไทย)")
    name_ar = models.CharField(max_length=200, blank=True, null=True, verbose_name="ชื่อวิชา (อาหรับ)")
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    credit = models.FloatField(default=1.0, verbose_name="หน่วยกิต")

    def __str__(self):
        return f"{self.code} - {self.name_th}"

# 3. ข้อมูลนักเรียน (เชื่อมกับ User ใน Core)
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=15, unique=True, verbose_name="เลขประจำตัวนักเรียน")
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, related_name='students')
    
    # ข้อมูลสำหรับต่อยอด AI (เช่น เกรดเฉลี่ยสะสม)
    gpax = models.FloatField(default=0.0, verbose_name="เกรดเฉลี่ยสะสม")

    def __str__(self):
        return f"{self.student_id} - {self.user.first_name} {self.user.last_name}"

# 4. การลงทะเบียนและเกรด
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.IntegerField(default=1) # ภาคเรียน
    year = models.IntegerField(default=2567) # ปีการศึกษา
    grade = models.FloatField(null=True, blank=True, verbose_name="เกรดที่ได้")

    class Meta:
        unique_together = ('student', 'subject', 'term', 'year')

# lms/models.py หรือสร้างแอปใหม่ชื่อ sms/models.py

class Schedule(models.Model):
    DAYS_OF_WEEK = (
        (1, 'จันทร์'),
        (2, 'อังคาร'),
        (3, 'พุธ'),
        (4, 'พฤหัสบดี'),
        (5, 'ศุกร์'),
        (6, 'เสาร์'),
        (7, 'อาทิตย์'),
    )
    
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sms_teacher_schedules' # ✅ ตั้งชื่อให้สื่อถึงแอป sms
        )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()} | {self.subject.name_th} ({self.classroom.name})"
    
