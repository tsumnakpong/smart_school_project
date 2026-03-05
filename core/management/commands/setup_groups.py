from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# นำเข้า Model ที่เราต้องการกำหนดสิทธิ์เฉพาะ (เช่น User ในแอป core)
from core.models import User 

class Command(BaseCommand):
    help = 'สร้างกลุ่มผู้ใช้งานและกำหนดสิทธิ์พื้นฐานอัตโนมัติ'

    def handle(self, *args, **options):
        # 1. นิยามกลุ่มและสิทธิ์ (App_label.codename)
        groups_data = {
            'Academic Admin': [
                'view_user', 'change_user', # สิทธิ์จัดการ User เบื้องต้น
            ],
            'Course Manager': [
                # ใส่สิทธิ์ของแอป lms เช่น 'add_course', 'change_lesson'
            ],
            'Technical Support': [
                'view_user',
            ],
            'Inventory Controller': [
                # ใส่สิทธิ์จัดการสต็อก
            ],
            'Financial Officer': [
                # ใส่สิทธิ์การเงิน
            ],
        }

        self.stdout.write(self.style.SUCCESS('--- กำลังเริ่มสร้างกลุ่มและสิทธิ์ ---'))

        for group_name, permissions in groups_data.items():
            # สร้างหรือดึงกลุ่มที่มีอยู่แล้ว
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'สร้างกลุ่ม: {group_name}')
            else:
                self.stdout.write(f'กลุ่ม {group_name} มีอยู่แล้ว')

            # กำหนดสิทธิ์ให้กลุ่ม
            for perm_code in permissions:
                try:
                    # ค้นหาสิทธิ์จาก codename
                    permission = Permission.objects.get(codename=perm_code)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  ⚠️ ไม่พบสิทธิ์: {perm_code}'))

        self.stdout.write(self.style.SUCCESS('--- ดำเนินการเสร็จสิ้น ---'))