# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('executive', 'Executive'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='profiles/', null=True, blank=True) # ตรวจสอบบรรทัดนี้

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
class Meta:
    permissions = [
        ("can_approve_repair", "สามารถอนุมัติงานซ่อมได้"),
        ("can_view_financial_report", "สามารถดูรายงานการเงินเชิงลึกได้"),
        ("can_manage_iot_gateways", "สามารถตั้งค่า Gateway ของ IoT ได้"),
    ]