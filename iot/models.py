from django.db import models
from sms.models import Student

class AttendanceLog(models.Model):
    STATUS_CHOICES = (
        ('PRESENT', 'มาเรียน'),
        ('LATE', 'สาย'),
        ('ABSENT', 'ขาด'),
    )
    # เชื่อมกับ Student ใน SMS
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    method = models.CharField(max_length=50) # เช่น "Face Recognition", "RFID"
    device_id = models.CharField(max_length=50) # ไอดีของกล้องหรือเครื่องสแกน

    def __str__(self):
        return f"{self.student.student_id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"