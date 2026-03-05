# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.db.models import Count

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    fieldsets = UserAdmin.fieldsets + (
        ('ข้อมูลเพิ่มเติม', {'fields': ('role', 'phone', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('ข้อมูลเพิ่มเติม', {'fields': ('role', 'phone', 'avatar')}),
    )

    # ✅ เพิ่มส่วนแสดงสรุปจำนวนในหน้ารายการ (Optional: โชว์ใน Changelist)
    def changelist_view(self, request, extra_context=None):
        counts = User.objects.values('role').annotate(total=Count('id'))
        # สร้างสรุปไว้อ่านง่ายๆ
        summary_text = " | ".join([f"{c['role'].upper()}: {c['total']}" for c in counts])
        
        extra_context = extra_context or {}
        extra_context['summary_text'] = summary_text
        return super().changelist_view(request, extra_context=extra_context)