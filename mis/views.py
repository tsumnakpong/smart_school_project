# mis/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
# สมมติว่ามี model เหล่านี้อยู่ในแอปอื่นๆ
# from sms.models import Student, Attendance
# from lms.models import Course
# ใน mis/views.py
from islamic.utils import get_prayer_times

def dashboard_view(request):
    prayer_times = get_prayer_times() # เรียกใช้ข้ามแอปได้เลย
    ...

class ExecutiveDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'mis/executive_dashboard.html'

    def test_func(self):
        # ตรวจสอบว่าต้องเป็นบทบาท executive เท่านั้น
        return self.request.user.role == 'executive'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ตัวอย่างข้อมูลสมมติ (ในงานจริงให้ Query จาก Database)
        context['summary'] = {
            'total_students': 1250,
            'avg_attendance': 94.5,
            'total_teachers': 85,
            'pending_fees': 45000,
        }
        
        # ข้อมูลสำหรับกราฟ (ส่งเป็น List ไปให้ Chart.js)
        context['chart_labels'] = ["ม.1", "ม.2", "ม.3", "ม.4", "ม.5", "ม.6"]
        context['chart_data'] = [85, 88, 75, 92, 80, 89] # คะแนนเฉลี่ยแต่ละระดับชั้น
        
        return context